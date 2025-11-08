## Worktree Creation Troubleshooting Guide

Common issues and solutions when creating git worktrees.

---

### Issue: "fatal: invalid reference"

**Symptoms:**
```
fatal: invalid reference: feature-name
```

**Cause:** Invalid branch name (spaces, special characters, etc.)

**Solution:**
Use valid git branch naming:
- No spaces (use hyphens or underscores)
- No special characters like `~`, `^`, `:`, `?`, `*`, `[`
- Don't start with a hyphen
- No consecutive dots `..`

**Good names:**
- `feature-payment`
- `fix/bug-123`
- `feature_user_auth`

**Bad names:**
- `feature payment` (space)
- `feature@payment` (special char)
- `-feature` (starts with hyphen)

---

### Issue: "fatal: 'path' already exists"

**Symptoms:**
```
fatal: 'path' already exists
```

**Cause:** Directory already exists at the target location

**Solution:**

1. Check if it's an existing worktree:
   ```bash
   git worktree list
   ```

2. If listed, use it or remove it:
   ```bash
   git worktree remove path/to/worktree
   ```

3. If not listed (leftover directory), delete manually:
   ```bash
   rm -rf path/to/worktree
   ```

4. Then retry creating the worktree

---

### Issue: "fatal: a branch with that name already exists"

**Symptoms:**
```
fatal: a branch with that name already exists
```

**Cause:** Branch name is already used

**Solution:**

1. Check existing branches:
   ```bash
   git branch -a
   ```

2. Options:
   - Use a different branch name
   - Checkout the existing branch in a worktree:
     ```bash
     git worktree add path/to/worktree existing-branch
     ```
   - Delete the existing branch (⚠️ be careful):
     ```bash
     git branch -D branch-name
     ```

---

### Issue: Files not copied (.env, .claude/, etc.)

**Symptoms:**
Worktree created but missing `.env` or config files

**Cause:** Files don't exist in source or script failed

**Solution:**

1. Check if files exist in main repo:
   ```bash
   ls -la .env .claude/ .cursor/
   ```

2. If they exist, manually copy:
   ```bash
   cp .env path/to/worktree/
   cp -r .claude/ path/to/worktree/
   cp -r .cursor/ path/to/worktree/
   ```

3. Update configuration to match your project:
   - Edit `.claude/worktree-config.json`
   - Add/remove files from `copyFiles` array

---

### Issue: IDE doesn't open automatically

**Symptoms:**
Worktree created but Cursor/VS Code didn't launch

**Cause:** IDE not in PATH or not installed

**Solution:**

1. Verify IDE installation:
   ```bash
   which cursor
   which code
   ```

2. If not found, add to PATH or install command:

   **For Cursor:**
   - Open Cursor
   - Command Palette (Cmd+Shift+P)
   - "Shell Command: Install 'cursor' command in PATH"

   **For VS Code:**
   - Open VS Code
   - Command Palette (Cmd+Shift+P)
   - "Shell Command: Install 'code' command in PATH"

3. Manually open IDE:
   ```bash
   cd path/to/worktree
   cursor .
   # or
   code .
   ```

---

### Issue: Permission denied when running scripts

**Symptoms:**
```
Permission denied: copy_ignored_files.sh
```

**Cause:** Script not executable

**Solution:**

```bash
chmod +x plugins/universal/skills/worktree-create/scripts/*.sh
```

---

### Issue: rsync command not found

**Symptoms:**
```
bash: rsync: command not found
```

**Cause:** rsync not installed (rare on macOS/Linux)

**Solution:**

**macOS:**
```bash
brew install rsync
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install rsync
```

**Alternative:** Use `cp` instead of `rsync` in the script

---

### Issue: Worktree created in wrong location

**Symptoms:**
Worktree created but not where expected

**Cause:** Configuration path issue

**Solution:**

1. Check your configuration:
   ```bash
   cat .claude/worktree-config.json
   ```

2. Verify `worktreeDir` template:
   ```json
   {
     "worktreeDir": "../{repo}_worktrees"
   }
   ```

3. The `{repo}` placeholder is replaced with current directory name

4. To use absolute path:
   ```json
   {
     "worktreeDir": "/Users/yourname/worktrees/{repo}"
   }
   ```

---

### Issue: Git version too old

**Symptoms:**
```
git: 'worktree' is not a git command
```

**Cause:** Git version < 2.5

**Solution:**

1. Check git version:
   ```bash
   git --version
   ```

2. Upgrade git:

   **macOS:**
   ```bash
   brew upgrade git
   ```

   **Linux (Ubuntu/Debian):**
   ```bash
   sudo add-apt-repository ppa:git-core/ppa
   sudo apt-get update
   sudo apt-get install git
   ```

