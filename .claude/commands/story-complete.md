# /story-complete

Mark the current story as done, archive it, and update sprint progress.

## Prerequisites

- An active story must exist in `docs/project/stories/current-story.md`
- All acceptance criteria should be met (or user confirms partial completion)

## Process

### 1. Verify Completion

Read `docs/project/stories/current-story.md`:
- Check all acceptance criteria checkboxes
- If any unchecked, ask user to confirm:
  - Complete remaining criteria?
  - Mark done anyway (with note)?
  - Cancel and continue working?

### 2. Capture Completion Details

Ask user (optional, can skip):
- Any notes or learnings to record?
- Actual effort vs estimate? (for velocity calibration)

### 3. Archive the Story

Create archive file at `docs/project/stories/archive/STORY-XXX.md`:

```markdown
# STORY-XXX: [Title] (Completed)

**Points**: X | **Sprint**: N | **Status**: Done
**Started**: YYYY-MM-DD | **Completed**: YYYY-MM-DD
**Labels**: [labels]

## User Story

As a [user type],
I want [goal],
So that [benefit].

## Acceptance Criteria

- [x] Criterion 1
- [x] Criterion 2
- [x] Criterion 3

## Completion Notes

[Any notes captured from user]

## Tasks Completed

- [x] Task 1
- [x] Task 2
```

### 4. Update Sprint Progress

Edit `docs/project/sprints/current-sprint.md`:
- Change story status from "In Progress" to "Done"
- Update progress calculation (completed points / total points)

### 5. Remove from Backlog

Edit `docs/project/backlog.md`:
- Remove the completed story entry
- Update "Last updated" date

### 6. Reset Current Story

Write placeholder to `docs/project/stories/current-story.md`:

```markdown
# Current Story

> No story in progress. Use `/story-start` to pull a story from the sprint backlog.
```

### 7. Clean Up Context

Update `.context/todo.md`:
- Remove or mark complete the story's tasks
- Add note: "STORY-XXX completed"

Update `.context/notes.md`:
- Remove "Current Story" section
- Optionally note completion

### 8. Suggest Next Action

Check sprint for remaining stories:
- If stories remain: "Use `/story-start` to begin next story"
- If sprint complete: "Sprint backlog complete! Use `/sprint-review` to close sprint"

Output summary:

```
Completed STORY-XXX: [Title]
- Points: X
- Sprint: N
- Archived to: docs/project/stories/archive/STORY-XXX.md

Sprint Progress: X/Y points (Z%)

[Next action suggestion]
```

## Guidelines

- **Verify completion**: Acceptance criteria are the definition of done
- **Capture learnings**: Notes help improve future estimates
- **Clean context**: Reset .context/ files for next story
- **Maintain flow**: Guide user to next story or sprint review
