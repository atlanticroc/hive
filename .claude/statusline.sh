#!/usr/bin/env bash
# Claude Code custom status line
# Output: single line of text shown below the input prompt

set -euo pipefail

parts=()

# ── Project name ──
proj=$(basename "$(git rev-parse --show-toplevel 2>/dev/null || basename "$PWD")")
parts+=("📦 $proj")

# ── Git branch + status ──
if git rev-parse --is-inside-work-tree &>/dev/null; then
  branch=$(git symbolic-ref --short HEAD 2>/dev/null || git rev-parse --short HEAD)
  dirty=""
  [[ -n $(git status --porcelain 2>/dev/null) ]] && dirty="*"

  ahead_behind=""
  counts=$(git rev-list --left-right --count HEAD...@{upstream} 2>/dev/null || true)
  if [[ -n "$counts" ]]; then
    ahead=$(echo "$counts" | awk '{print $1}')
    behind=$(echo "$counts" | awk '{print $2}')
    [[ "$ahead"  -gt 0 ]] && ahead_behind+="↑${ahead}"
    [[ "$behind" -gt 0 ]] && ahead_behind+="↓${behind}"
  fi

  parts+=("🌿 ${branch}${dirty}${ahead_behind:+ $ahead_behind}")
fi

# ── Python / uv environment ──
py_ver=$(python3 --version 2>/dev/null | awk '{print $2}')
venv=""
if [[ -n "${VIRTUAL_ENV:-}" ]]; then
  venv=$(basename "$VIRTUAL_ENV")
elif [[ -f .python-version ]]; then
  venv="uv:$(cat .python-version | tr -d '[:space:]')"
fi
[[ -n "$py_ver" ]] && parts+=("🐍 ${py_ver}${venv:+ ($venv)}")

# ── Sprint / task context ──
sprint_file="docs/ops/project/sprints/active-sprints.md"
story_file="docs/ops/project/stories/active-stories.md"
ctx=""
if [[ -s "$sprint_file" ]]; then
  ctx=$(head -5 "$sprint_file" | grep -m1 -oE 'sprint-s[0-9]+|S[0-9]+' || true)
fi
if [[ -z "$ctx" && -s "$story_file" ]]; then
  ctx=$(head -5 "$story_file" | grep -m1 -oE 'story-s[0-9]+-[0-9]+|S[0-9]+-[0-9]+' || true)
fi
[[ -n "$ctx" ]] && parts+=("🎯 $ctx")

# ── System resources ──
if command -v vm_stat &>/dev/null; then
  # macOS
  cpu=$(ps -A -o %cpu | awk '{s+=$1} END {printf "%.0f", s}')
  pages_free=$(vm_stat | awk '/Pages free/ {gsub(/\./,"",$3); print $3}')
  pages_active=$(vm_stat | awk '/Pages active/ {gsub(/\./,"",$3); print $3}')
  pages_spec=$(vm_stat | awk '/Pages speculative/ {gsub(/\./,"",$3); print $3}')
  pages_wired=$(vm_stat | awk '/Pages wired/ {gsub(/\./,"",$3); print $3}')
  total=$((pages_free + pages_active + pages_spec + pages_wired))
  used=$((pages_active + pages_wired))
  if [[ $total -gt 0 ]]; then
    mem_pct=$((used * 100 / total))
  else
    mem_pct=0
  fi
  parts+=("⚡ cpu:${cpu}% mem:${mem_pct}%")
fi

# ── Output ──
IFS=' │ '
echo "${parts[*]}"