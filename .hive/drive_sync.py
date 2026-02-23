#!/usr/bin/env python3
"""
One-way (local -> Google Drive) sync with live updates.

Requires Google Drive API credentials (OAuth client) and the following deps:
  - google-api-python-client
  - google-auth-httplib2
  - google-auth-oauthlib
  - watchdog
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import sys
import threading
import time
from pathlib import Path
from typing import Dict, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

SCOPES = ["https://www.googleapis.com/auth/drive"]
FOLDER_MIME = "application/vnd.google-apps.folder"


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        return {}


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True))


def _expand_path(path: str) -> Path:
    return Path(os.path.expanduser(path)).resolve()


class DriveSyncer:
    def __init__(
        self,
        service,
        local_root: Path,
        drive_folder_id: Optional[str],
        drive_folder_name: str,
        state_path: Path,
        exclude: list[str],
        delete_remote: bool,
    ) -> None:
        self.service = service
        self.local_root = local_root
        self.state_path = state_path
        self.exclude = exclude
        self.delete_remote = delete_remote

        self.state = _load_json(state_path)
        self.state.setdefault("folders", {})
        self.state.setdefault("files", {})

        self.folder_cache: Dict[str, str] = dict(self.state["folders"])

        if drive_folder_id:
            self.root_folder_id = drive_folder_id
        else:
            self.root_folder_id = self._get_or_create_folder(
                drive_folder_name, parent_id="root"
            )

        self.folder_cache[""] = self.root_folder_id
        self._save_state()

    def _save_state(self) -> None:
        self.state["folders"] = self.folder_cache
        _write_json(self.state_path, self.state)

    def _match_exclude(self, rel_path: str) -> bool:
        if any(part.startswith(".") for part in Path(rel_path).parts):
            return True
        for pattern in self.exclude:
            if fnmatch.fnmatch(rel_path, pattern):
                return True
        return False

    def _query(self, q: str):
        return (
            self.service.files()
            .list(
                q=q,
                spaces="drive",
                fields="files(id,name,parents,mimeType)",
                pageSize=10,
            )
            .execute()
            .get("files", [])
        )

    def _get_or_create_folder(self, name: str, parent_id: str) -> str:
        safe_name = name.replace("'", "\\'")
        query = (
            f"mimeType='{FOLDER_MIME}' and name='{safe_name}' "
            f"and '{parent_id}' in parents and trashed=false"
        )
        items = self._query(query)
        if items:
            return items[0]["id"]

        metadata = {"name": name, "mimeType": FOLDER_MIME, "parents": [parent_id]}
        created = (
            self.service.files()
            .create(body=metadata, fields="id")
            .execute()
        )
        return created["id"]

    def _ensure_drive_folder(self, rel_dir: str) -> str:
        rel_dir = rel_dir.strip("/")
        if rel_dir in self.folder_cache:
            return self.folder_cache[rel_dir]

        parts = rel_dir.split("/") if rel_dir else []
        parent_id = self.folder_cache[""]
        current = ""
        for part in parts:
            current = f"{current}/{part}" if current else part
            if current in self.folder_cache:
                parent_id = self.folder_cache[current]
                continue
            folder_id = self._get_or_create_folder(part, parent_id)
            self.folder_cache[current] = folder_id
            parent_id = folder_id

        self._save_state()
        return parent_id

    def _find_file_id(self, name: str, parent_id: str) -> Optional[str]:
        safe_name = name.replace("'", "\\'")
        query = (
            f"name='{safe_name}' and '{parent_id}' in parents "
            "and trashed=false"
        )
        items = self._query(query)
        if items:
            return items[0]["id"]
        return None

    def _should_upload(self, rel_path: str, mtime: float, size: int) -> bool:
        info = self.state["files"].get(rel_path)
        if not info:
            return True
        return info.get("mtime") != mtime or info.get("size") != size

    def upload_file(self, local_path: Path) -> None:
        if not local_path.is_file():
            return
        rel_path = str(local_path.relative_to(self.local_root))
        if self._match_exclude(rel_path):
            return

        stat = local_path.stat()
        mtime = stat.st_mtime
        size = stat.st_size
        if not self._should_upload(rel_path, mtime, size):
            return

        rel_dir = str(Path(rel_path).parent)
        parent_id = self._ensure_drive_folder("" if rel_dir == "." else rel_dir)

        file_id = self.state["files"].get(rel_path, {}).get("id")
        if not file_id:
            file_id = self._find_file_id(local_path.name, parent_id)

        media = MediaFileUpload(str(local_path), resumable=True)

        if file_id:
            self.service.files().update(fileId=file_id, media_body=media).execute()
        else:
            metadata = {"name": local_path.name, "parents": [parent_id]}
            created = (
                self.service.files()
                .create(body=metadata, media_body=media, fields="id")
                .execute()
            )
            file_id = created["id"]

        self.state["files"][rel_path] = {
            "id": file_id,
            "mtime": mtime,
            "size": size,
        }
        self._save_state()

    def delete_file(self, local_path: Path) -> None:
        rel_path = str(local_path.relative_to(self.local_root))
        info = self.state["files"].get(rel_path)
        if not info:
            return
        file_id = info.get("id")
        if not file_id:
            return
        try:
            self.service.files().delete(fileId=file_id).execute()
        except HttpError:
            pass
        self.state["files"].pop(rel_path, None)
        self._save_state()

    def initial_sync(self) -> None:
        for path in self.local_root.rglob("*"):
            if path.is_file():
                try:
                    self.upload_file(path)
                except HttpError as exc:
                    print(f"Drive error uploading {path}: {exc}", file=sys.stderr)


class DebouncedHandler(FileSystemEventHandler):
    def __init__(self, syncer: DriveSyncer, debounce_seconds: float) -> None:
        super().__init__()
        self.syncer = syncer
        self.debounce = debounce_seconds
        self._timers: Dict[Path, threading.Timer] = {}
        self._lock = threading.Lock()

    def _schedule(self, path: Path) -> None:
        if path.is_dir():
            return
        with self._lock:
            timer = self._timers.get(path)
            if timer:
                timer.cancel()
            timer = threading.Timer(self.debounce, self._run, args=(path,))
            timer.daemon = True
            self._timers[path] = timer
            timer.start()

    def _run(self, path: Path) -> None:
        with self._lock:
            self._timers.pop(path, None)
        try:
            self.syncer.upload_file(path)
        except HttpError as exc:
            print(f"Drive error uploading {path}: {exc}", file=sys.stderr)

    def on_created(self, event) -> None:
        self._schedule(Path(event.src_path))

    def on_modified(self, event) -> None:
        self._schedule(Path(event.src_path))

    def on_moved(self, event) -> None:
        dest = Path(event.dest_path)
        self._schedule(dest)
        if self.syncer.delete_remote:
            self.syncer.delete_file(Path(event.src_path))

    def on_deleted(self, event) -> None:
        if self.syncer.delete_remote:
            self.syncer.delete_file(Path(event.src_path))


def _get_credentials(credentials_path: Path, token_path: Path) -> Credentials:
    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)
        _write_json(token_path, json.loads(creds.to_json()))
    return creds


def _build_service(creds: Credentials):
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="One-way Google Drive sync.")
    parser.add_argument(
        "--local",
        required=True,
        help="Local folder to sync (one-way to Drive).",
    )
    parser.add_argument(
        "--drive-folder-name",
        default="docs",
        help="Drive folder name to create/use in My Drive.",
    )
    parser.add_argument(
        "--drive-folder-id",
        default=None,
        help="Existing Drive folder ID to sync into.",
    )
    parser.add_argument(
        "--credentials",
        required=True,
        help="Path to OAuth client credentials.json.",
    )
    parser.add_argument(
        "--token",
        default="~/.config/drive-sync/token.json",
        help="Path to store OAuth token.json.",
    )
    parser.add_argument(
        "--state",
        default="~/.config/drive-sync/state.json",
        help="Path to store sync state.",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=["*.tmp", "*.swp", ".DS_Store"],
        help="Glob patterns to exclude; may be repeated.",
    )
    parser.add_argument(
        "--delete-remote",
        action="store_true",
        help="If set, delete Drive files when local files are deleted.",
    )
    parser.add_argument(
        "--debounce",
        type=float,
        default=1.0,
        help="Seconds to debounce file changes before upload.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    local_root = _expand_path(args.local)
    if not local_root.exists():
        raise SystemExit(f"Local path does not exist: {local_root}")

    credentials_path = _expand_path(args.credentials)
    token_path = _expand_path(args.token)
    state_path = _expand_path(args.state)

    creds = _get_credentials(credentials_path, token_path)
    service = _build_service(creds)

    syncer = DriveSyncer(
        service=service,
        local_root=local_root,
        drive_folder_id=args.drive_folder_id,
        drive_folder_name=args.drive_folder_name,
        state_path=state_path,
        exclude=args.exclude,
        delete_remote=args.delete_remote,
    )

    syncer.initial_sync()

    handler = DebouncedHandler(syncer, args.debounce)
    observer = Observer()
    observer.schedule(handler, str(local_root), recursive=True)
    observer.start()

    print(f"Watching {local_root} for changes. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
