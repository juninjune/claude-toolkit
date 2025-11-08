---
name: context-bridge
description: Manage context exhaustion by transitioning to a new session with structured context handoff. Triggered when token usage exceeds 80% during long tasks. Creates session documentation and generates a handoff message for seamless work continuation. Use when Claude proactively suggests it or user explicitly requests "context-bridge" or "세션 전환".
---

# Context Bridge

## Overview

Context-bridge enables seamless work continuation across Claude Code sessions when context windows become exhausted. Unlike `/compact` which compresses conversation history within the same session, context-bridge performs a **lossless session handoff**: documenting the current session completely in `.dev-journal/`, then generating a minimal handoff message to start a fresh session with only essential context.

## When to Use This Skill

### Proactive Trigger (Recommended)
Claude should **proactively suggest** context-bridge when:
- **Token usage ≥ 80%** AND work is ongoing (not near completion)
- User indicates more work ahead (e.g., "다음은...", "이제 [next task]...")
- Task complexity suggests it will exceed current context

**Suggestion template**:
```
토큰 사용량이 [X%]입니다. 작업이 계속될 것 같은데 context-bridge로
새 세션으로 전환하시겠습니까? 현재 작업을 문서화하고 핵심 컨텍스트만
다음 세션으로 이관해드리겠습니다.
```

### Explicit Invocation
User requests:
- "context-bridge 해줘"
- "세션 전환해줘"
- "새 세션으로 넘어가자"

### DO NOT Use When
- Token usage < 80% (not urgent)
- Work is nearly complete (no need for new session)
- User explicitly wants `/compact` instead
- In the middle of critical operation (wait for safe checkpoint)

## Core Workflow

### Step 1: Confirm Transition

When triggered (proactively or explicitly), confirm with the user:
```
현재 토큰 사용량: [X%]
작업을 문서화하고 새 세션으로 전환하겠습니다. 진행하시겠습니까?
```

If user declines, continue current session.

### Step 2: Document Current Session

**Use session-journal skill** to create a complete session record:
```
/skill universal:session-journal
```

This creates a timestamped markdown file in `.dev-journal/` with:
- Full conversation context
- Keyword extraction
- Related session links

**IMPORTANT**: Wait for session-journal to complete before proceeding.

### Step 3: Extract Minimal Context

Read the just-created session file and extract **ONLY** what's needed for the next session:

**A. Current Work Goal** (1-2 sentences):
```
Example: "API 엔드포인트 5개를 리팩토링하여 공통 에러 핸들링 로직을 적용하는 작업"
```

**B. Completed Work** (3-5 bullet points):
```
Example:
- ✅ `/api/users` 엔드포인트 리팩토링 완료
- ✅ 공통 에러 핸들러 `handleApiError()` 함수 생성
- ✅ 타입 정의 `ApiError` 인터페이스 추가
```

**C. Remaining Tasks** (from "Next Steps" section):
```
Example:
- [ ] `/api/posts` 엔드포인트에 에러 핸들러 적용
- [ ] `/api/comments` 엔드포인트에 에러 핸들러 적용
- [ ] 통합 테스트 작성
```

**D. Key Decisions** (1-2 critical choices only):
```
Example:
- 에러 응답 형식을 `{error: string, code: number, details?: any}` 구조로 표준화
```

**E. Essential File Paths** (3-5 files user will need):
```
Example:
- `src/api/users.ts` - 리팩토링 완료된 참조 코드
- `src/utils/handleApiError.ts` - 공통 에러 핸들러
- `src/types/api.ts` - 타입 정의
```

**Extraction Rules**:
- Keep it **minimal**: Only what's needed to resume work
- No code snippets (files are in the codebase)
- No detailed explanations (full context is in `.dev-journal/`)
- Focus on **actionable information**

### Step 4: Generate Handoff Message

Create a structured message for the user to paste in the new session:

