# Read Context Skill

Skill for bootstrapping session context from the `.context/` directory.

## Purpose
Load relevant context at the start of any Codex session to understand:
- What task is currently active
- What decisions have been made
- What the implementation plan is

## Execution Steps

### Step 1: Read Handoff
```
File: .context/handoff.md
Extract:
- Current task description
- Key decisions already made
- Referenced plan file path
- Any blockers or gotchas
- Files to be aware of
```

### Step 2: Read Todo
```
File: .context/todo.md
Extract:
- Uncompleted tasks ([ ] items)
- Task priority/order
- Acceptance criteria
- Dependencies between tasks
```

### Step 3: Read Plan (if referenced)
```
File: [path from handoff.md]
Extract:
- Implementation steps
- File structure
- Technical approach
- Integration points
```

### Step 4: Scan Changelog (optional)
```
File: .context/changelog.md
Extract:
- Recent decisions (last 5-10 entries)
- Rationale for key choices
- Any constraints to follow
```

## Output: Context Summary

After reading, synthesize into working context:

```
## Active Task
[1-2 sentence description]

## Implementation Plan
Source: [plan file path]
Steps remaining: [count]

## Key Decisions
- [Decision 1]: [rationale]
- [Decision 2]: [rationale]

## Files to Create/Modify
- [ ] path/to/file1.ts - [purpose]
- [ ] path/to/file2.ts - [purpose]

## Constraints
- [Constraint 1]
- [Constraint 2]

## Ready to Implement
[Yes/No - if No, state what's missing]
```

## When Context is Incomplete

If essential information is missing:

```
⚠️ CONTEXT INCOMPLETE

Missing:
- [ ] Plan file not found: [path]
- [ ] Todo has no uncompleted items
- [ ] Handoff is empty/stale

Options:
1. Wait for Claude to update context
2. Ask user for clarification
3. Proceed with available context (risky)

Recommendation: [option]
```

## Context Freshness Check

Verify context is current:
- Handoff date within last 7 days
- Todo has actionable items
- Plan file exists and is readable

If stale:
```
⚠️ CONTEXT MAY BE STALE

Handoff last updated: [date]
Recommend: Request fresh context from Claude
```

## Usage

Call this skill at the start of every session:
```
> Using skill: read-context
> Reading .context/handoff.md...
> Reading .context/todo.md...
> Reading plan file...
> Context loaded. Ready to implement.
```
