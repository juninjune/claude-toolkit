---
name: worktree-merge
description: "[AGENT-ONLY] Internal skill for merging worktree branches back to main branch with conflict detection and resolution guidance. This skill should NEVER be invoked directly from main context. Only agents (like worktree-agent) should use this skill."
---

# Worktree Merge (Agent-Only)

## ⚠️ Usage Restriction

**THIS SKILL IS FOR AGENTS ONLY**

- **DO NOT** invoke this skill directly from main context
- **DO NOT** call this skill when user says "worktree 병합해줘" or similar
- **DO** use the Task tool to launch worktree-agent instead
- **DO** let worktree-agent invoke this skill autonomously

## Overview

Merge a worktree branch back into the main branch with:
- Automatic main branch detection (main/master/dev)
- Uncommitted changes validation
- Merge conflict detection
- Detailed conflict resolution guidance
- Post-merge cleanup suggestions

This completes the parallel development workflow by safely integrating changes from isolated worktrees.

## When Agents Should Use This Skill

Agents should use this skill when:
- Operating within worktree-agent context
- User requests merging a worktree
- Currently in a worktree directory (not main repo)
- All changes are committed

## Workflow

### Step 1: Validate Current Location

Verify we're in a worktree (not the main repository):

```bash
# Get current branch
CURRENT_BRANCH=$(git branch --show-current)

# Get repository root
REPO_ROOT=$(git rev-parse --show-toplevel)

# Get repository name
REPO_NAME=$(basename "$REPO_ROOT")

# Check if we're in a worktree by checking path
pwd | grep "_worktrees/"
```

If not in a worktree, report error:
```
❌ Error: Not in a worktree

Current location: /Users/jun/Projects/claude-toolkit
Current branch: main

This command should be run from within a worktree directory.
To see available worktrees: "worktree list"
```

### Step 2: Check for Uncommitted Changes

```bash
git status --porcelain
```

If there are uncommitted changes, report error:
```
❌ Error: You have uncommitted changes

Please commit or stash your changes before merging:

Modified files:
  M lib/main.dart
  M README.md
?? new_file.txt

To commit:
  git add .
  git commit -m "your message"

Or to stash:
  git stash
```

**STOP HERE** - user must commit first.

### Step 3: Detect Main Branch

Try to detect the main branch in order of preference:

```bash
# Check if 'main' exists
git show-ref --verify --quiet refs/heads/main && echo "main"

# Check if 'master' exists
git show-ref --verify --quiet refs/heads/master && echo "master"

# Check if 'dev' or 'develop' exists
git show-ref --verify --quiet refs/heads/dev && echo "dev"
git show-ref --verify --quiet refs/heads/develop && echo "develop"
```

If none found, ask user to specify:
```
❓ Which branch should I merge into?

Common options:
- main
- master
- develop

Please specify the target branch name.
```

### Step 4: Navigate to Main Repository

Calculate main repository path:

```bash
# Current: /Users/jun/Projects/claude-toolkit_worktrees/feature-payment
# Main repo: /Users/jun/Projects/claude-toolkit

# Get parent directory of worktrees folder
MAIN_REPO=$(dirname $(dirname "$REPO_ROOT"))/${REPO_NAME}
```

Navigate to main repo:

```bash
cd "$MAIN_REPO"
```

Verify we're in the right place:

```bash
git branch --show-current  # Should show main/master/dev
pwd  # Should NOT contain "_worktrees"
```

### Step 5: Checkout Main Branch

```bash
git checkout <main_branch>
```

Example:
```bash
git checkout main
```

### Step 6: Attempt Merge

```bash
git merge <feature_branch> --no-ff
```

Example:
```bash
git merge feature-payment --no-ff
```

The `--no-ff` flag ensures a merge commit is created even for fast-forward merges, preserving the feature branch history.

### Step 7a: Merge Success ✅

If merge succeeds without conflicts:

```
✅ Merge successful!

Branch 'feature-payment' has been merged into 'main'.

Merge commit: abc1234
Files changed: 15 files, 234 insertions(+), 67 deletions(-)

📊 Summary:
  - New files: 3
  - Modified files: 12
  - Deletions: 0

🎉 Your changes are now in the main branch!

Next steps:
1. Review the merge with: git log --oneline -5
2. Run tests to ensure everything works
3. Push to remote: git push origin main
4. Clean up worktree: "worktree 정리해줘"
```

