# AGENTS.md instructions for /Users/atlanticroc/atlantida/repos/hive

This file provides guidance to non-Claude agents (e.g., Codex, Copilot) when working with code in this repository. It is vendor-native and should not override each vendor's own workflows. Claude's instructions live in `CLAUDE.md` and must not be edited by agents.

## Multi-Agent Role Boundaries

This repository implements a **three-CLI strategy** for optimal productivity:

| Agent | Role | Responsibilities | Boundaries |
|-------|------|------------------|------------|
| **Claude Code** | Planner & Architect | Complex thinking, architecture decisions, planning, context management | Writes to `.context/`, `docs/`, creates plans |
| **Codex** | Executor | Code implementation, follows plans, executes tasks | Reads plans, writes to `src/`, follows established patterns |
| **Copilot CLI** | Repository Manager | Git operations, PRs, commits, branches, GitHub workflows | Reads `.context/`, manages GitHub artifacts |
| **Copilot PR Review** | Quality Gate | Code review, feedback, approval | Reviews against `AGENTS.md` guidelines |

### Information Flow

```
┌─────────────┐    plans/context    ┌─────────────┐
│ Claude Code │ ─────────────────▶  │   Codex     │
│  (Planning) │                     │ (Execution) │
└─────────────┘                     └──────┬──────┘
       │                                   │
       │ .context/                         │ code changes
       ▼                                   ▼
┌─────────────┐    PR + commits    ┌─────────────┐
│ Copilot CLI │ ◀───────────────── │    src/     │
│  (Git Ops)  │                    │   (Code)    │
└──────┬──────┘                    └─────────────┘
       │
       │ PR
       ▼
┌─────────────┐
│Copilot Review│
│(Quality Gate)│
└─────────────┘
```

### Role-Specific Rules

#### For Codex
- **DO**: Execute implementation plans, write code, run tests
- **DO NOT**: Make architectural decisions, modify `.context/` or `docs/`
- **Input**: Plans from Claude, context from `.context/handoff.md`
- **Output**: Working code in `src/`

#### For Copilot CLI
- **DO**: Create PRs, write commits, manage branches, respond to reviews
- **DO NOT**: Implement features, modify context files, make design decisions
- **Input**: `.context/changelog.md` for PR context
- **Output**: Clean git history, descriptive PRs

#### For Copilot PR Review
- **DO**: Review code quality, catch bugs, ensure patterns are followed
- **DO NOT**: Approve changes that bypass the multi-agent workflow
- **Focus**: Code correctness, test coverage, adherence to `AGENTS.md`

## Source of Truth

The system's authoritative memory is:
- **`.context/` (working memory)** - short-term, task-focused context
- **`docs/` (long-term memory)** - durable project knowledge

Agents should treat `.context/` and `docs/` as the source of truth and keep them aligned with the current task state.

## Repository Purpose

This is an **AI-native collaborative workspace** designed as a meta-framework for multi-AI-agent development. The repository structure is optimized for AI comprehension and collaboration rather than traditional software patterns.

## Current State

This is a **template/scaffold repository** with empty placeholder files. No build system, dependencies, or source code exists yet. The repository is technology-agnostic and awaiting project initialization.

## Directory Structure (High-Level)

### AI Assistant Configurations
- **`.claude/`** - Claude Code specific configurations
- **`.codex/`** - Codex configurations (parallel structure to `.claude/`)
- **`.github/`** - GitHub Copilot configurations and workflows

### Context Management System (Source of Truth)
- **`.context/`** - Shared AI context files acting as working memory
- **`docs/`** - Long-term reference storage

### Source Code
- **`src/`** - Currently empty, awaiting implementation

## Context-Driven Development

Agents should follow a pull-work-push flow, keeping `.context/` lean and current while ensuring durable knowledge is stored in `docs/`.

### Task Lifecycle: Information Flow

1) **Task Start - Pull (`docs/` → `.context/`)**
   - Read `docs/` only as needed for the task.
   - Summarize key requirements into `.context/` files.
   - Avoid loading or copying large sections verbatim.

2) **During Task - Work (`.context/` only)**
   - Track reasoning and temporary notes in `.context/`.
   - Update task progress in `.context/`.
   - Read additional `docs/` files only if genuinely needed.

3) **Task End - Push & Clean (`.context/` → `docs/`)**
   - Persist decisions and outcomes in relevant `docs/` files.
   - Archive or clear temporary content from `.context/`.

### Size Constraints

Each `.context/` file should stay under **500 lines** to preserve efficient token usage. When approaching limits:
- Summarize older content
- Move details to `docs/`
- Archive completed items
- Delete truly temporary notes

### File-Specific Guidance for `.context/`

| File | Purpose | Lifecycle | Cleanup Pattern |
|------|---------|-----------|-----------------|
| `handoff.md` | Context for next session/agent | Update at task end | Clear after successful handoff |
| `notes.md` | Temporary reasoning & notes | During task | Clear frequently; keep 10-20 line summary at task end |
| `todo.md` | Current task tracking | During task | Archive completed tasks to sprint notes |
| `changelog.md` | Recent decisions | During task | Move older entries to `docs/` |
| `runbook.md` | Operational procedures | Stable reference | Update only when procedures change |

## Development Commands

None exist yet. This section will be populated after project initialization.
