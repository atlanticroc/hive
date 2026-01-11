# Follow Plan Skill

Skill for executing implementation plans created by Claude.

## Purpose
Translate Claude's plans into working code systematically and accurately.

## Plan Format Recognition

Plans may come in various formats. Recognize and adapt:

### Checklist Format
```markdown
## Implementation Steps
- [ ] Step 1: Create user model
- [ ] Step 2: Add validation
- [ ] Step 3: Create API endpoint
```
**Approach**: Execute sequentially, check off as completed.

### Hierarchical Format
```markdown
## Phase 1: Data Layer
### 1.1 Models
### 1.2 Migrations

## Phase 2: API Layer
### 2.1 Routes
### 2.2 Controllers
```
**Approach**: Complete each phase before moving to next.

### File-Centric Format
```markdown
## Files to Create
- src/models/user.ts
- src/routes/auth.ts
- src/middleware/validate.ts
```
**Approach**: Create files in dependency order.

### Narrative Format
```markdown
First, we need to set up the database models. The User model
should have fields for email, passwordHash, and createdAt...
```
**Approach**: Extract actionable items, then execute.

## Execution Protocol

### Before Starting
```
□ Plan file located and read
□ All steps identified
□ Dependencies understood
□ Execution order determined
□ Blockers identified (if any)
```

### During Execution
```
For each step:
  1. Announce: "Implementing: [step description]"
  2. Execute: Write the code
  3. Verify: Test/lint if possible
  4. Commit: Atomic commit for the step
  5. Update: Mark step complete (mentally)
```

### After Each Step
Quick check:
- Does code compile/parse?
- Does it integrate with previous steps?
- Are there obvious errors?

### After All Steps
```
□ All plan items implemented
□ Final build passes
□ Final tests pass
□ Ready for PR
```

## Handling Plan Ambiguity

### Missing Detail
```
Plan says: "Add authentication"
Need: Specific auth method, token format, etc.

Response:
⚠️ PLAN AMBIGUITY

Step: "Add authentication"
Missing: Authentication method specification

Assumptions I could make:
1. JWT with Bearer tokens (most common)
2. Session-based auth
3. OAuth integration

Proceeding with: [#1 JWT] unless directed otherwise.
```

### Conflicting Instructions
```
Plan says: "Use REST" but also "Use GraphQL"

Response:
⚠️ PLAN CONFLICT

Conflict: REST vs GraphQL specified
Location: [plan sections]

Options:
1. REST only
2. GraphQL only
3. Both (hybrid)

Awaiting clarification.
```

### Impossible Requirement
```
Plan requires feature that doesn't exist

Response:
🚫 PLAN BLOCKED

Step: [step description]
Issue: [why impossible]
Alternatives:
1. [Alternative approach 1]
2. [Alternative approach 2]

Need guidance to proceed.
```

## Deviation Protocol

**Never deviate from plan without signaling.**

If deviation seems necessary:
```
⚠️ PROPOSED DEVIATION

Plan says: [original instruction]
Issue: [why this won't work]
Proposed: [alternative approach]
Impact: [what changes]

Proceeding with deviation: [Yes/No - awaiting approval]
```

Small deviations (implementation details): Proceed and document.
Large deviations (architecture/approach): Stop and ask.

## Progress Tracking

Maintain mental checklist:
```
Plan: auth-implementation.md
Progress: 3/7 steps complete

✓ Step 1: Create User model
✓ Step 2: Add password hashing
✓ Step 3: Create login endpoint
○ Step 4: Create register endpoint  ← CURRENT
○ Step 5: Add JWT middleware
○ Step 6: Protect routes
○ Step 7: Add refresh tokens
```

## Commit Strategy

One commit per logical plan step:
```
feat(auth): implement user login endpoint

Plan step 3/7: Create login endpoint
- POST /api/auth/login
- Validates credentials
- Returns JWT token

Plan: ~/.claude/plans/auth-implementation.md
```

## Completion Signal

When plan is fully executed:
```
## Plan Execution Complete

Plan: [plan file path]
Steps: [X/X] completed
Commits: [N] commits made

### Summary
[Brief description of what was built]

### Files Created/Modified
- [list of files]

### Ready For
- [ ] Copilot CLI to create PR
- [ ] Further testing
- [ ] Code review
```
