# CLAUDE.md

AI-native collaborative workspace for multi-AI-agent development. Currently a template/scaffold awaiting project initialization.

## Essential Constraints
- **Token efficiency**: Load only context needed for current task
- **File limits**: Each .context/ file max 500 lines
- **Pattern**: .context/ is working memory, docs/ is reference storage

## Context Files (.context/)

| File | Purpose | Read When |
|------|---------|-----------|
| INDEX.md | Status & pointers | Always read first |
| handoff.md | Session continuity | Continuing previous work |
| todo.md | Task tracking | During any task |
| notes.md | Temporary reasoning | During task (clear at end) |
| changelog.md | Recent decisions | Making architectural choices |

## Available Commands

| Command | Purpose |
|---------|---------|
| /bootstrap-context | Load task context from docs/ |
| /bootstrap-product | Create product vision (research-backed) |
| /story-create | Add story to backlog |
| /story-start | Begin story implementation |
| /story-complete | Archive completed story |
| /sprint-plan | Start new 2-week sprint |
| /sprint-review | Close sprint, update velocity |
| /handoff | Create session handoff |

## Directory Map
```
.claude/       Commands, skills, hooks
.context/      Working memory (read INDEX.md first)
docs/product/  Product vision, architecture, ADRs
docs/project/  Sprints, stories, backlog
docs/guides/   Reference documentation
src/           Source code (empty)
```

## Workflow
1. **Start**: Read .context/INDEX.md
2. **If continuing**: Read handoff.md, todo.md
3. **If new task**: Run /bootstrap-context
4. **During**: Use notes.md, update todo.md
5. **End**: Run /handoff

---
Full documentation: docs/guides/memory-hierarchy.md
