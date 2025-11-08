# Timing Strategies for Context-Bridge

This document defines when and how to trigger context-bridge proactively or responsively.

## Core Principle

Context-bridge should trigger at the **sweet spot** where:
- Context exhaustion is imminent (80%+)
- User has more work ahead (not near completion)
- Current state is a safe checkpoint (no operations in-flight)

**Too early**: Wastes context, unnecessary session break
**Too late**: May hit hard limit before handoff completes
**Just right**: Seamless transition with minimal disruption

## Token Usage Monitoring

Claude Code provides token usage information in context. Monitor for:
- **Current usage**: Tokens consumed so far
- **Budget**: Total available tokens (e.g., 200,000)
- **Percentage**: Current / Budget

**Trigger threshold**: **80% token usage**

Example detection:
```
<system_warning>Token usage: 162000/200000; 38000 remaining</system_warning>

→ 81% used, 19% remaining
→ TRIGGER ZONE: Suggest context-bridge
```

## Proactive Trigger Conditions

Suggest context-bridge when **ALL** of these conditions are met:

### 1. Token Usage ≥ 80%
```
Token usage: 160000/200000 or higher
```

### 2. Work is Ongoing
Indicators that more work is ahead:
- User mentions future tasks: "다음은...", "이제 [task]...", "그 다음에..."
- Current task is part of a sequence: "3개 중 1개 완료"
- User asks about next steps: "뭐 하면 될까?"
- Task list (TodoWrite) has pending items

**Counter-indicators** (do NOT trigger):
- User says: "마지막...", "이제 끝", "완료했어"
- No pending todos
- Current task is clearly final (e.g., "문서화", "정리")

### 3. Safe Checkpoint
Current state allows interruption:
- ✅ Task just completed
- ✅ File edit committed
- ✅ Tests passed
- ✅ Bash command finished
- ✅ User asked a question (natural pause)

**Unsafe states** (wait before triggering):
- ❌ In the middle of file editing (Edit tool called, not yet complete)
- ❌ Bash command running in background
- ❌ Test execution in progress
- ❌ Claude is in the middle of explaining something complex

## Suggestion Templates

### Standard Proactive Suggestion

```
토큰 사용량이 [X%]입니다. 작업이 계속될 것 같은데 context-bridge로
새 세션으로 전환하시겠습니까? 현재 작업을 문서화하고 핵심 컨텍스트만
다음 세션으로 이관해드리겠습니다.

현재까지 완료: [brief 1-line summary]
남은 작업: [brief 1-line summary]

계속 진행하려면 "응" 또는 "context-bridge",
현재 세션 유지하려면 "아니" 또는 "계속"을 입력하세요.
```

### After Todo List Update

If TodoWrite shows many pending tasks:
```
토큰 사용량이 [X%]이고 남은 작업이 [N]개입니다.
context-bridge로 새 세션을 시작하시겠습니까?

남은 작업:
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3
...
```

### Near Completion (Do Not Trigger)

If work is nearly done:
```
(No suggestion - let user finish in current session)
```

## User Response Handling

### Positive Responses
User agrees to transition:
- "응", "그래", "좋아", "해줘"
- "context-bridge"
- "세션 전환"

**Action**: Proceed with context-bridge workflow

### Negative Responses
User wants to continue:
- "아니", "아니야", "괜찮아", "계속"
- "나중에"
- "/compact" (user prefers compaction)

**Action**:
```
알겠습니다. 계속 진행하겠습니다.
필요하시면 언제든 "context-bridge"로 세션을 전환하실 수 있습니다.
```

### Ambiguous Responses
User doesn't clearly accept or decline:
- "잠깐만", "기다려"
- "일단 [task] 먼저"

**Action**: Wait and respect user's intent, re-suggest later if still at 80%+

## Explicit Invocation

User directly requests context-bridge:
- "context-bridge 해줘"
- "세션 전환해줘"
- "새 세션으로 넘어가자"

**Action**:
- Skip suggestion, proceed directly
- Confirm current state is safe (if mid-operation, wait for completion)
- Execute context-bridge workflow

## Timing Edge Cases

