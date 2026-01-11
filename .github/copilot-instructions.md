# GitHub Copilot Instructions

This file provides guidance to GitHub Copilot (CLI and PR Review) when working in this repository.

## Role in Multi-Agent System

This repository uses a **three-CLI strategy** with distinct responsibilities:

| Agent | Primary Role | Reads From | Writes To |
|-------|--------------|------------|-----------|
| **Claude Code** | Planning, architecture, complex decisions | `docs/`, `.context/` | `.context/`, `docs/`, plans |
| **Codex** | Code execution, implementation | `.context/`, plans | `src/`, code files |
| **Copilot CLI** | GitHub operations, PRs, commits | `.context/` | PRs, commits, branches |
| **Copilot PR Review** | Code review feedback | `AGENTS.md`, code | Review comments |

## Copilot CLI Responsibilities

### DO
- Write clear, descriptive PR titles and descriptions
- Generate commit messages following conventional commits format
- Manage branches following the naming conventions
- Reference `.context/changelog.md` for recent decisions when writing PRs
- Reference `.context/handoff.md` for current task context
- Create atomic, focused commits

### DO NOT
- Make architectural decisions (defer to Claude)
- Implement complex features without a plan (defer to Codex with Claude's plan)
- Modify `.context/` files (that's Claude's domain)
- Modify `docs/` files (that's Claude's domain)

## Conventions

### Branch Naming
```
<type>/<short-description>
```
Types: `feature/`, `fix/`, `refactor/`, `docs/`, `chore/`

### Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/):
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```
Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### PR Descriptions
Structure PR descriptions as:
1. **Summary**: What this PR does (1-2 sentences)
2. **Changes**: Bullet list of key changes
3. **Context**: Reference to `.context/changelog.md` entries or story
4. **Testing**: How to verify the changes

## Copilot PR Review Guidelines

When reviewing PRs in this repository:

### Focus Areas
- Code correctness and potential bugs
- Adherence to existing patterns in the codebase
- Test coverage for new functionality
- Security considerations

### Context Awareness
- Check if changes align with patterns documented in `AGENTS.md`
- Verify changes don't violate the memory hierarchy (`.context/` vs `docs/`)
- Ensure AI-generated code follows repository conventions

### Review Style
- Be constructive and specific
- Suggest improvements, don't just point out problems
- Reference documentation when relevant
- Approve when changes meet quality standards

## Source of Truth

Refer to these files for authoritative information:
- **`AGENTS.md`**: Cross-agent instructions and context management
- **`.context/handoff.md`**: Current task context
- **`.context/changelog.md`**: Recent decisions and changes
- **`docs/`**: Long-term project documentation
