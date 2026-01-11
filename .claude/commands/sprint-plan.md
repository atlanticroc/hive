# /sprint-plan

Start a new sprint by selecting stories from the backlog.

## Prerequisites

- No active sprint (or previous sprint has been reviewed with `/sprint-review`)
- Stories exist in `docs/project/backlog.md` Priority 1 section

If a sprint is active, prompt user to run `/sprint-review` first.

## Process

### 1. Check Current State

Read `docs/project/sprints/current-sprint.md`:
- If sprint is active (has stories), ask user to complete it first
- If empty/placeholder, proceed

Read `docs/project/velocity.md`:
- Get average velocity for capacity planning
- If no history, suggest starting with 15-20 points

### 2. Determine Sprint Number

Check `docs/project/sprints/archive/` for existing sprints.
New sprint = highest sprint number + 1, or Sprint 1 if none exist.

### 3. Get Sprint Details

Ask user using AskUserQuestion:

**Required:**
- **Sprint Goal**: One sentence describing what this sprint achieves
- **Start Date**: Default to today (YYYY-MM-DD)

**Calculated:**
- **End Date**: Start date + 14 days (2-week sprint)
- **Capacity**: Based on velocity (or 15-20 for first sprint)

### 4. Select Stories

Read `docs/project/backlog.md` and display Priority 1 stories.

Ask user to select stories for the sprint:
- Show story ID, title, and points
- Running total of points vs capacity
- Warn if exceeding capacity

User can also pull from Priority 2 if Priority 1 is empty.

### 5. Create Sprint File

Write to `docs/project/sprints/current-sprint.md`:

```markdown
# Sprint N: [Goal]

**Dates**: YYYY-MM-DD → YYYY-MM-DD (2 weeks)
**Capacity**: X points (based on velocity: Y)

## Sprint Backlog

| ID | Title | Points | Status |
|----|-------|--------|--------|
| STORY-XXX | [Title] | X | Not Started |
| STORY-XXY | [Title] | Y | Not Started |
| STORY-XXZ | [Title] | Z | Not Started |

**Total Committed**: X points

## Progress

- **Completed**: 0 / X points (0%)
- **Stories Done**: 0 / N

## Daily Log

<!-- Optional: Track daily progress -->

### YYYY-MM-DD (Day 1)
- Sprint started

## Notes

<!-- Blockers, scope changes, decisions -->

---
Use `/story-start` to begin work on a story.
Use `/sprint-review` at sprint end.
```

### 6. Update Context

Update `.context/notes.md`:
- Add "## Sprint N: [Goal]" section
- List committed stories for quick reference

Update `.context/todo.md`:
- Add sprint planning complete
- Note first story to start

Update `.context/handoff.md`:
- Record sprint start for session continuity

### 7. Confirm Sprint Start

Output summary:

```
Sprint N started: [Goal]
- Duration: YYYY-MM-DD → YYYY-MM-DD
- Committed: X points across N stories
- Capacity: Y points (velocity-based)

Stories:
1. STORY-XXX: [Title] (X pts)
2. STORY-XXY: [Title] (Y pts)
3. STORY-XXZ: [Title] (Z pts)

Use `/story-start` to begin the first story.
```

## Guidelines

- **Don't overcommit**: Stay at or below velocity capacity
- **Clear goal**: Sprint goal guides prioritization decisions
- **Ready stories**: Only commit stories with clear acceptance criteria
- **Sustainable pace**: 2-week sprints with realistic capacity
