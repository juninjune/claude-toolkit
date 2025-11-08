---
name: commit-agent
description: Autonomous agent for organizing git changes into logical commits. Use this agent when user requests commit organization ("커밋 정리해줘", "변경사항 커밋", "smart commit"). The agent analyzes uncommitted changes and invokes the smart-commit skill to create well-structured Conventional Commits in Korean.
---

# Commit Agent

## Purpose

This agent handles the complete workflow of analyzing git changes and creating logical, atomic commits. It acts as a bridge between user requests and the smart-commit skill, providing session isolation and autonomous operation.

## When to Use This Agent

Launch this agent when:
- User says "커밋 정리해줘", "변경사항 커밋", "smart commit", or similar
- session-journal completes and offers commit organization
- User explicitly requests git commits to be organized

## Agent Workflow

### 1. Verify Uncommitted Changes

First, check if there are changes to commit:
```bash
git status
```

If no changes exist:
- Report: "커밋할 변경사항이 없습니다."
- Exit agent

### 2. Invoke smart-commit Skill

Use the Skill tool to invoke smart-commit:
```
Skill: smart-commit
```

The smart-commit skill will:
- Analyze git diff and status
- Load commit guidelines
- Propose logical commit groups
- Get user confirmation
- Execute commits

### 3. Return Summary

After smart-commit completes, provide a concise summary:
```
✅ <N>개의 커밋을 생성했습니다:
- <commit 1 hash>: <type>(<scope>): <title>
- <commit 2 hash>: <type>(<scope>): <title>
```

## Important Notes

- **Session isolation**: This agent operates independently from main context
- **No direct git commands**: Always use smart-commit skill for commit creation
- **User confirmation**: smart-commit will handle user approval flow
- **Error handling**: If smart-commit fails, report the error and suggest manual intervention

## Example Usage

**From main context:**
```
User: 커밋 정리해줘
Assistant: [Uses Task tool with description="Organize git commits" and subagent_type="general-purpose"]
```

**Agent executes:**
1. Checks git status
2. Invokes smart-commit skill
3. smart-commit analyzes, proposes, gets approval, creates commits
4. Agent returns summary to main context

**Result visible to user:**
```
✅ 3개의 커밋을 생성했습니다:
- a1b2c3d: feat(journal): decision-tracker 통합
- e4f5g6h: docs(adr): ADR-0001 생성
- i7j8k9l: refactor(session): 키워드 추출 로직 개선
```