3. Verify upgrade:
   ```bash
   git --version
   # Should be 2.5 or higher
   ```

---

### Issue: "Not a git repository"

**Symptoms:**
```
fatal: not a git repository (or any of the parent directories): .git
```

**Cause:** Running command outside of a git repository

**Solution:**

1. Navigate to your project:
   ```bash
   cd /path/to/your/project
   ```

2. Verify it's a git repo:
   ```bash
   git status
   ```

3. If not initialized:
   ```bash
   git init
   ```

---

### Issue: Worktree directory not in .gitignore

**Symptoms:**
Worktree directories showing up in `git status`

**Cause:** Worktree parent directory is inside main repo

**Solution:**

1. **Best practice:** Keep worktrees outside main repo
   ```
   /Users/you/Projects/
   ├── my-project/          ← main repo
   └── my-project_worktrees/ ← worktrees (sibling)
       ├── feature-1/
       └── feature-2/
   ```

2. If inside main repo, add to `.gitignore`:
   ```bash
   echo "*_worktrees/" >> .gitignore
   git add .gitignore
   git commit -m "Ignore worktree directories"
   ```

---

### Issue: Disk space running out

**Symptoms:**
Multiple worktrees consuming lots of space

**Cause:** Each worktree is a full copy of working directory

**Solution:**

1. Clean up unused worktrees regularly:
   ```bash
   git worktree list
   # Remove unused ones
   git worktree remove path/to/unused
   ```

2. Check disk usage:
   ```bash
   du -sh my-project_worktrees/*
   ```

3. For large projects, consider:
   - Keeping fewer active worktrees
   - Using git worktree for short-lived feature branches only
   - Cleaning up after merging

---

### Issue: IDE settings not syncing between worktrees

**Symptoms:**
Each worktree has different IDE configurations

**Cause:** `.vscode/` or `.cursor/` are gitignored and copied independently

**Solution:**

**Option 1:** Track settings in git
```bash
# In main repo
git add .vscode/settings.json
git commit -m "Track VS Code settings"
```

**Option 2:** Use symbolic links
```bash
# In worktree
rm -rf .vscode
ln -s ../../../my-project/.vscode .vscode
```

**Option 3:** Accept differences
- Sometimes different settings per feature are useful
- Main repo has production settings
- Worktrees can have debugging/testing settings

---

### Issue: Git hooks not working in worktree

**Symptoms:**
Pre-commit hooks, etc. don't run in worktrees

**Cause:** Hooks are stored in `.git/hooks` which is in main repo

**Solution:**

Hooks automatically apply to all worktrees (they share `.git`). If not working:

1. Check hook location:
   ```bash
   ls -la .git/hooks/
   ```

2. Ensure hooks are executable:
   ```bash
   chmod +x .git/hooks/*
   ```

3. Test hook manually:
   ```bash
   .git/hooks/pre-commit
   ```

---

### Issue: Large node_modules or build artifacts copied

**Symptoms:**
Worktree creation is very slow, large disk usage

**Cause:** Copy script includes heavy directories

**Solution:**

1. Verify what's being copied:
   ```bash
   cat .claude/worktree-config.json
   ```

2. Ensure these are **NOT** in `copyFiles`:
   - `node_modules/`
   - `build/`
   - `dist/`
   - `.next/`
   - `target/` (Rust)
   - `venv/` (Python)

3. These should be regenerated in worktree:
   ```bash
   cd path/to/worktree
   npm install  # or equivalent
   ```

---

### Quick Diagnostic Commands

When things go wrong, run these:

```bash
# Check git worktree status
git worktree list

# Check for issues
git worktree prune

# Verify git version
git --version

# Check current directory
pwd

# Check if in git repo
git rev-parse --is-inside-work-tree

# List all branches
git branch -a

# Check for uncommitted changes
git status

# View worktree configuration
cat .claude/worktree-config.json

# Check script permissions
ls -l plugins/universal/skills/worktree-create/scripts/
```

---

## Getting Help

If issues persist:

1. **Check git worktree docs:**
   ```bash
   git worktree --help
   ```

2. **Ask Claude Code for help:**
   ```
   "I'm getting this error when creating a worktree: [paste error]"
   ```

3. **Manual worktree creation:**
   ```bash
   # Create manually to test
   mkdir -p ../my-project_worktrees
   git worktree add ../my-project_worktrees/test-branch -b test-branch
   cd ../my-project_worktrees/test-branch
   ```

4. **Reset if corrupted:**
   ```bash
   git worktree prune
   rm -rf ../my-project_worktrees/problematic-worktree
   git worktree add ../my-project_worktrees/new-attempt -b new-branch
   ```
