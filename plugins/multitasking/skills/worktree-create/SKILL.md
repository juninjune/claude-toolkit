---
name: worktree-create
description: "[AGENT-ONLY] Internal skill for creating git worktrees with automated file copying and IDE integration. This skill should NEVER be invoked directly from main context. Only agents (like worktree-agent) should use this skill."
---

# Worktree Create (Agent-Only)

## ⚠️ Usage Restriction

**THIS SKILL IS FOR AGENTS ONLY**

- **DO NOT** invoke this skill directly from main context
- **DO NOT** call this skill when user says "worktree 만들어줘" or similar
- **DO** use the Task tool to launch worktree-agent instead
- **DO** let worktree-agent invoke this skill autonomously

## Overview

Create a new git worktree with automated setup including:
- Branch creation in isolated directory
- Copying gitignored files (.env, .claude/, .cursor/)
- Automatic IDE launching (cursor or VS Code)
- Project-specific configuration support

This enables parallel development workflows where multiple Claude Code sessions can work on different features simultaneously without conflicts.

## When Agents Should Use This Skill

Agents should use this skill when:
- Operating within worktree-agent context
- User requests creating a new worktree
- Branch name has been confirmed
- Working directory is a valid git repository

## Workflow

### Step 1: Validate Git Repository

Ensure we're in a git repository:

```bash
git rev-parse --is-inside-work-tree
```

If not a git repo, report error and exit.

### Step 2: Load Configuration

Check for project-specific configuration:

```bash
Read: .claude/worktree-config.json
```

If file exists, use those settings. Otherwise, use defaults:

```json
{
  "worktreeDir": "../{repo}_worktrees",
  "copyFiles": [
    ".env",
    ".env.local",
    ".claude/",
    ".cursor/",
    ".vscode/"
  ],
  "ide": "cursor",
  "autoOpen": true,
  "mainBranch": "main"
}
```

**Configuration explanation:**
- `worktreeDir`: Template for worktree parent directory. `{repo}` is replaced with current repo name
- `copyFiles`: List of files/directories to copy (typically gitignored files)
- `ide`: Preferred IDE ("cursor" or "code")
- `autoOpen`: Whether to automatically open IDE after creation
- `mainBranch`: Default main branch name (main/master/dev)

**For agents**: If config doesn't exist, you can offer to create one with defaults.

### Step 3: Get Repository Information

```bash
# Get current directory name (repository name)
basename $(pwd)

# Get current branch (as parent branch)
git branch --show-current

# List existing worktrees to check for conflicts
git worktree list
```

### Step 4: Determine Worktree Path

Based on configuration and branch name:

1. Replace `{repo}` in `worktreeDir` template with repository name
2. Append branch name to create full path
3. Check if path already exists

Example:
- Repository: `claude-toolkit`
- Branch: `feature-payment`
- Template: `../{repo}_worktrees`
- Result: `../claude-toolkit_worktrees/feature-payment`

### Step 5: Create Worktree Parent Directory

```bash
mkdir -p <worktree_parent_dir>
```

Example: `mkdir -p ../claude-toolkit_worktrees`

### Step 6: Create Git Worktree

```bash
git worktree add <full_worktree_path> -b <branch_name>
```

Example:
```bash
git worktree add ../claude-toolkit_worktrees/feature-payment -b feature-payment
```

**Error handling:**
- If branch already exists: Report error with existing branch info
- If worktree path already exists: Report error and suggest cleanup
- If git command fails: Report git error message

### Step 7: Copy Gitignored Files

Execute the copy script with configured files:

```bash
bash plugins/universal/skills/worktree-create/scripts/copy_ignored_files.sh \
  <source_dir> \
  <target_dir> \
  <file1> <file2> ...
```

Example:
```bash
bash plugins/universal/skills/worktree-create/scripts/copy_ignored_files.sh \
  . \
  ../claude-toolkit_worktrees/feature-payment \
  .env .env.local .claude/ .cursor/ .vscode/
```

**Note for agents**: Use the full path `plugins/universal/skills/worktree-create/scripts/copy_ignored_files.sh` when invoking this skill from an agent context.

The script will:
- Check each file/directory existence
- Copy with proper permissions
- Report success/skip status
- Handle errors gracefully

### Step 8: Open IDE (if configured)

If `autoOpen` is true in configuration:

```bash
bash plugins/universal/skills/worktree-create/scripts/detect_ide.sh \
  <worktree_path> \
  <ide_preference>
```

Example:
```bash
bash plugins/universal/skills/worktree-create/scripts/detect_ide.sh \
  ../claude-toolkit_worktrees/feature-payment \
  cursor
```

**Note for agents**: Use the full path `plugins/universal/skills/worktree-create/scripts/detect_ide.sh` when invoking this skill from an agent context.

The script will:
1. Check for cursor (if preferred)
2. Fallback to VS Code if cursor not found
3. Open in new window (`-n` flag)
4. Report success or provide manual instructions

### Step 9: Report Success

Provide clear success message with:

```
✅ Worktree created successfully!

📍 Location: ../claude-toolkit_worktrees/feature-payment
🌿 Branch: feature-payment
💻 IDE: Cursor (opened in new window)

📋 Files copied:
  ✓ .env
  ✓ .claude/
  ✓ .cursor/

🚀 Ready to work! The new worktree is set up and ready for parallel development.

Next steps:
- Start a new Claude Code session in the new window
- Work on your feature independently
- Use "worktree 병합해줘" when ready to merge back
```

## Error Scenarios

### Not a Git Repository
```
❌ Error: Not a git repository

This command must be run from within a git repository.
Please navigate to your project directory and try again.
```

### Branch Already Exists
```
❌ Error: Branch 'feature-payment' already exists

Existing branch info:
  Branch: feature-payment
  Last commit: abc1234 - "Add payment feature"

Options:
1. Use a different branch name
2. Delete the existing branch: git branch -D feature-payment
3. Check out existing worktree: git worktree list
```

### Worktree Path Already Exists
```
❌ Error: Worktree path already exists

Path: ../claude-toolkit_worktrees/feature-payment

This might be:
1. An existing worktree (check: git worktree list)
2. A leftover directory from previous worktree

To fix:
- If it's a valid worktree: use it or remove with "worktree 정리해줘"
- If it's leftover: manually delete the directory
```

### Copy Script Fails
```
⚠️ Warning: Some files could not be copied

This is usually okay - these files might not exist in your project.
The worktree is still functional.

Skipped files:
  - .env.local (not found)
  - .vscode/ (not found)
```

### IDE Not Found
```
⚠️ Warning: Could not automatically open IDE

No cursor or VS Code installation found.

To open manually:
  cd ../claude-toolkit_worktrees/feature-payment
  cursor .   # or: code .
```

## Tips for Agents

1. **Always validate** git repository before attempting creation
2. **Check existing worktrees** to avoid conflicts
3. **Use full paths** when calling scripts from agent context
4. **Report errors clearly** with actionable solutions
5. **Confirm branch name** with user if not provided
6. **Offer config creation** if `.claude/worktree-config.json` doesn't exist

## References

- Configuration template: `plugins/universal/skills/worktree-create/references/config_template.json`
- Troubleshooting guide: `plugins/universal/skills/worktree-create/references/troubleshooting.md`
- Copy script: `plugins/universal/skills/worktree-create/scripts/copy_ignored_files.sh`
- IDE detection script: `plugins/universal/skills/worktree-create/scripts/detect_ide.sh`