### Case 1: Token Usage Spikes Suddenly

```
75% → 88% in one response (large file read, complex task)
```

**Action**:
- Suggest immediately, even if mid-task
- Explain urgency: "토큰이 예상보다 빠르게 소진되어..."

### Case 2: Gradual Approach to Threshold

```
70% → 75% → 78% → 82% over multiple exchanges
```

**Action**:
- At 78%: Mention token status casually ("토큰 사용량이 78%입니다")
- At 82%: Formal context-bridge suggestion

### Case 3: User Keeps Declining

```
82% → suggest → declined
85% → suggest → declined
90% → ???
```

**Action**:
- At 90%: More urgent tone
  ```
  토큰이 거의 다 찼습니다(90%). 곧 자동 compaction이 발생할 수 있습니다.
  context-bridge로 작업 내용을 보존하고 새 세션으로 전환하는 것을 강력히 권장합니다.
  ```
- At 95%: Final warning
  ```
  토큰 한계에 근접했습니다(95%). 자동 compaction 전에 context-bridge를 실행하지 않으면
  세부 컨텍스트가 손실될 수 있습니다.
  ```

### Case 4: Task Completes Before Threshold

```
80% reached → suggest → user: "거의 다 했어"
→ 5 minutes later → 85% → task complete
```

**Action**:
- If user indicates near-completion, don't insist
- Suggest `/compact` instead as a lighter option

### Case 5: Multiple Handoffs in Sequence

Second or third handoff in a row (user has very long task):

```
Session 1 → 80% → handoff → Session 2 → 80% → handoff → Session 3
```

