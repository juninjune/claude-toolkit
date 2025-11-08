# Example: Bug Investigation Handoff

This example demonstrates a context-bridge handoff during a complex bug investigation that requires deep context.

## Scenario

User is investigating a memory leak in a React dashboard. After 2 hours of debugging, Claude has identified the root cause and partially implemented a fix. Token usage reaches 85% while still mid-fix.

## Original Session Context

**Session**: `.dev-docs/sessions/20251109_1615_memory-leak-investigation.md`

**What happened** (summary):
- User reported: Dashboard crashes after ~30 minutes of use
- Chrome DevTools Memory Profiler revealed growing heap
- Investigated 5 components: `Dashboard`, `DataChart`, `AnalyticsWidget`, `UserTable`, `ActivityFeed`
- Root cause identified: Event listeners not cleaned up in `useEffect`
- Fixed `DataChart` component (added cleanup function)
- Still need to fix `AnalyticsWidget` and `ActivityFeed`
- Need to verify fix with memory profiling

**Token usage**: 170,000 / 200,000 (85%)

**Critical context**:
- Specific pattern identified: Chart.js instances + resize event listeners
- Decision: Use `useEffect` cleanup, not `componentWillUnmount` (functional components)

## Generated Handoff Message

```markdown
## 이전 세션 연속 작업

**세션 기록**: `.dev-docs/sessions/20251109_1615_memory-leak-investigation.md`

### 작업 목표
대시보드 페이지에서 발생하는 메모리 누수를 수정하여 장시간 사용 시 브라우저 크래시 방지

### 완료된 작업
- ✅ Chrome DevTools Memory Profiler로 누수 원인 특정: Chart.js 인스턴스 및 resize 이벤트 리스너 미정리
- ✅ `DataChart` 컴포넌트 수정: `useEffect` cleanup 함수 추가, `.destroy()` 호출
- ✅ 패턴 확립: 모든 차트 컴포넌트에 동일 cleanup 패턴 적용 필요

### 다음 작업
- [ ] `AnalyticsWidget` 컴포넌트에 동일 cleanup 패턴 적용
- [ ] `ActivityFeed` 컴포넌트의 인터벌 타이머 정리 추가
- [ ] 메모리 프로파일링으로 수정 검증 (30분 실행 테스트)

### 주요 결정사항
- Chart.js 인스턴스를 `useRef`에 저장하여 cleanup에서 접근 - 클로저 문제 방지

### 필요한 파일
- `src/components/DataChart.tsx` - 수정 완료된 참조 코드 (cleanup 패턴)
- `src/components/AnalyticsWidget.tsx` - 다음 수정 대상 (동일 이슈)
- `src/components/ActivityFeed.tsx` - 인터벌 타이머 정리 필요
- `src/pages/Dashboard.tsx` - 메모리 누수 발생 페이지

---

**첫 번째 작업**: `AnalyticsWidget` 컴포넌트 메모리 누수 수정

`AnalyticsWidget.tsx`는 `DataChart`와 동일한 Chart.js 사용 패턴입니다.
`DataChart.tsx:45-62`의 cleanup 패턴(useRef로 인스턴스 저장, useEffect cleanup에서
`.destroy()` 및 이벤트 리스너 제거)을 그대로 적용하세요.
```

## User Workflow

1. **Session 1** (token at 85%, mid-investigation):
   ```
   Claude: [analyzing ActivityFeed component]
           토큰 사용량이 85%입니다. 버그 수정 작업이 계속될 것 같은데
           context-bridge로 새 세션으로 전환하시겠습니까?

           현재까지 완료: DataChart 수정 완료
           남은 작업: AnalyticsWidget, ActivityFeed 수정 및 검증

   User: 응, 전환하자
   Claude: [generates handoff message]
           [calls session-journal to document investigation process]

           위 메시지를 복사한 후:
           1. `/clear` 입력
           2. 새 세션 시작
           3. 메시지 붙여넣기

           전체 디버깅 과정과 발견한 단서들은 세션 파일에 보존되었습니다.
   ```

2. **User starts new session** with handoff message

3. **Claude in new session**:
   ```
   이전 세션에서 메모리 누수 조사를 이어받았습니다.

   완료 사항:
   - 원인: Chart.js 인스턴스 및 이벤트 리스너 미정리
   - DataChart 컴포넌트 수정 완료

   AnalyticsWidget 수정을 시작하겠습니다. 먼저 두 파일을 비교하여
   동일한 패턴을 적용하겠습니다.

   [reads DataChart.tsx, AnalyticsWidget.tsx]
   [applies fix using reference pattern]
   ```

## Why Context-Bridge is Critical Here

### Deep Context Preserved

