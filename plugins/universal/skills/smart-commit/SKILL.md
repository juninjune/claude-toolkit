---
name: smart-commit
description: "[AGENT-ONLY] Internal skill for analyzing git changes and creating logical commits. This skill should NEVER be invoked directly from main context. Only agents (like commit-agent) should use this skill. It operates independently using git commands and requires no session context."
---

# Smart Commit (Agent-Only)

## ⚠️ Usage Restriction

**THIS SKILL IS FOR AGENTS ONLY**

- **DO NOT** invoke this skill directly from main context
- **DO NOT** call this skill when user says "커밋 정리해줘" or similar
- **DO** use the Task tool to launch commit-agent instead
- **DO** let commit-agent invoke this skill autonomously

## Overview

Analyze uncommitted git changes and create logical, atomic commits with well-structured Conventional Commits messages in Korean. This skill intelligently groups changes by feature/issue context first, then by file type, ensuring each commit represents one coherent logical change.

## When Agents Should Use This Skill

Agents should use this skill when:
- Operating within commit-agent context
- There are uncommitted changes to analyze
- User has confirmed they want commits to be created
- Multiple unrelated changes need to be organized into logical commits

## Workflow

### Step 1: Analyze Current Changes

Run git commands to understand the current state:

```bash
git status
git diff
git diff --staged  # if there are staged changes
```

Review all changes thoroughly to understand:
- What files were modified
- What features or issues the changes address
- Whether changes are related or independent

### Step 2: Read Commit Guidelines

Load the commit guidelines reference to understand grouping strategy:

```
Read: plugins/universal/skills/smart-commit/references/commit_guidelines.md
```

This reference contains:
- Conventional Commits format with Korean descriptions
- Commit grouping decision tree
- Body writing guidelines for junior developer education
- Special cases (journal files, tests, config)

**Note for agents**: Use the full path `plugins/universal/skills/smart-commit/references/commit_guidelines.md` when invoking this skill from an agent context.

### Step 3: Propose Commit Groups

Based on the analysis and guidelines, propose logical commit groups to the user. For each proposed commit:

1. **List affected files**
2. **Suggest commit type and scope**: e.g., `feat(ocr)`, `docs(journal)`
3. **Provide commit title** (Korean)
4. **Explain grouping rationale**: Why these changes belong together
5. **Draft commit body** (2-4 sentences in Korean explaining context and approach)

**Grouping Priority**:
1. Feature/issue cohesion (highest priority) - Group related changes even if mixed file types
2. Logical atomicity - Each commit should represent one clear purpose
3. File type separation (lowest priority) - Only separate by type if unrelated

Present the proposal in a clear, structured format:

```
## Proposed Commits

### Commit 1: feat(ocr): 해상도 최적화 로직 구현
**Files:**
- lib/screens/text_extraction_test.dart
- .dev-journal/20251109_0111_ocr-resolution-optimization.md

**Rationale:**
코드 변경과 문서화가 같은 OCR 해상도 최적화 작업에 속하므로 함께 커밋합니다.

**Body:**
PDF를 고해상도(300 DPI)로 렌더링하도록 개선하여 OCR 정확도를 향상시켰습니다.
기존 72 DPI에서는 텍스트 인식률이 낮았으나, 300 DPI로 변경 후 한글 인식률이 크게 개선되었습니다.
개발 저널에 최적화 과정과 테스트 결과를 기록했습니다.

---

### Commit 2: docs(journal): OCR 구현 과정 업데이트
...
```

### Step 4: Get User Confirmation

After presenting the proposal, ask the user:

```
이렇게 커밋을 나누는 것이 적절할까요?
수정이 필요한 부분이 있다면 말씀해주세요.
```

Wait for user approval or feedback. If the user requests changes:
- Adjust the grouping or commit messages as requested
- Re-present the updated proposal
- Get confirmation again

### Step 5: Execute Commits

Once approved, create each commit sequentially:

For each commit:
1. Stage the relevant files: `git add <files>`
2. Create the commit with the approved message using heredoc format:

```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <title in Korean>

<body in Korean>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

3. Verify success: `git log -1 --stat`

### Step 6: Verify and Report

After all commits are created:

1. Run `git status` to confirm working directory is clean (or show remaining changes)
2. Run `git log -n <number-of-commits> --oneline` to show the created commits
3. Report summary to user:

```
✅ <N>개의 커밋을 생성했습니다:
- <commit 1 summary>
- <commit 2 summary>
- ...
```

## Important Notes

### Commit Message Quality

- **Title**: Clear, concise (50 chars or less), describes WHAT changed
- **Body**: 2-4 sentences explaining WHY and HOW, suitable for junior developers
  - Provide problem context
  - Explain solution approach
  - Avoid excessive technical detail
- **Korean language**: Use natural, professional Korean

### Grouping Decisions

**DO group together:**
- Code and related documentation for the same feature
- Tests with the feature they test
- Small config changes needed for a feature
- Multiple journal entries from the same work session

**DO separate:**
- Unrelated features or fixes
- Large configuration changes
- Documentation updates for different topics
- Changes that could be reverted independently

### Edge Cases

**Journal files**: Multiple related journal updates can be grouped. Use `docs(journal):` scope.

**Configuration files**: Small config changes can be included with related feature commits. Large or unrelated config changes should be separate `chore(config):` commits.

**Mixed staged/unstaged**: If some changes are already staged, preserve the staging area or ask user how to proceed.

**Empty commits**: If no changes exist, inform the user and skip commit creation.

## Resources

### references/commit_guidelines.md
Detailed guidelines for commit message format, grouping strategy decision tree, body writing style, and special cases. Load this file in Step 2 to inform the commit analysis and proposal.