**Action**:
- Reference original session: "**원본 세션**: `.dev-docs/sessions/[first_session].md`"
- Consolidate context if possible (don't keep expanding)
- Suggest task decomposition to user

## Safe Checkpoint Detection

### Identifying Safe States

**Monitor recent tool calls**:

1. **Just completed a discrete task**:
   - TodoWrite shows task marked completed
   - User says: "완료", "됐어", "끝"
   - Tests passed successfully

2. **Natural conversation pause**:
   - User asked a question
   - Claude asked a question and waiting for answer
   - User reviewing output

3. **File operations complete**:
   - Edit tool executed successfully
   - Write tool finished
   - Read tool returned (information gathering complete)

4. **Bash commands finished**:
   - Command exited with code 0
   - No background processes running
   - Git commit completed

### Identifying Unsafe States

**Do NOT trigger if**:

1. **Mid-operation**:
   - Edit tool called, user hasn't confirmed result
   - Bash command running (no exit code yet)
   - Test execution in progress
   - Background process active (check with BashOutput)

2. **Mid-explanation**:
   - Claude is explaining complex logic
   - User is reading large output
   - Debugging in progress (multiple read/grep cycles)

3. **Critical section**:
   - Git operations in progress (add, commit)
   - Database migrations running
   - Build process executing

**Detection heuristic**:
- Look at last 3-5 tool calls
- If most recent tool call is pending or just started → **UNSAFE**
- If most recent tool call completed and user responded → **SAFE**

## Timing Optimization

### Ideal Trigger Moments

**Best times** (in order of preference):

1. **Right after task completion**:
   ```
   User: 이제 다음 컨트롤러 리팩토링해줘
   Claude: [checks token usage: 82%]
           토큰 사용량이 82%입니다. context-bridge로 전환하시겠습니까?
   ```

2. **During planning/discussion**:
   ```
   User: 다음에 뭐 하면 될까?
   Claude: [checks token usage: 81%]
           다음 작업을 논의하기 전에, 토큰이 81%입니다. context-bridge로...
   ```

3. **After information gathering**:
   ```
   Claude: [read 5 files to understand codebase]
           코드베이스를 파악했습니다. 그런데 토큰이 83%라서...
   ```

### Suboptimal Moments (Wait)

**Defer trigger until better moment**:

1. **Mid-debugging**:
   ```
   User: 왜 이 버그가 생기는 거지?
   Claude: [investigating with multiple reads/greps]
           (wait until root cause found, THEN suggest)
   ```

2. **Mid-file-edit**:
   ```
   Claude: [Edit tool executing]
           (wait for edit to complete and user to confirm)
   ```

3. **User is focused**:
   ```
   User: [rapid-fire questions/instructions]
   Claude: (user is in flow state, don't interrupt)
   ```

## Integration with /compact

If user has both options available:

### When to Suggest context-bridge over /compact

- Work will span multiple sessions (hours/days)
- Need full context preservation (complex debugging, large refactor)
- Many pending tasks (5+)
- Critical decisions made that shouldn't be compressed

### When to Suggest /compact instead

- Work might finish in current session (~30 mins)
- Simple, linear task (no complex dependencies)
- User prefers staying in same session
- Token usage < 85% (not urgent)

**Combined approach**:
```
토큰 사용량이 82%입니다. 두 가지 옵션이 있습니다:

1. `/compact`: 현재 세션 유지, 대화 내용 압축 (작업이 곧 끝날 것 같으면 추천)
2. `context-bridge`: 새 세션 전환, 완전한 기록 보존 (작업이 길어질 것 같으면 추천)

어떤 방식을 선호하시나요?
```

## Monitoring Strategy

Claude should **continuously monitor** token usage:

1. **Every response**: Check `<system_warning>Token usage: X/Y</system_warning>`
2. **Calculate percentage**: X / Y * 100
3. **If ≥ 80%**: Evaluate trigger conditions (ongoing work? safe checkpoint?)
4. **If conditions met**: Suggest context-bridge
5. **If declined**: Re-check at +5% increments (85%, 90%, 95%)

**Implementation note**: Token usage warnings appear automatically in system messages. Claude doesn't need to call a tool to check usage; just parse the warning.

## Example Decision Flow

```
┌─────────────────────────┐
│ Token Usage ≥ 80%?     │
└───────┬─────────────────┘
        │ Yes
        ▼
┌─────────────────────────┐
│ Work ongoing?           │  ← User says "다음은...", todos pending
└───────┬─────────────────┘
        │ Yes
        ▼
┌─────────────────────────┐
│ Safe checkpoint?        │  ← Task complete, no operations in-flight
└───────┬─────────────────┘
        │ Yes
        ▼
┌─────────────────────────┐
│ SUGGEST CONTEXT-BRIDGE  │
└─────────────────────────┘
```

If any condition is "No", wait and re-evaluate later.

## Quality Checklist

Before suggesting context-bridge:

- [ ] Token usage is **≥ 80%**
- [ ] User has indicated **more work ahead**
- [ ] Current state is a **safe checkpoint** (no in-flight operations)
- [ ] Last task or sub-task is **complete** (not mid-action)
- [ ] User is **not in rapid-fire mode** (multiple quick messages)
- [ ] Suggestion is **clear and concise** (not buried in long response)
- [ ] User is given **clear yes/no choice**

## Anti-Patterns to Avoid

### ❌ Triggering Too Early
```
Token usage: 72%
Claude: "토큰이 70%가 넘었으니 context-bridge 하실래요?"
```
**Problem**: Premature, user can continue for a while

### ❌ Triggering Mid-Task
```
Token usage: 83%
User: "이 함수 리팩토링해줘"
Claude: [starts editing] "context-bridge 하실래요?"
```
**Problem**: Interrupts active work

### ❌ Ignoring User's Decline
```
Token usage: 82%
Claude: "context-bridge 하실래요?"
User: "아니, 계속해"
Token usage: 85%
Claude: "context-bridge 하실래요?"
User: "아니라고"
Token usage: 88%
Claude: "context-bridge 하실래요?"
```
**Problem**: Annoying, respect user's choice

### ❌ Not Monitoring Token Usage
```
Token usage: 65% → 70% → 78% → 85% → 92% (never suggested)
Claude: [suddenly hits limit, auto-compaction kicks in]
```
**Problem**: Missed opportunity for lossless handoff

## Summary

**Golden Rules**:
1. Monitor token usage **every response**
2. Suggest at **80%** if work is ongoing and state is safe
3. **Respect user's choice** if declined
4. Find **natural breakpoints** (task boundaries, pauses)
5. **Never interrupt** mid-operation or mid-explanation