**Template**:
```markdown
## 이전 세션 연속 작업

**세션 기록**: `.dev-journal/[YYYYMMDD_HHMM_topic-slug].md`

### 작업 목표
[1-2 sentence goal]

### 완료된 작업
- ✅ [Completed item 1]
- ✅ [Completed item 2]
- ✅ [Completed item 3]

### 다음 작업
- [ ] [Next task 1]
- [ ] [Next task 2]
- [ ] [Next task 3]

### 주요 결정사항
- [Key decision 1]
- [Key decision 2]

### 필요한 파일
- `[file/path/1]` - [purpose]
- `[file/path/2]` - [purpose]
- `[file/path/3]` - [purpose]

---

**첫 번째 작업**: [Next task 1 with brief context]
```

### Step 5: Instruct User

Provide clear instructions:
```
1. 위 메시지를 복사하세요
2. `/clear`를 입력하여 현재 세션을 종료하세요
3. 새 세션을 시작하고 복사한 메시지를 붙여넣으세요
4. 작업을 계속 진행하세요

전체 작업 맥락은 `.dev-journal/[filename].md`에 저장되었습니다.
필요시 `session-recall` 스킬로 참조할 수 있습니다.
```

## Best Practices

### 1. Timing is Critical
- **Too early**: Wastes context (session could have continued)
- **Too late**: May hit hard token limit before handoff completes
- **Sweet spot**: 80-85% token usage

### 2. Checkpoint Awareness
Don't trigger context-bridge in the middle of:
- File editing (wait for edit to complete)
- Test execution (wait for results)
- Bash command chains (wait for completion)

Find a **natural breakpoint** (task completed, decision made, safe state).

### 3. Handoff Message Quality
- **Specific, not generic**: "Refactor `/api/posts` endpoint" NOT "Continue refactoring"
- **Actionable**: User should know exactly what to do next
- **Self-contained**: No references to "the code above" or "as we discussed"

### 4. Don't Overload Handoff
Resist the urge to include everything. If user needs more context, they can:
- Read the full session file in `.dev-journal/`
- Use `session-recall` skill
- Read the relevant files directly

### 5. Integrate with Other Skills
- **session-journal**: Always call first to document session
- **session-recall**: Mention it as a fallback for detailed context
- **decision-tracker**: Reference ADR files if critical decisions were made

## Edge Cases

### User Wants to Continue Without Transition
```
User: 아니야, 그냥 계속 진행할게
Claude: 알겠습니다. 계속 진행하겠습니다. 필요하시면 언제든 "context-bridge" 명령으로 전환하실 수 있습니다.
```

### Token Limit Hit Before Completion
If token limit is hit during context-bridge execution:
```
1. Try to complete session-journal (highest priority)
2. If that fails, create a minimal emergency handoff:
   - Current task description
   - Last completed action
   - Immediate next step
3. Apologize and explain the situation
```

### Multiple Handoffs in a Row
If user needs multiple session transitions:
- Each session gets documented separately
- Handoff message should reference the original session as "root context"
- Example: "**원본 세션**: `.dev-journal/[first_session].md`"

## Common Pitfalls

- **Don't trigger too aggressively**: 80%+ is the threshold, not 70%
- **Don't skip session-journal**: The handoff message alone is not enough documentation
- **Don't include code in handoff**: Files exist in the codebase, just reference paths
- **Don't make handoff messages too long**: Defeats the purpose of context reduction

## Integration with /compact

Context-bridge and `/compact` serve different purposes:

| Feature | /compact | context-bridge |
|---------|----------|----------------|
| Paradigm | Compress history | Session handoff |
| Information | Lossy (summarized) | Lossless (documented) |
| Context | Same session | New session |
| Use case | Mid-session cleanup | Long task continuation |

**When to use which**:
- Use `/compact`: Short-term context reduction, work continues in ~30 mins
- Use `context-bridge`: Long task will span multiple hours/days, clean break needed

## Reference Documentation

For implementation details:

- **`references/handoff_format.md`**: Handoff message templates and examples
- **`references/context_extraction.md`**: Rules for extracting minimal context from session
- **`references/timing_strategies.md`**: When to trigger proactively vs wait

## Related Skills

- **session-journal**: Creates the session documentation (required)
- **session-recall**: Retrieves past session context if needed
- **decision-tracker**: ADRs can be referenced in handoff messages
