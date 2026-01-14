#!/usr/bin/env python3
"""
Fetch sample METAR data from official sources.

Examples:
  python src/metar_samples.py --source iem --station LPMA --start 2024-01-01 --end 2024-02-01 --out /tmp/lpma.csv
  python src/metar_samples.py --source awc --station LPMA --hours 24 --format json
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import gzip
import json
import sys
import urllib.parse
import urllib.request

IEM_BASE = "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py"
AWC_BASE = "https://aviationweather.gov/api/data"


def _iso_z(value: str, default_time: str) -> str:
    if "T" in value:
        return value
    return f"{value}T{default_time}Z"


def _read_response(resp: urllib.response.addinfourl) -> bytes:
    payload = resp.read()
    if resp.headers.get("Content-Encoding") == "gzip":
        return gzip.decompress(payload)
    return payload


def _fetch(url: str, user_agent: str, timeout: int) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": user_agent})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return _read_response(resp)


def build_iem_url(
    stations: list[str],
    start: str,
    end: str,
    data_fields: list[str],
    tz: str,
    fmt: str,
    missing: str,
    trace: str,
) -> str:
    params: list[tuple[str, str]] = []
    for field in data_fields:
        params.append(("data", field))
    for station in stations:
        params.append(("station", station))
    params.extend(
        [
            ("sts", _iso_z(start, "00:00:00")),
            ("ets", _iso_z(end, "00:00:00")),
            ("tz", tz),
            ("format", fmt),
            ("missing", missing),
            ("trace", trace),
        ]
    )
    return f"{IEM_BASE}?{urllib.parse.urlencode(params, doseq=True)}"


def build_awc_metar_url(stations: list[str], fmt: str) -> str:
    params = {
        "ids": ",".join(stations),
        "format": fmt,
    }
    return f"{AWC_BASE}/metar?{urllib.parse.urlencode(params)}"


def build_awc_dataserver_url(
    stations: list[str],
    fmt: str,
    start: str | None,
    end: str | None,
    hours: int | None,
) -> str:
    params = {
        "dataSource": "metars",
        "requestType": "retrieve",
        "stationString": ",".join(stations),
        "format": fmt,
    }
    if start and end:
        params["startTime"] = _iso_z(start, "00:00:00")
        params["endTime"] = _iso_z(end, "00:00:00")
    elif hours is not None:
        params["hoursBeforeNow"] = str(hours)
    return f"{AWC_BASE}/dataserver?{urllib.parse.urlencode(params)}"


def summarize_csv(payload: bytes) -> tuple[int, list[str]]:
    text = payload.decode("utf-8", errors="replace")
    reader = csv.reader(text.splitlines())
    rows = list(reader)
    if not rows:
        return 0, []
    header = rows[0]
    return max(len(rows) - 1, 0), header


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch sample METAR data.")
    parser.add_argument("--source", choices=["iem", "awc"], required=True)
    parser.add_argument("--station", action="append", required=True)
    parser.add_argument("--start", help="Start date (YYYY-MM-DD or ISO8601).")
    parser.add_argument("--end", help="End date (YYYY-MM-DD or ISO8601).")
    parser.add_argument("--hours", type=int, help="Hours before now (AWC dataserver).")
    parser.add_argument("--format", default="csv", help="Output format (csv/json/xml/raw).")
    parser.add_argument("--data", action="append", help="IEM data fields (repeatable).")
    parser.add_argument("--tz", default="UTC", help="Timezone for IEM request.")
    parser.add_argument("--missing", default="M", help="Missing value marker (IEM).")
    parser.add_argument("--trace", default="0.0001", help="Trace value marker (IEM).")
    parser.add_argument("--user-agent", default="lpma-metar-sampler/0.1")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--out", help="Output file path (default: stdout).")
    parser.add_argument("--summary", action="store_true", help="Print row count summary.")
    parser.add_argument("--validate", action="store_true", help="Validate CSV has data.")
    args = parser.parse_args()

    data_fields = args.data or ["all"]

    if args.source == "iem":
        if not args.start or not args.end:
            parser.error("--start and --end are required for IEM requests.")
        url = build_iem_url(
            stations=args.station,
            start=args.start,
            end=args.end,
            data_fields=data_fields,
            tz=args.tz,
            fmt=args.format,
            missing=args.missing,
            trace=args.trace,
        )
    else:
        if args.start and args.end:
            url = build_awc_dataserver_url(
                stations=args.station,
                fmt=args.format,
                start=args.start,
                end=args.end,
                hours=args.hours,
            )
        elif args.hours is not None:
            url = build_awc_dataserver_url(
                stations=args.station,
                fmt=args.format,
                start=None,
                end=None,
                hours=args.hours,
            )
        else:
            url = build_awc_metar_url(args.station, args.format)

    payload = _fetch(url, args.user_agent, args.timeout)

    if args.summary or args.validate:
        if args.format.lower() == "csv":
            rows, header = summarize_csv(payload)
            print(f"rows={rows} columns={len(header)}", file=sys.stderr)
            if args.validate and rows == 0:
                print("no data rows returned", file=sys.stderr)
                return 1
        elif args.format.lower() == "json":
            data = json.loads(payload.decode("utf-8", errors="replace"))
            count = len(data) if isinstance(data, list) else 1
            print(f"records={count}", file=sys.stderr)

    if args.out:
        with open(args.out, "wb") as handle:
            handle.write(payload)
    else:
        sys.stdout.buffer.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
