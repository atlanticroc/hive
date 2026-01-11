# /sprint-review

Close the current sprint, capture learnings, and update velocity.

## Prerequisites

- An active sprint exists in `docs/project/sprints/current-sprint.md`
- Sprint end date has passed (or user wants to close early)

## Process

### 1. Gather Sprint Data

Read `docs/project/sprints/current-sprint.md`:
- Sprint number and goal
- Start and end dates
- All committed stories with their status
- Points committed vs completed

Calculate:
- **Velocity**: Total points of completed stories
- **Completion rate**: Completed stories / Committed stories
- **Carryover**: Stories not completed (if any)

### 2. Review with User

Present sprint summary and ask:

**What went well?**
- Accomplishments, learnings, wins

**What could improve?**
- Blockers, challenges, process issues

**Carryover decision** (if incomplete stories):
- Move back to backlog Priority 1?
- Continue in next sprint?
- Deprioritize to Priority 2/3?

### 3. Archive the Sprint

Create archive file at `docs/project/sprints/archive/sprint-N.md`:

```markdown
# Sprint N: [Goal] (Archived)

**Dates**: YYYY-MM-DD → YYYY-MM-DD
**Velocity**: X points completed

## Results

| ID | Title | Points | Status |
|----|-------|--------|--------|
| STORY-XXX | [Title] | X | Done |
| STORY-XXY | [Title] | Y | Done |
| STORY-XXZ | [Title] | Z | Carried Over |

**Committed**: X points | **Completed**: Y points | **Velocity**: Y

## Retrospective

### What Went Well
- [User input]

### What Could Improve
- [User input]

### Action Items
- [Any process improvements for next sprint]

## Notes

[Any additional notes from sprint]

---
Archived: YYYY-MM-DD
```

### 4. Update Velocity Tracking

Edit `docs/project/velocity.md`:

Add row to Sprint History table:
```
| N | [Goal] | X | Y | Y | [Notes] |
```

Update metrics:
- Recalculate average velocity
- Update best sprint if applicable
- Note trend (improving/stable/declining)

### 5. Handle Carryover Stories

For incomplete stories based on user decision:

**Move to backlog:**
- Add story back to `docs/project/backlog.md` Priority 1
- Note "Carried over from Sprint N"

**Continue in next sprint:**
- Keep in backlog Priority 1, will be auto-suggested in next `/sprint-plan`

### 6. Reset Sprint File

Write placeholder to `docs/project/sprints/current-sprint.md`:

```markdown
# Current Sprint

> No active sprint. Use `/sprint-plan` to start a new sprint.

## Previous Sprint Summary

- **Sprint N**: [Goal]
- **Velocity**: X points
- **Completed**: YYYY-MM-DD

Use `/sprint-plan` to start Sprint N+1.
```

### 7. Update Context

Update `.context/notes.md`:
- Clear sprint-specific content
- Note sprint completion

Update `.context/changelog.md`:
- Add entry for sprint completion with velocity

Update `.context/handoff.md`:
- Record sprint review for next session
- Note velocity and any carryover

### 8. Confirm Review Complete

Output summary:

```
Sprint N Review Complete

Results:
- Goal: [Goal]
- Velocity: X points (Y committed)
- Completion: Z%
- Stories: A completed, B carried over

Retrospective captured in: docs/project/sprints/archive/sprint-N.md

Average Velocity: X points/sprint
Trend: [improving/stable/declining]

Ready for Sprint N+1. Use `/sprint-plan` when ready.
```

## Guidelines

- **Honest assessment**: Velocity is for planning, not performance judgment
- **Capture learnings**: Retrospective notes improve future sprints
- **Handle carryover**: Don't let incomplete work disappear
- **Update velocity**: Accurate velocity improves planning accuracy
