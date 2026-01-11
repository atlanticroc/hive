Create a session handoff by updating context files for the next session.

## Process

### 1. Update INDEX.md
Update `.context/INDEX.md` with current status:
- Session date
- Sprint/story status
- 1-line handoff summary
- Pending task count
- File line counts and summaries

### 2. Create Handoff Document
Write `.context/handoff.md` with:

**Session Context** (5 lines max)
- Date, sprint/story, session focus

**What Was Accomplished** (10-15 lines)
- Summary of completed tasks
- Key changes made

**Current State** (5 lines)
- In progress items
- Blockers
- Build/test status

**Next Steps** (5-10 lines)
- Immediate actions for next session
- Key files to review

**Keep total under 50 lines.**

### 3. Clean notes.md
Clear `.context/notes.md` except:
- Keep last 10-20 lines as "Previous Session Summary"
- Delete all other temporary reasoning

### 4. Prune changelog.md
If `.context/changelog.md` exceeds 100 lines:
- Move entries older than current sprint to `docs/product/adr.md`
- Keep only recent decisions (last 2-3 sessions)

### 5. Archive Completed Tasks
Move completed tasks from `.context/todo.md` to sprint notes:
- Keep only pending tasks in todo.md
- Target: <30 lines in todo.md

### 6. Provide Summary
Tell the user:
- What was saved to handoff.md
- Files cleaned/pruned
- Ready for next session

## Handoff Template

```markdown
# Handoff - [Brief Title]

## Session Context
- **Date**: YYYY-MM-DD
- **Sprint/Story**: [status]
- **Focus**: [1-line description]

## Accomplished
- [bullet points of completed work]

## Current State
- **In Progress**: [or "None"]
- **Blockers**: [or "None"]
- **Build/Test**: [status]

## Next Steps
1. [immediate action]
2. [next action]

## Key Files
- [file]: [why relevant]
```

## Guidelines

**DO:**
- Keep handoff.md under 50 lines
- Update INDEX.md every time
- Clean notes.md aggressively
- Prune changelog.md when >100 lines

**DON'T:**
- Include full code snippets
- Copy entire documents
- Keep stale information
- Exceed line limits
