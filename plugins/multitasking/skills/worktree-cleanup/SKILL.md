---
name: worktree-cleanup
description: "[AGENT-ONLY] Internal skill for safely removing git worktrees and optionally deleting their branches. This skill should NEVER be invoked directly from main context. Only agents (like worktree-agent) should use this skill."
---

# Worktree Cleanup (Agent-Only)

## ⚠️ Usage Restriction

**THIS SKILL IS FOR AGENTS ONLY**

- **DO NOT** invoke this skill directly from main context
- **DO NOT** call this skill when user says "worktree 정리해줘" or similar
- **DO** use the Task tool to launch worktree-agent instead
- **DO** let worktree-agent invoke this skill autonomously

## Overview

Safely remove git worktrees and clean up associated directories with:
- Uncommitted changes validation
- Safe worktree removal
- Directory deletion
- Optional branch deletion
- Comprehensive safety checks

This completes the worktree lifecycle by cleaning up after merged or abandoned features.

## When Agents Should Use This Skill

Agents should use this skill when:
- Operating within worktree-agent context
- User requests cleaning up a worktree
- After successful merge (as a suggestion)
- Worktree is no longer needed

## Workflow

### Step 1: List Available Worktrees

```bash
git worktree list
```

Example output:
```
/Users/jun/Projects/claude-toolkit                 abc1234 [main]
/Users/jun/Projects/claude-toolkit_worktrees/feat1 def5678 [feature-payment]
/Users/jun/Projects/claude-toolkit_worktrees/feat2 ghi9012 [feature-auth]
```

Parse and present to user in friendly format:

```
📋 Available worktrees:

1. main (current directory)
   Path: /Users/jun/Projects/claude-toolkit
   Branch: main

2. feature-payment
   Path: /Users/jun/Projects/claude-toolkit_worktrees/feature-payment
   Branch: feature-payment

3. feature-auth
   Path: /Users/jun/Projects/claude-toolkit_worktrees/feature-auth
   Branch: feature-auth
```

### Step 2: Determine Target Worktree

**Option A: User specifies branch name**
```
User: "worktree 정리해줘 feature-payment"
→ Use 'feature-payment' as target
```

**Option B: Auto-detect if in worktree**
```bash
# Check if current directory is a worktree
pwd | grep "_worktrees/"

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)
```

If in worktree, offer to clean up current one:
```
You're currently in worktree 'feature-payment'.
Would you like to clean up this worktree?
```

**Option C: Ask user to choose**
If neither A nor B applies, show list and ask:
```
Which worktree would you like to clean up?

Available worktrees:
  1. feature-payment
  2. feature-auth

Enter number or branch name:
```

### Step 3: Validate Target Worktree

Ensure we're not trying to delete the main repository:

```bash
git worktree list | grep <target_branch>
```

If target is the main repository path:
```
❌ Error: Cannot remove main repository

You're trying to remove the main repository at:
  /Users/jun/Projects/claude-toolkit

This command only removes worktrees, not the main repository.

Use "worktree list" to see worktrees.
```

### Step 4: Check for Uncommitted Changes

Navigate to the worktree (if not already there):

```bash
cd <worktree_path>
git status --porcelain
```

If uncommitted changes exist:

```
⚠️  Warning: Uncommitted changes detected!

The worktree 'feature-payment' has uncommitted changes:

Modified files:
  M lib/main.dart
  M README.md
?? new_file.txt

Options:
1. Commit changes first:
   cd <worktree_path>
   git add .
   git commit -m "your message"

2. Stash changes:
   cd <worktree_path>
   git stash

3. Force remove (⚠️  WILL LOSE CHANGES):
   Proceed anyway? (yes/no)
```

**STOP HERE** unless user explicitly confirms force removal.

### Step 5: Check Merge Status

Optionally check if branch has been merged:

```bash
# Navigate to main repo first
cd <main_repo_path>

# Check if branch is merged
git branch --merged | grep <feature_branch>
```

If not merged, warn user:

```
⚠️  Warning: Branch not merged

The branch 'feature-payment' has not been merged into main.

Merge status:
  ✗ Not merged into 'main'

You may lose work if you remove this worktree.

Options:
1. Merge first: "worktree 병합해줘"
2. Keep the worktree for now
3. Proceed with removal anyway (if work is no longer needed)

Proceed? (yes/no)
```

### Step 6: Remove Worktree

Navigate to main repository:

```bash
cd <main_repo_path>
```

Remove the worktree:

```bash
git worktree remove <worktree_path>
```

