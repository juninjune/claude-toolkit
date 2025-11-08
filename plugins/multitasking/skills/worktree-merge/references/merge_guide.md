# Git Merge Conflict Resolution Guide

## Understanding Merge Conflicts

A merge conflict occurs when Git cannot automatically determine which changes to keep. This happens when:

1. **Same line edited**: Two branches modified the same line differently
2. **File deleted vs modified**: One branch deleted a file, another modified it
3. **Binary conflicts**: Binary files (images, PDFs) changed in both branches

## Conflict Markers Explained

When you open a conflicted file, you'll see markers like this:

```
<<<<<<< HEAD
Current content in main branch
=======
Your content from feature branch
>>>>>>> feature-payment
```

**Breaking it down:**
- `<<<<<<< HEAD`: Start of main branch content (current branch)
- `=======`: Separator between the two versions
- `>>>>>>> feature-payment`: End marker with feature branch name

## Resolution Strategies

### 1. Keep Current (Main Branch)
Choose this when main branch changes are correct.

**In VS Code/Cursor:**
- Click "Accept Current Change"

**Manually:**
```
Delete everything else, keep only:
Current content in main branch
```

### 2. Keep Incoming (Feature Branch)
Choose this when your worktree changes are correct.

**In VS Code/Cursor:**
- Click "Accept Incoming Change"

**Manually:**
```
Delete everything else, keep only:
Your content from feature branch
```

### 3. Keep Both Changes
Choose this when both changes are needed.

**In VS Code/Cursor:**
- Click "Accept Both Changes"

**Manually:**
```
Current content in main branch
Your content from feature branch
```

Then edit to make sense together.

### 4. Manual Edit (Best for Complex Conflicts)
Choose this when you need to combine or rewrite.

1. Delete all conflict markers
2. Write the correct version
3. Test the result

## Step-by-Step Resolution Process

### Step 1: Identify All Conflicted Files

```bash
git status
```

Look for "both modified" files.

Or use:
```bash
git diff --name-only --diff-filter=U
```

### Step 2: Open Each File

Use your IDE's conflict resolution UI:
- **VS Code/Cursor**: Click on conflicted files, use inline buttons
- **Other editors**: Manually edit the file

### Step 3: Choose Resolution Strategy

For each conflict:
1. Read both versions carefully
2. Understand the intent of each change
3. Choose or combine accordingly

### Step 4: Remove All Markers

Ensure no conflict markers remain:
- No `<<<<<<<`
- No `=======`
- No `>>>>>>>`

### Step 5: Test the Resolution

If it's code:
```bash
# Run your tests
npm test
# or
flutter test
# or
pytest
```

If it's configuration:
- Check syntax
- Verify values make sense

### Step 6: Stage Resolved Files

```bash
# Stage individual files
git add path/to/resolved/file.dart

# Or stage all resolved files
git add .
```

### Step 7: Commit the Merge

```bash
# Git will use a default merge commit message
git commit

# Or provide a custom message
git commit -m "Merge feature-payment into main

Resolved conflicts in:
- lib/screens/home_screen.dart: kept both navigation changes
- README.md: combined documentation updates
"
```

### Step 8: Verify the Merge

```bash
# Check the merge commit
git log --oneline -3

# Check no conflicts remain
git status
```

## Common Conflict Scenarios

### Scenario 1: Both Added Same Navigation Item

**Main branch (HEAD):**
```dart
items: [
  NavItem('Home'),
  NavItem('Profile'),  // Added in main
]
```

**Feature branch:**
```dart
items: [
  NavItem('Home'),
  NavItem('Settings'),  // Added in feature
]
```

**Resolution**: Keep both
```dart
items: [
  NavItem('Home'),
  NavItem('Profile'),
  NavItem('Settings'),
]
```

### Scenario 2: Different Function Implementations

**Main branch:**
```dart
double calculateTotal() {
  return items.fold(0, (sum, item) => sum + item.price);
}
```

**Feature branch:**
```dart
double calculateTotal() {
  // Added tax calculation
  var subtotal = items.fold(0, (sum, item) => sum + item.price);
  return subtotal * 1.10; // 10% tax
}
```

**Resolution**: Keep feature branch version (has enhancement)
```dart
double calculateTotal() {
  // Added tax calculation
  var subtotal = items.fold(0, (sum, item) => sum + item.price);
  return subtotal * 1.10; // 10% tax
}
```

### Scenario 3: README Documentation Conflict

**Main branch:**
```markdown
## Features

- User authentication
- Profile management
- Dashboard
```

**Feature branch:**
```markdown
## Features

- User authentication
- Profile management
- Payment processing
```

**Resolution**: Combine both
```markdown
## Features

- User authentication
- Profile management
- Dashboard
- Payment processing
```

### Scenario 4: Import Statement Conflicts

**Main branch:**
```dart
import 'package:app/models/user.dart';
import 'package:app/services/api.dart';
import 'package:app/utils/validator.dart';
```

**Feature branch:**
```dart
import 'package:app/models/user.dart';
import 'package:app/services/api.dart';
import 'package:app/services/payment.dart';
```

**Resolution**: Merge and sort
```dart
import 'package:app/models/user.dart';
import 'package:app/services/api.dart';
import 'package:app/services/payment.dart';
import 'package:app/utils/validator.dart';
```

## Binary File Conflicts

For binary files (images, PDFs, compiled files):

```bash
# Keep main branch version
git checkout --ours path/to/file.png

# Keep feature branch version
git checkout --theirs path/to/file.png

# Then stage
git add path/to/file.png
```

## Aborting a Merge

If you need to cancel the merge:

```bash
# Abort and return to pre-merge state
git merge --abort
```

This is safe and will restore your repository to before the merge attempt.

## Prevention Tips

1. **Commit frequently**: Smaller, focused commits are easier to merge
2. **Pull/merge main regularly**: Keep your feature branch up to date
3. **Communicate**: If working with a team, coordinate on shared files
4. **Use feature flags**: For long-running features, merge frequently with flags
5. **Modular code**: Well-separated code has fewer conflicts

## Getting Help

If you're stuck on a conflict:

1. **Ask Claude Code**: Describe the conflict and ask for advice
   ```
   "I have a merge conflict in payment.dart between two different
   implementation approaches. Here's the conflict: [paste code]"
   ```

2. **Consult the team**: For complex business logic conflicts

3. **Check git history**: Understand why each change was made
   ```bash
   git log -p path/to/conflicted/file.dart
   ```

4. **Use a diff tool**: For complex conflicts
   ```bash
   git mergetool
   ```

## After Resolution

Once all conflicts are resolved and committed:

1. **Run tests**: Ensure nothing broke
2. **Review changes**: `git diff HEAD~1`
3. **Push changes**: `git push origin main`
4. **Clean up worktree**: `"worktree 정리해줘"`

## Quick Reference

```bash
# View conflicted files
git status
git diff --name-only --diff-filter=U

# Choose version for entire file
git checkout --ours <file>    # Keep main
git checkout --theirs <file>  # Keep feature

# After resolving
git add <file>
git commit

# Abort merge
git merge --abort
```

## Remember

- **Take your time**: Conflicts are normal and expected
- **Test thoroughly**: After resolution, verify everything works
- **Commit clearly**: Document what conflicts you resolved and how
- **Ask for help**: When in doubt, consult the team or Claude Code

Merge conflicts are an opportunity to understand both sets of changes deeply!
