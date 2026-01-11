# Project Management Skill

Agile project management for solo developers using lightweight Scrum.

## Activation Triggers

Invoke this skill when the user mentions:
- Sprint planning, starting, or reviewing sprints
- Creating, starting, or completing stories
- Backlog management or prioritization
- Velocity, capacity, or estimation
- Agile, Scrum, or project management

## Available Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/sprint-plan` | Start a new 2-week sprint | Beginning of sprint cycle |
| `/sprint-review` | Close sprint, capture learnings | End of sprint cycle |
| `/story-create` | Add story to backlog | New feature/bug identified |
| `/story-start` | Begin work on a story | Ready to implement |
| `/story-complete` | Mark story done, archive | Acceptance criteria met |

## Workflow

```
/story-create → backlog.md
        ↓
/sprint-plan → current-sprint.md
        ↓
/story-start → current-story.md
        ↓
    [work]
        ↓
/story-complete → archive
        ↓
/sprint-review → velocity.md
```

## Key Files

**Templates** (docs/project/):
- `backlog.md` - Prioritized story queue
- `sprints/current-sprint.md` - Active sprint
- `stories/current-story.md` - Story in progress
- `velocity.md` - Historical tracking

**Archives**:
- `sprints/archive/sprint-N.md` - Completed sprints
- `stories/archive/STORY-XXX.md` - Completed stories

## Configuration

- **Sprint length**: 2 weeks
- **Estimation**: Story points (1, 2, 3, 5, 8)
- **One story at a time**: Complete before starting next
- **Velocity-based planning**: Use average for capacity

## Natural Language Routing

| User Says | Route To |
|-----------|----------|
| "start a sprint", "plan sprint", "new sprint" | `/sprint-plan` |
| "close sprint", "end sprint", "sprint retro" | `/sprint-review` |
| "create story", "add story", "new feature", "new bug" | `/story-create` |
| "start story", "work on story", "begin story" | `/story-start` |
| "done with story", "complete story", "finish story" | `/story-complete` |
| "show backlog", "what's in backlog" | Read `backlog.md` |
| "sprint status", "how's the sprint" | Read `current-sprint.md` |
| "what's my velocity" | Read `velocity.md` |

## Context Integration

This skill follows CLAUDE.md memory hierarchy:

**Pull** (at sprint/story start):
- Load relevant context from docs/ to .context/

**Work** (during implementation):
- Track tasks in .context/todo.md
- Notes in .context/notes.md

**Push** (at completion):
- Archive completed work to docs/
- Update velocity and changelog
- Clean .context/ for next cycle

## Guidelines

- **Don't overcommit**: Stay at or below velocity
- **Small stories**: If > 8 points, suggest splitting
- **Clear acceptance criteria**: Definition of done
- **Sustainable pace**: 2-week cycles with realistic capacity
- **Capture learnings**: Retrospectives improve process