**In session file** `.dev-docs/sessions/20251109_1615_memory-leak-investigation.md`:
- Full investigation timeline (which components checked first)
- Dead ends explored (UserTable was suspected but ruled out)
- Memory profiler screenshots/data
- Specific line numbers where leaks occurred
- Discussion of alternative approaches considered

**In handoff message**:
- Only the **actionable outcome**: Root cause + fix pattern
- Reference to detailed investigation (session file)

### Lossless Knowledge Transfer

If user had used `/compact` instead:
- Might lose details about which components were already ruled out
- Risk of re-investigating the same dead ends
- Might forget the specific cleanup pattern that worked
- No permanent record of the investigation process

With context-bridge:
- New session knows exactly where to continue
- All investigation history preserved
- Reference pattern clearly documented
- Future reference via `session-recall` (e.g., "이전에 메모리 누수 어떻게 해결했지?")

## Key Features Demonstrated

### 1. Complex Investigation Preserved
- Root cause clearly stated (not obvious from code alone)
- Pattern established (reusable for similar fixes)
- Decisions documented (why `useRef`, not other approaches)

### 2. Immediate Actionability
- User doesn't need to re-investigate
- Clear next step with reference to working example
- Specific line numbers provided

### 3. Fallback to Full Context
- If new session Claude needs more details, can read session file
- Example: "왜 UserTable은 수정 안 하나요?" → session file explains it was ruled out

## Handoff Quality Assessment

**What makes this handoff effective**:

✅ **Clear root cause**: "Chart.js 인스턴스 및 resize 이벤트 리스너 미정리"
- User immediately knows what the problem was

✅ **Reference pattern**: "DataChart.tsx:45-62의 cleanup 패턴"
- New session can replicate the fix exactly

✅ **Critical decision preserved**: "useRef에 저장하여 cleanup에서 접근"
- Prevents user from trying less effective approaches

✅ **Minimal size**: ~200 words
- Doesn't waste context on full investigation timeline

**What's excluded (but preserved in session file)**:
- Initial hypothesis (wrong guess: "UserTable pagination issue")
- Steps to reproduce the bug
- Detailed profiler analysis
- Alternative solutions considered (WeakMap, manual tracking)

## Alternative: What if `/compact` was used?

**Likely outcome**:
```
User: 계속해서 AnalyticsWidget 수정해줘
Claude: [reads AnalyticsWidget.tsx]
        이 컴포넌트에서 어떤 메모리 누수 패턴을 발견하셨나요?
        (context about root cause was compressed away)

User: 이벤트 리스너 안 정리한 거
Claude: 알겠습니다. cleanup 함수를 추가하겠습니다.
        [might use a different pattern than DataChart]
        (inconsistent fixes across components)
```

**Problem**: Lost context about the established pattern and root cause specifics.

## Session File Contents (Excerpt)

For reference, the full session file contains:

```markdown
## What We Did

### 1. 문제 재현 및 관찰
- 대시보드 30분 실행 → Chrome 탭 크래시
- DevTools Memory Profiler: Heap 크기 150MB → 800MB

### 2. 용의자 컴포넌트 조사
- `UserTable`: 페이지네이션 데이터 정리 확인 → **문제 없음**
- `ActivityFeed`: setInterval 사용 → **정리 안됨** (추가 작업 필요)
- `DataChart`, `AnalyticsWidget`: Chart.js 사용 → **주범**

### 3. 근본 원인 특정
Chart.js 인스턴스를 생성하지만 컴포넌트 언마운트 시 `.destroy()` 호출 안 함.
또한 window resize 이벤트 리스너 등록 후 제거 안 함.

### 4. 해결 방법 탐색
- ❌ componentWillUnmount: 함수형 컴포넌트라서 사용 불가
- ❌ WeakMap 사용: 복잡도 증가, 오버엔지니어링
- ✅ useEffect cleanup: 표준 React 패턴, 간단명료

### 5. DataChart 수정
`src/components/DataChart.tsx:45-62` 참조

Before:
```typescript
useEffect(() => {
  const chart = new Chart(canvasRef.current, config)
  window.addEventListener('resize', handleResize)
}, [data])
```

After:
```typescript
const chartRef = useRef<Chart | null>(null)

useEffect(() => {
  chartRef.current = new Chart(canvasRef.current, config)
  window.addEventListener('resize', handleResize)

  return () => {
    chartRef.current?.destroy()
    window.removeEventListener('resize', handleResize)
  }
}, [data])
```

## Key Decisions

- **useRef 사용 이유**: cleanup 함수에서 차트 인스턴스에 접근해야 하는데,
  클로저로 직접 참조하면 stale closure 문제 발생 가능. useRef는 항상 최신 참조 유지.

...
```

**Size**: ~5,000 words with code examples and full reasoning

**Handoff message**: ~200 words, only essential outcomes

**Result**: 25x context reduction while preserving all knowledge
