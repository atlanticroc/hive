# Memory Hierarchy & Context Management

This document explains the two-tier memory system for AI context management in this repository.

## Overview

The repository implements progressive disclosure of context:

| Tier | Location | Token Cost | Load When |
|------|----------|------------|-----------|
| **Tier 0** | CLAUDE.md, INDEX.md | ~700 | Always |
| **Tier 1** | .context/*.md | On-demand | Task start |
| **Tier 2** | docs/**/*.md | On-demand | Specific need |

## Two-Tier Memory System

### Working Memory (.context/)
- **Purpose**: Task-focused, session-scoped information
- **Constraint**: Max 500 lines per file
- **Files**:
  - `INDEX.md` - Status pointer (always read first)
  - `handoff.md` - Session continuity
  - `todo.md` - Current task tracking
  - `notes.md` - Temporary reasoning (clear at task end)
  - `changelog.md` - Recent decisions (rolling window)

### Reference Storage (docs/)
- **Purpose**: Comprehensive, permanent documentation
- **Load**: On-demand only
- **Directories**:
  - `docs/product/` - Product vision, architecture, ADRs
  - `docs/project/` - Sprints, stories, backlog
  - `docs/guides/` - Reference documentation (this file)

## Task Lifecycle

### 1. Task Start (Pull)

```
Read INDEX.md → Understand current state
     ↓
Determine task type:
  - Continue work → Read handoff.md, todo.md
  - New feature → Run /bootstrap-context
  - Bug fix → Read todo.md, relevant source
  - Planning → Read backlog.md, velocity.md
     ↓
Summarize into notes.md (max 50 lines)
```

### 2. During Task (Work)

- Use notes.md for temporary reasoning
- Update todo.md with progress
- Record decisions in changelog.md
- Avoid re-reading docs already summarized

### 3. Task End (Push & Clean)

```
Run /handoff
     ↓
Updates INDEX.md with current status
     ↓
Clears notes.md (keeps 10-20 line summary)
     ↓
Prunes changelog.md if >100 lines
     ↓
Creates handoff.md for next session
```

## File-Specific Guidelines

| File | Max Lines | Lifecycle | Cleanup Trigger |
|------|-----------|-----------|-----------------|
| INDEX.md | 35 | Updated each /handoff | Always current |
| handoff.md | 100 | Updated at task end | After successful handoff |
| todo.md | 50 | During task | Archive completed to sprint |
| notes.md | 50 | During task | Clear at task end |
| changelog.md | 100 | During task | Move old entries to ADR |

## Size Management

**When approaching limits:**
1. Summarize older content
2. Move details to appropriate docs/ files
3. Archive completed items
4. Delete truly temporary content

**Example**: If changelog.md reaches 80 lines, move entries older than current sprint to `docs/product/adr.md`.

## Commands

| Command | Context Behavior |
|---------|------------------|
| /bootstrap-context | Loads docs/ selectively based on task type |
| /handoff | Updates INDEX.md, cleans notes.md, prunes changelog.md |
| /story-start | Loads story into todo.md and notes.md |
| /story-complete | Archives story, updates sprint progress |
| /sprint-plan | Loads backlog.md, velocity.md |
| /sprint-review | Archives sprint, updates velocity.md |

## Token Efficiency Goals

| Metric | Target |
|--------|--------|
| CLAUDE.md | <60 lines (~700 tokens) |
| INDEX.md | <35 lines (~400 tokens) |
| Total .context/ | <200 lines (~2,500 tokens) |
| Session startup overhead | <1,100 tokens |

## Anti-Patterns

**Don't:**
- Load entire docs/ directory at session start
- Copy full documents into .context/ files
- Keep notes.md content across sessions
- Let changelog.md grow unbounded

**Do:**
- Read INDEX.md first for situational awareness
- Load only files relevant to current task
- Summarize, don't copy
- Clean up at task end via /handoff
