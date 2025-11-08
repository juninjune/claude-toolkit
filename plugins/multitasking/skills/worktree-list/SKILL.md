---
name: worktree-list
description: "Display all git worktrees in a friendly, formatted table. This skill can be invoked directly or by agents."
---

# Worktree List

## Overview

Display all active git worktrees for the current repository in a clear, formatted view. This skill shows:
- Main repository location and branch
- All active worktrees with their paths and branches
- Current worktree indicator (if applicable)
- Commit information for each worktree

Unlike other worktree skills, this is **NOT agent-only** and can be invoked directly.

## When to Use This Skill

Use this skill when:
- You want to see all active worktrees
- You need to check which worktrees exist before creating a new one
- You want to verify a worktree was created successfully
- You're deciding which worktree to merge or clean up

## Workflow

### Step 1: Validate Git Repository

```bash
git rev-parse --is-inside-work-tree
```

If not in a git repository:
```
❌ Error: Not a git repository

This command must be run from within a git repository.
```

### Step 2: Get Worktree List

```bash
git worktree list
```

Example output:
```
/Users/jun/Projects/claude-toolkit                        abc1234 [main]
/Users/jun/Projects/claude-toolkit_worktrees/feature-pay  def5678 [feature-payment]
/Users/jun/Projects/claude-toolkit_worktrees/feature-auth ghi9012 [feature-auth]
```

### Step 3: Get Current Location

```bash
pwd
git branch --show-current
```

This helps identify which worktree the user is currently in.

### Step 4: Format and Display

Parse the git worktree list and present in a friendly format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📂 Git Worktrees for 'claude-toolkit'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏠 Main Repository
   Path: /Users/jun/Projects/claude-toolkit
   Branch: main
   Commit: abc1234

📦 Active Worktrees (2)

1️⃣  feature-payment  👈 (you are here)
   Path: /Users/jun/Projects/claude-toolkit_worktrees/feature-payment
   Branch: feature-payment
   Commit: def5678
   Status: ✓ Clean

2️⃣  feature-auth
   Path: /Users/jun/Projects/claude-toolkit_worktrees/feature-auth
   Branch: feature-auth
   Commit: ghi9012
   Status: ⚠️  Uncommitted changes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Quick actions:
   • Create new: "worktree 만들어줘 <branch-name>"
   • Merge: "worktree 병합해줘"
   • Cleanup: "worktree 정리해줘 <branch-name>"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 5: Add Status Information (Optional Enhancement)

For each worktree, you can check status:

```bash
cd <worktree_path>
git status --porcelain
```

If output is empty: Status = "✓ Clean"
If output exists: Status = "⚠️ Uncommitted changes"

### Alternative: Simple Table Format

For a more compact view:

```
Worktree List (3 total)
────────────────────────────────────────────────────────────────────
Branch              Location                                  Status
────────────────────────────────────────────────────────────────────
main                ~/Projects/claude-toolkit                 ✓
feature-payment     ~/Projects/claude-toolkit_worktrees/...   ✓ 👈
feature-auth        ~/Projects/claude-toolkit_worktrees/...   ⚠️
────────────────────────────────────────────────────────────────────

Legend:
  ✓ = Clean (no uncommitted changes)
  ⚠️ = Uncommitted changes present
  👈 = Current location
```

## Error Scenarios

### Not a Git Repository

```
❌ Error: Not a git repository

Current directory: /Users/jun/Documents

Navigate to a git repository first:
  cd /path/to/your/repository
```

### No Worktrees

```
📂 Git Worktrees for 'claude-toolkit'

🏠 Main Repository
   Path: /Users/jun/Projects/claude-toolkit
   Branch: main

📦 Active Worktrees: None

💡 Create your first worktree:
   "worktree 만들어줘 <branch-name>"
```

### Git Command Failed

```
❌ Error: Could not retrieve worktree list

Git error: <error message>

This might happen if:
- Repository is corrupted
- Git version is too old (requires Git 2.5+)
- Filesystem permissions issue

Try:
  git worktree list
```

## Implementation Notes

### Parsing Git Worktree List

The output format is:
```
<path>  <commit-hash> [<branch>]
```

Example parsing logic:
1. Split by newlines
2. For each line:
   - First field: worktree path
   - Second field: commit hash
   - Third field (in brackets): branch name

### Determining Current Location

Compare `pwd` output with each worktree path to identify current location.

### Status Checking

Optional but useful:
- For each worktree, `cd` into it
- Run `git status --porcelain`
- Empty output = clean
- Any output = has changes

### Path Abbreviation

For readability, abbreviate long paths:
- Use `~` for home directory
- Show `...` for middle of long paths
- Keep filename visible

Example:
```
Before: /Users/jun/Projects/claude-toolkit_worktrees/feature-payment
After:  ~/Projects/claude-toolkit_worktrees/feature-payment

Or even shorter:
../claude-toolkit_worktrees/feature-payment
```

## Usage Examples

### Example 1: Check before creating

```
User: "worktree list"

[Displays list showing feature-payment and feature-auth]

User: "worktree 만들어줘 feature-checkout"
[Creates new worktree without conflicts]
```

### Example 2: Identify current location

```
User: "worktree list"

[Shows you're in feature-payment worktree]

User: "worktree 병합해줘"
[Knows to merge feature-payment]
```

### Example 3: Find uncommitted changes

```
User: "worktree list"

[Shows feature-auth has uncommitted changes]

User: "Looks like I need to commit feature-auth first"
```

## Tips for Implementation

1. **Cache git worktree list output**: Run once, parse multiple times
2. **Use color coding**: Green for clean, yellow for changes
3. **Show relative paths** when possible for brevity
4. **Highlight current location** to help user orientation
5. **Include quick actions** to guide next steps
6. **Handle edge cases**: locked worktrees, missing directories, etc.

## Integration with Other Skills

This skill is often used in conjunction with:
- **worktree-create**: Check before creating to avoid name conflicts
- **worktree-merge**: Identify which worktrees are ready to merge
- **worktree-cleanup**: Select which worktrees to clean up

The agent can automatically call this skill to gather context before executing other worktree operations.
