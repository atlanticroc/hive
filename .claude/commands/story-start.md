# /story-start

Pull a story from the current sprint into active work.

## Prerequisites

- An active sprint must exist in `docs/project/sprints/current-sprint.md`
- The sprint must have uncommitted stories (status: "Not Started")

If no sprint exists, prompt user to run `/sprint-plan` first.

## Process

### 1. Check Current State

Read `docs/project/stories/current-story.md`:
- If a story is already in progress, ask user to complete it first with `/story-complete`
- If empty/placeholder, proceed

Read `docs/project/sprints/current-sprint.md`:
- Get list of stories with status "Not Started"
- If no stories available, inform user sprint backlog is empty

### 2. Select Story

If multiple stories are available, use AskUserQuestion to let user choose which story to start.

Present stories with their ID, title, and points.

If only one story, confirm with user before starting.

### 3. Get Story Details from Backlog

Read the full story details from `docs/project/backlog.md` using the story ID.

Extract:
- Title
- Points
- Labels
- User story text
- Acceptance criteria

### 4. Create Active Story File

Write to `docs/project/stories/current-story.md`:

```markdown
# STORY-XXX: [Title]

**Points**: X | **Sprint**: N | **Status**: In Progress
**Started**: YYYY-MM-DD
**Labels**: [labels]

## User Story

As a [user type],
I want [goal],
So that [benefit].

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Tasks

<!-- Break down into implementation tasks -->
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## Notes

<!-- Implementation notes, decisions, blockers -->

---
Use `/story-complete` when all acceptance criteria are met.
```

### 5. Update Sprint Status

Edit `docs/project/sprints/current-sprint.md`:
- Change the story's status from "Not Started" to "In Progress"

### 6. Update Working Context

Update `.context/todo.md`:
- Add tasks from the story's acceptance criteria
- Mark as the current focus

Update `.context/notes.md`:
- Add "## Current Story: STORY-XXX" section
- Include key acceptance criteria for quick reference

### 7. Confirm Start

Output summary:

```
Started STORY-XXX: [Title]
- Points: X
- Sprint: N
- Acceptance Criteria: X items

Tasks added to .context/todo.md

Focus on completing acceptance criteria. Use `/story-complete` when done.
```

## Guidelines

- **One story at a time**: Finish current story before starting another
- **Break into tasks**: Help user decompose story into concrete implementation tasks
- **Update context**: Ensure .context/ files reflect current focus
- **Flow**: story-start → implement → story-complete
