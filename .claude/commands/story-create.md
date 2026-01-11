# /story-create

Create a new user story and add it to the product backlog.

## Process

### 1. Gather Story Information

Ask the user for story details using AskUserQuestion:

**Required:**
- **Title**: Short, descriptive name (e.g., "Add user authentication")
- **User Story**: "As a [user], I want [goal], so that [benefit]"
- **Acceptance Criteria**: Testable conditions for "done" (2-5 criteria)

**Optional (ask if not provided):**
- **Priority**: 1 (Next Sprint), 2 (Soon), 3 (Later), or Icebox
- **Points**: Story points 1, 2, 3, 5, or 8 (use Planning Poker scale)
- **Labels**: feature, bug, tech-debt, or research

### 2. Generate Story ID

Read `docs/project/backlog.md` to find the highest existing STORY-XXX number.
Increment by 1 for the new story ID.

If no stories exist, start with STORY-001.

### 3. Format the Story

Use this exact format:

```markdown
### STORY-XXX: [Title]
**Points**: X | **Created**: YYYY-MM-DD
**Labels**: [label]

As a [user type],
I want [goal],
So that [benefit].

**Acceptance Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
```

### 4. Add to Backlog

Insert the formatted story into `docs/project/backlog.md` under the appropriate priority section:
- Priority 1 → "## Priority 1 - Next Sprint"
- Priority 2 → "## Priority 2 - Soon"
- Priority 3 → "## Priority 3 - Later"
- Icebox → "## Icebox"

Add new stories at the END of their priority section (newest last within priority).

Update the "Last updated" line at the bottom with today's date.

### 5. Confirm Creation

Output a summary:

```
Created STORY-XXX: [Title]
- Points: X
- Priority: X
- Added to: docs/project/backlog.md

Use `/sprint-plan` to include this story in a sprint.
```

## Guidelines

- **Keep stories small**: If points > 8, suggest breaking into smaller stories
- **Clear acceptance criteria**: Each criterion should be independently testable
- **User-focused**: Stories describe user value, not implementation details
- **INVEST criteria**: Independent, Negotiable, Valuable, Estimable, Small, Testable

## Examples

**Good story:**
```
### STORY-012: Display 24-hour forecast
**Points**: 3 | **Created**: 2026-01-11
**Labels**: feature

As a passenger,
I want to see a 24-hour disruption forecast,
So that I can plan my travel timing.

**Acceptance Criteria**:
- [ ] Forecast displays hourly disruption probability
- [ ] Visual timeline shows next 24 hours
- [ ] Updates automatically every 30 minutes
```

**Too large (suggest splitting):**
```
"Implement full authentication system" (13+ points)
→ Split into: "User registration", "Login/logout", "Password reset"
```