Example:
```bash
git worktree remove ../claude-toolkit_worktrees/feature-payment
```

**Handle errors:**

```bash
# If worktree is locked or has issues
git worktree remove <worktree_path> --force
```

### Step 7: Verify Removal

```bash
git worktree list
```

Confirm the worktree is gone:

```
✓ Worktree removed from git tracking

Remaining worktrees:
  - feature-auth (/Users/jun/Projects/claude-toolkit_worktrees/feature-auth)
```

### Step 8: Clean Up Directory (Optional)

Check if directory still exists:

```bash
ls -d <worktree_path> 2>/dev/null
```

If directory exists:

```
The worktree has been removed from git, but the directory still exists:
  <worktree_path>

Would you like to delete the directory? (yes/no)
```

If user confirms:

```bash
rm -rf <worktree_path>
```

Verify deletion:

```
✓ Directory deleted: <worktree_path>
```

### Step 9: Optionally Delete Branch

Ask user if they want to delete the branch:

```
The worktree has been cleaned up.

Would you like to delete the branch 'feature-payment'?

⚠️  This will permanently delete the branch.

Options:
  1. Safe delete (only if merged): git branch -d feature-payment
  2. Force delete: git branch -D feature-payment
  3. Keep the branch

Your choice?
```

**If user chooses safe delete:**

```bash
git branch -d <feature_branch>
```

If branch is not merged, this will fail safely:
```
error: The branch 'feature-payment' is not fully merged.
If you are sure you want to delete it, run 'git branch -D feature-payment'.
```

**If user chooses force delete:**

```bash
git branch -D <feature_branch>
```

### Step 10: Prune Worktree References

Clean up any stale worktree references:

```bash
git worktree prune
```

This removes references to worktrees that no longer exist.

### Step 11: Final Report

Provide comprehensive summary:

```
✅ Worktree cleanup complete!

Removed:
  ✓ Worktree: feature-payment
  ✓ Directory: /Users/jun/Projects/claude-toolkit_worktrees/feature-payment
  ✓ Branch: feature-payment (deleted)

📊 Current worktree status:
  - Main repository: /Users/jun/Projects/claude-toolkit (branch: main)
  - Active worktrees: 1
    • feature-auth

🎉 All cleaned up! Your repository is organized.
```

## Error Scenarios

### Main Repository Cannot Be Removed

```
❌ Error: Cannot remove main repository

You're attempting to remove the main repository. This is not allowed.

Main repository: /Users/jun/Projects/claude-toolkit

To remove worktrees, specify a worktree path containing "_worktrees".
```

### Worktree Not Found

```
❌ Error: Worktree not found

Branch 'feature-payment' is not an active worktree.

Available worktrees:
  - feature-auth (/Users/jun/Projects/claude-toolkit_worktrees/feature-auth)

Use "worktree list" to see all worktrees.
```

### Uncommitted Changes (User Declined Force)

```
❌ Cleanup cancelled

Worktree 'feature-payment' still has uncommitted changes.

To proceed, either:
1. Commit your changes
2. Stash your changes
3. Confirm force removal (will lose changes)
```

### Locked Worktree

```
⚠️  Warning: Worktree is locked

The worktree may be in use by another process.

Attempting force removal...

✓ Force removal successful

Note: If you were running Claude Code or an IDE in that worktree,
you may need to close it manually.
```

### Branch Deletion Failed

```
⚠️  Warning: Could not delete branch

Worktree removed successfully, but branch deletion failed:

Error: The branch 'feature-payment' is not fully merged.

The branch still exists. You can:
1. Merge it first: "worktree 병합해줘"
2. Force delete: git branch -D feature-payment
3. Keep it for later use
```

## Tips for Agents

1. **Always check** for uncommitted changes before removal
2. **Warn about** unmerged branches to prevent data loss
3. **Confirm destructive actions** especially force removals
4. **Provide clear options** at each decision point
5. **Report comprehensive status** after cleanup
6. **Handle errors gracefully** with recovery suggestions
7. **Auto-detect current worktree** to streamline UX
8. **Suggest merge first** if branch is not merged

## Safety Checklist

Before removing a worktree, verify:

- [ ] No uncommitted changes (or user confirmed force)
- [ ] Not the main repository
- [ ] User confirmed if branch not merged
- [ ] Worktree actually exists in git worktree list
- [ ] User confirmed branch deletion (if applicable)

## References

- Git worktree documentation: https://git-scm.com/docs/git-worktree
- Recovery guide: If worktree removed accidentally, branch still exists and can be checked out
