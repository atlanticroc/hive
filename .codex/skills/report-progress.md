# Report Progress Skill

Skill for signaling task status to other agents in the ecosystem.

## Purpose
Communicate implementation progress so:
- Claude knows what's done for next planning
- Copilot CLI knows what to include in PRs
- Humans can track overall progress

## Progress Signals

### Starting Work
```
🚀 STARTING IMPLEMENTATION

Task: [task description]
Plan: [plan file reference]
Scope: [N] steps to implement

Starting at: [timestamp]
```

### Step Complete
```
✓ STEP COMPLETE

Step: [step description]
Files: [files created/modified]
Commit: [commit message summary]

Progress: [X/N] steps complete
```

### Blocked
```
🚫 BLOCKED

Step: [step attempting]
Blocker: [what's preventing progress]
Need: [what would unblock]

Waiting for: [Claude/User/External]
```

### Clarification Needed
```
❓ CLARIFICATION NEEDED

Step: [step description]
Question: [specific question]
Options: [if applicable]

Paused until clarified.
```

### Work Complete
```
✅ IMPLEMENTATION COMPLETE

Task: [task description]
Plan: [plan file reference]
Duration: [time taken]

Commits: [N]
Files changed: [N]

Summary:
[2-3 sentences on what was built]

Ready for: PR creation by Copilot CLI
```

## Reporting Channels

### Via Commits
Every commit is a progress signal:
```
feat(module): implement feature X

Plan step [N/M]: [step description]
[details]

Status: [X/M] complete
```

### Via Console Output
During interactive sessions, print progress:
```
[2/7] Implementing user validation...
[3/7] Creating API endpoint...
[4/7] ✓ Tests passing
```

### Via Handoff (End of Session)
If session ends mid-task, leave breadcrumbs:

**DO NOT MODIFY `.context/handoff.md`** (Claude's domain)

Instead, make a descriptive final commit:
```
wip(auth): partial implementation - 4/7 steps complete

Completed:
- User model
- Password hashing
- Login endpoint
- Register endpoint

Remaining:
- JWT middleware
- Protected routes
- Refresh tokens

Next Codex session should continue from step 5.
```

## Status Templates

### For Simple Tasks
```
✅ DONE: [task] - [one line summary]
```

### For Multi-Step Tasks
```
📊 PROGRESS: [task]
━━━━━━━━━━━━━━━━━━━━
[████████░░] 80% (8/10 steps)

Recent:
✓ Step 7: Added error handling
✓ Step 8: Created unit tests

Next:
○ Step 9: Integration tests
○ Step 10: Documentation
```

### For Blocked Tasks
```
🚫 BLOCKED: [task]
━━━━━━━━━━━━━━━━━━━━
Completed: 5/10 steps
Blocked at: Step 6

Issue: [description]
Needs: [what's required to unblock]
```

## Integration with Multi-Agent Flow

### What Claude Needs to Know
- Which plan steps are complete
- Any deviations from plan
- Blockers requiring re-planning
- Quality/test status

### What Copilot CLI Needs to Know
- Summary for PR description
- List of changes for PR body
- Any special review notes

### Signal Handoff Points
```
Codex → Copilot CLI:
"Implementation complete. [N] commits ready. 
Summary: [what was built]
PR should mention: [key points]"

Codex → Claude:
"Completed plan [X]. Encountered [issues].
Suggest next: [follow-up work]"
```

## Error Reporting

### Build/Test Failures
```
❌ BUILD FAILED

Command: npm run build
Error: [error message]
File: [file with issue]

Attempting fix...
```

### Unrecoverable Errors
```
💥 UNRECOVERABLE ERROR

Task: [task]
Error: [error description]
Attempted: [what was tried]

Need: [human/Claude intervention]
```

## Quality Checklist
- [ ] Progress visible in commits
- [ ] Blockers clearly communicated
- [ ] Completion clearly signaled
- [ ] Handoff info available for next agent
