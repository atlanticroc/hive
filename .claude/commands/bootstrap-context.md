Bootstrap working context by selectively loading from docs/ based on task type.

## Process

### 1. Read INDEX.md First
Read `.context/INDEX.md` for current status:
- Session freshness
- Sprint/story state
- What's already loaded

If INDEX.md shows fresh context from today, skip to step 4.

### 2. Determine Task Type
Ask the user if unclear:
- **Continue**: Picking up previous work
- **Feature**: Implementing new functionality
- **Bug fix**: Fixing an issue
- **Planning**: Sprint/story planning
- **Research**: Exploring/understanding codebase

### 3. Load Based on Task Type

| Task Type | Files to Load |
|-----------|---------------|
| Continue | handoff.md, todo.md |
| Feature | current-story.md, architecture.md (if needed) |
| Bug fix | todo.md, relevant source files |
| Planning | backlog.md, velocity.md, current-sprint.md |
| Research | None (just answer questions) |

**Selective loading rules:**
- Only load files listed for task type
- Read architecture.md only if task involves architectural decisions
- Read product.md only if task involves product direction

### 4. Summarize to notes.md
Write to `.context/notes.md` (max 50 lines):

```markdown
# Session Notes - [Date]

## Task: [type] - [brief description]

## Key Context
- [3-5 bullet points from loaded docs]

## Constraints
- [relevant architectural constraints]

## Files to Reference
- [file:line]: [why relevant]
```

### 5. Update todo.md
Add tasks from handoff "Next Steps" if continuing:
- Mark first task as in_progress
- Keep todo.md under 30 lines

### 6. Provide Bootstrap Summary
Tell the user:
- What was loaded
- Current task focus
- First 1-3 actions to take

## Task-Specific Loading Details

### Continue Previous Work
```
Read: handoff.md, todo.md
Skip: All docs/ files (already summarized)
Output: "Continuing [task]. Next: [action]"
```

### New Feature
```
Read: current-story.md (if exists)
Read: architecture.md (if architectural impact)
Skip: product.md, roadmap.md, adr.md (unless needed)
Output: Story summary, acceptance criteria, first step
```

### Bug Fix
```
Read: todo.md (for context on issue)
Read: Relevant source files
Skip: All docs/ files
Output: Bug description, suspected location, first step
```

### Sprint/Story Planning
```
Read: backlog.md, velocity.md
Read: current-sprint.md
Skip: Product docs (unless prioritizing)
Output: Available capacity, top stories, recommended commitment
```

## Guidelines

**DO:**
- Read INDEX.md first
- Ask task type if unclear
- Load only what's needed
- Keep notes.md under 50 lines

**DON'T:**
- Load entire docs/ directory
- Copy full documents into notes.md
- Re-read files already summarized
- Skip INDEX.md check