**Offer cleanup**: Ask if user wants to run worktree-cleanup skill now.

### Step 7b: Merge Conflicts ⚠️

If merge fails due to conflicts:

```bash
# Check for conflicts
git diff --name-only --diff-filter=U
```

Report conflict status:

```
⚠️ Merge conflict detected!

Branch 'feature-payment' has conflicts with 'main'.

📋 Conflicted files:
  - lib/screens/home_screen.dart
  - lib/models/payment.dart
  - README.md

🔧 Conflict markers to look for:
  <<<<<<< HEAD (current main branch changes)
  =======  (separator)
  >>>>>>> feature-payment (your worktree changes)
```

### Step 8: Load and Display Merge Guide

Read the comprehensive merge guide:

```
Read: plugins/universal/skills/worktree-merge/references/merge_guide.md
```

**Note for agents**: Use the full path when invoking from agent context.

Display the guide content to help user resolve conflicts.

### Step 9: Open IDE for Conflict Resolution

```bash
# Detect and open IDE in main repository
bash plugins/universal/skills/worktree-create/scripts/detect_ide.sh \
  <main_repo_path> \
  cursor
```

**Note for agents**: Reuse the detect_ide.sh script from worktree-create skill.

### Step 10: Provide Resolution Instructions

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 How to resolve conflicts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I've opened the main repository in Cursor/VS Code.

**Steps to resolve:**

1. Open each conflicted file
2. Look for conflict markers (<<<<<<, =======, >>>>>>>)
3. Use your IDE's conflict resolution tools:
   • Accept Current Change (keep main)
   • Accept Incoming Change (keep feature)
   • Accept Both Changes
   • Edit Manually

4. Save all files

5. Stage resolved files:
   git add <file1> <file2> ...

6. Complete the merge:
   git commit

7. Verify the merge:
   git log --oneline -3

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After resolving conflicts, run:
  "worktree 정리해줘"

This will clean up the worktree since the merge is complete.

Need help? Ask me to explain any specific conflict!
```

**IMPORTANT**: Do NOT proceed with cleanup until user confirms conflicts are resolved.

## Error Scenarios

### Not in a Worktree
```
❌ Error: Not in a worktree directory

Current location: /Users/jun/Projects/claude-toolkit
Current branch: main

You're in the main repository, not a worktree.

To merge a worktree:
1. Navigate to the worktree directory
2. Or specify which worktree to merge

Available worktrees:
  feature-payment  (/Users/jun/Projects/claude-toolkit_worktrees/feature-payment)
  feature-auth     (/Users/jun/Projects/claude-toolkit_worktrees/feature-auth)
```

### Uncommitted Changes
```
❌ Error: Uncommitted changes detected

You must commit your changes before merging.

Uncommitted files:
  M lib/main.dart
  M README.md

Please run:
  git add .
  git commit -m "Your commit message"

Then try merging again.
```

### Main Branch Not Found
```
❌ Error: Could not detect main branch

Searched for: main, master, dev, develop
Found branches: feature-payment, experimental

Please tell me which branch to merge into.
```

### Main Repository Not Found
```
❌ Error: Could not locate main repository

Expected location: /Users/jun/Projects/claude-toolkit
Worktree location: /Users/jun/Projects/claude-toolkit_worktrees/feature-payment

The main repository might have been moved or deleted.
Please check the repository location.
```

## Tips for Agents

1. **Always check** for uncommitted changes before attempting merge
2. **Detect main branch** automatically but ask if detection fails
3. **Use full paths** when calling scripts from agent context
4. **Display full merge guide** when conflicts occur
5. **Open IDE** automatically to help with conflict resolution
6. **Suggest cleanup** after successful merge
7. **Do NOT auto-cleanup** if conflicts exist - wait for user confirmation

## References

- Merge conflict guide: `plugins/universal/skills/worktree-merge/references/merge_guide.md`
- Conflict examples: `plugins/universal/skills/worktree-merge/references/conflict_examples.md`
- IDE detection script: `plugins/universal/skills/worktree-create/scripts/detect_ide.sh` (reused)
