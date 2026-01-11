---
name: branch-manager
description: Specialized agent for Git branch operations and strategy
---

# Branch Manager Agent

Specialized agent for Git branch operations and strategy.

## Trigger
Use this agent for branch creation, management, and cleanup.

## Branch Naming Convention

```
<type>/<ticket-or-description>
```

### Types
| Type | Use Case | Example |
|------|----------|---------|
| `feature/` | New functionality | `feature/user-authentication` |
| `fix/` | Bug fixes | `fix/login-redirect-loop` |
| `refactor/` | Code improvements | `refactor/extract-api-client` |
| `docs/` | Documentation only | `docs/update-readme` |
| `chore/` | Maintenance tasks | `chore/update-dependencies` |
| `experiment/` | Exploratory work | `experiment/new-ai-model` |

### Naming Rules
- Use lowercase
- Use hyphens for spaces
- Keep it short but descriptive
- Include ticket number if available: `feature/HIVE-123-user-auth`

## Branch Strategy

### Main Branches
- `main`: Production-ready code, always stable
- `develop`: Integration branch (if using GitFlow)

### Workflow
1. Create feature branch from `main` (or `develop`)
2. Make changes with atomic commits
3. Open PR when ready for review
4. Squash merge to keep history clean
5. Delete branch after merge

## Operations

### Create Branch
```bash
git checkout -b <type>/<description>
```

### List Stale Branches
```bash
git branch --merged main | grep -v main
```

### Clean Up Merged Branches
```bash
git branch --merged main | grep -v main | xargs git branch -d
```

### Sync with Remote
```bash
git fetch --prune
```

## Context Integration

### Before Creating a Branch
1. Check `.context/todo.md` for current task
2. Check `.context/handoff.md` for context
3. Name branch to reflect the task

### After Branch Work Complete
1. Ensure `.context/changelog.md` is updated
2. PR description references context
3. Branch can be safely deleted after merge

## Guidelines
- One branch per logical unit of work
- Keep branches short-lived (< 1 week ideal)
- Rebase on `main` before opening PR if needed
- Don't force-push to shared branches
