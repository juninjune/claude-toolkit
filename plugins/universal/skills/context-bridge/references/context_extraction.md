# Context Extraction Rules

This document defines how to extract minimal essential context from a full session document for context-bridge handoffs.

## Extraction Philosophy

**The Golden Rule**: Include only what the user **cannot easily find** or **reconstruct** themselves.

- **DON'T include**: Code, detailed explanations, obvious information
- **DO include**: Decisions made, tasks completed, priorities set, non-obvious file locations

Think of it as a **memory aid**, not a tutorial.

## Input: Full Session Document

Context-bridge receives a complete `.dev-journal/YYYYMMDD_HHMM_topic-slug.md` file with:
- Full conversation history (implicitly in Claude's context)
- Summary section
- Keywords
- What We Did section
- Key Decisions section
- Next Steps section

## Output: Handoff Components

Extract these five components:

### 1. Work Goal (작업 목표)

**Source**: Session title + Summary section

**Extraction process**:
1. Read session title and summary
2. Identify the **overarching objective** (not individual tasks)
3. Condense to 1-2 sentences
4. Include **what** and **why** (but not how)

**Example extraction**:

Input (session summary):
> "REST API의 에러 핸들링을 표준화하고 인증 미들웨어를 추가하는 리팩토링 작업. 현재 각 컨트롤러마다 에러 처리 방식이 달라서 일관성이 없고, 인증 로직이 각 엔드포인트에 중복 구현되어 있음. 공통 에러 핸들러와 인증 미들웨어를 만들어 8개 엔드포인트에 적용 예정."

Output (work goal):
> "REST API 엔드포인트 8개에 표준화된 에러 핸들링과 인증 미들웨어를 적용하여 일관된 에러 응답과 보안 강화"

**Rules**:
- 20-40 words
- Remove background/motivation details (they're in the session file)
- Focus on **outcome**, not process
- No specific file names (too detailed)

### 2. Completed Work (완료된 작업)

**Source**: "What We Did" section + conversation history

**Extraction process**:
1. Scan "What We Did" for discrete completed tasks
2. Prioritize **major milestones** (not every small edit)
3. Include file/component names for context
4. Convert to checklist format with ✅

**Example extraction**:

Input ("What We Did" section):
> "1. 공통 에러 핸들러 구현
>    - `src/utils/errorHandler.ts` 파일 생성
>    - `handleApiError(error, res)` 함수 작성
>    - 다양한 에러 타입 처리 (Validation, Database, Auth 등)
>    - 표준 에러 응답 형식 적용
>
> 2. 인증 미들웨어 구현
>    - `src/middleware/auth.ts` 파일 생성
>    - JWT 토큰 검증 로직
>    - 권한 체크 로직
>
> 3. UserController 리팩토링
>    - 7개 메서드 모두 try-catch 추가
>    - handleApiError 호출 통합
>    - 불필요한 중복 코드 제거
>
> 4. 타입 정의
>    - ApiErrorResponse 인터페이스
>    - AuthPayload 타입"

Output (completed work):
```
- ✅ 공통 에러 핸들러 `handleApiError()` 구현 (`src/utils/errorHandler.ts`)
- ✅ 인증 미들웨어 `requireAuth()` 구현 (`src/middleware/auth.ts`)
- ✅ `UserController` 전체 메서드 리팩토링 (try-catch + error handler 적용)
- ✅ 에러 응답 타입 `ApiErrorResponse` 인터페이스 정의
```

**What was omitted**:
- Sub-bullet implementation details ("JWT 토큰 검증 로직", "권한 체크 로직")
- Specific line counts ("7개 메서드")
- Minor supporting types (`AuthPayload` - less critical)

**Rules**:
- 3-5 items maximum
- Each item = one **logical unit of work** (function, component, refactor)
- Include file paths for orientation
- Group related sub-tasks (don't list every file edit separately)
- Use past tense, outcomes-focused language

**Prioritization heuristic**:
1. New functionality/components (highest priority)
2. Major refactorings
3. Bug fixes
4. Minor changes (lowest priority - often omitted)

### 3. Remaining Tasks (다음 작업)

**Source**: "Next Steps" section

**Extraction process**:
1. Copy unchecked items from "Next Steps"
2. Re-order by priority if needed
3. Add file/component context if not present
4. Limit to 3-5 items

**Example extraction**:

Input ("Next Steps" section):
```
- [ ] PostController 리팩토링
- [ ] CommentController 리팩토링
- [ ] 라우터에 인증 미들웨어 적용
- [ ] 통합 테스트 작성
- [ ] 에러 핸들러 단위 테스트
- [ ] API 문서 업데이트
- [ ] 로그 형식 통일
```

Output (remaining tasks):
```
- [ ] `PostController`에 에러 핸들러 적용 (5개 메서드)
- [ ] `CommentController`에 에러 핸들러 적용 (4개 메서드)
- [ ] 모든 엔드포인트에 인증 미들웨어 라우터 레벨 적용
- [ ] 통합 테스트 작성: 인증 실패 및 에러 응답 형식 검증
```

**What was omitted**:
- "에러 핸들러 단위 테스트" (lower priority than integration tests)
- "API 문서 업데이트" (peripheral task)
- "로그 형식 통일" (nice-to-have)

**Rules**:
- 3-5 items, **ordered by priority**
- Add specificity: file names, counts, scope
- First item = immediate next action
- Omit peripheral tasks (docs, cleanup, etc.) unless critical
- Focus on **core work**, not polish

**Prioritization heuristic**:
1. Direct continuation of current work (highest priority)
2. Related functionality
3. Testing critical paths
4. Polish/documentation (lowest - often omitted)

### 4. Key Decisions (주요 결정사항)

**Source**: "Key Decisions" section + conversation history

**Extraction process**:
1. Scan "Key Decisions" section
2. Identify **architecture-level** decisions (not implementation details)
3. Include brief rationale
4. Omit trivial choices

**Example extraction**:

Input ("Key Decisions" section):
> "- **에러 핸들러 위치**: 각 컨트롤러 메서드 내부에 중복 구현하는 대신 공통 유틸 함수로 분리. 일관성 유지 및 향후 수정 용이성을 위해.
>
> - **에러 응답 형식**: `{error: string, code: number, details?: any}` 구조로 표준화. 클라이언트가 에러를 파싱하기 쉽도록.
>
> - **인증 미들웨어 레벨**: 컨트롤러 레벨이 아닌 라우터 레벨에 적용. 각 메서드마다 호출할 필요 없고 실수 방지.
>
> - **변수명 컨벤션**: `err` 대신 `error` 사용. 가독성 향상.
>
> - **로깅 라이브러리**: Winston 대신 Pino 사용. 더 빠른 성능."

Output (key decisions):
```
- 에러 핸들러를 각 메서드 내부가 아닌 공통 유틸로 분리 - 일관성 유지 및 향후 수정 용이
```

**What was omitted**:
- 에러 응답 형식 (implementation detail, discoverable from code)
- 인증 미들웨어 레벨 (good practice, not controversial)
- 변수명 컨벤션 (trivial)
- 로깅 라이브러리 (peripheral to main task)

**Rules**:
- 1-2 decisions maximum
- Include **only** if:
  - Non-obvious choice (multiple valid approaches existed)
  - Affects future implementation significantly
  - Reversal would require major refactoring
- Include **brief rationale** (not full justification)
- **Omit section entirely** if no critical decisions

**Decision significance test**:
- **Include**: "Should we use REST or GraphQL?" (architecture-level)
- **Include**: "Should middleware be at router or controller level?" (affects scalability)
- **Exclude**: "Should we use `err` or `error`?" (trivial)
- **Exclude**: "Should we add error handling?" (obvious)

### 5. Essential Files (필요한 파일)

**Source**: Conversation history (files read/edited) + "What We Did"

**Extraction process**:
1. List all files **directly involved** in the work
2. Prioritize files user will **edit** or **reference**
3. Omit files that can be found via IDE search
4. Add brief purpose description

**Example extraction**:

Input (files from conversation):
- Read: `src/controllers/UserController.ts`, `src/controllers/PostController.ts`, `src/utils/logger.ts`, `src/types/api.ts`, `package.json`, `tsconfig.json`, `src/middleware/auth.ts`
- Edited: `src/utils/errorHandler.ts`, `src/middleware/auth.ts`, `src/controllers/UserController.ts`, `src/types/api.ts`

Output (essential files):
```
- `src/controllers/UserController.ts` - 리팩토링 완료된 참조 패턴
- `src/controllers/PostController.ts` - 다음 작업 대상
- `src/utils/errorHandler.ts` - 공통 에러 핸들러
- `src/middleware/auth.ts` - 인증 미들웨어
```

**What was omitted**:
- `src/types/api.ts` (user can find via IDE if needed)
- `package.json`, `tsconfig.json` (not directly relevant to tasks)
- `src/utils/logger.ts` (not part of next tasks)

**Rules**:
- 3-5 files maximum
- Prioritize:
  1. Files user will **edit next** (highest priority)
  2. Files user will **reference as examples**
  3. Files with **new functionality** created this session
- Add purpose: "다음 작업 대상", "참조 패턴", "공통 유틸"
- Use **absolute paths** (not relative)
- Omit config files unless directly relevant

**Prioritization heuristic**:
1. Next immediate task files (will edit)
2. Reference/pattern files (will read)
3. New abstractions created this session (might not know they exist)
4. Config/setup files (lowest - only if critical)

## Extraction Workflow

**Step-by-step process**:

1. **Read the session file** generated by session-journal
2. **Scan these sections** in order:
   - Title → extract work goal
   - Summary → enrich work goal
   - What We Did → extract completed work
   - Next Steps → extract remaining tasks
   - Key Decisions → filter for critical decisions
   - Conversation history (implicit) → identify files involved
3. **Apply filters**:
   - Completed work: Keep top 3-5 milestones
   - Remaining tasks: Keep top 3-5 priorities
   - Key decisions: Keep 1-2 critical, omit rest
   - Essential files: Keep 3-5 most relevant
4. **Validate extraction**:
   - Total word count: 150-300 words (excluding first task expansion)
   - Each item is **specific** and **actionable**
   - No code snippets, no detailed explanations
   - No obvious information user already knows
5. **Generate handoff message** using `handoff_format.md` template

## Common Extraction Mistakes

### ❌ Including Too Much Detail

**Bad**:
```
### 완료된 작업
- ✅ 에러 핸들러를 다음과 같이 구현했습니다. 먼저 에러 타입을 체크하고,
  ValidationError면 400 상태코드를, DatabaseError면 500을 반환합니다.
  각 에러마다 적절한 메시지를 포함하며...
```

**Good**:
```
### 완료된 작업
- ✅ 공통 에러 핸들러 `handleApiError()` 구현 (`src/utils/errorHandler.ts`)
```

### ❌ Vague Task Descriptions

**Bad**:
```
### 다음 작업
- [ ] 나머지 컨트롤러들 수정
```

**Good**:
```
### 다음 작업
- [ ] `PostController`에 에러 핸들러 적용 (5개 메서드)
```

### ❌ Including Trivial Decisions

**Bad**:
```
### 주요 결정사항
- 변수명을 `err`에서 `error`로 변경
- async/await 사용
- 들여쓰기 2칸 유지
```

**Good**:
```
### 주요 결정사항
(section omitted - no critical decisions)
```

### ❌ Too Many Files

**Bad**:
```
### 필요한 파일
- src/controllers/UserController.ts
- src/controllers/PostController.ts
- src/controllers/CommentController.ts
- src/controllers/AdminController.ts
- src/utils/errorHandler.ts
- src/utils/logger.ts
- src/middleware/auth.ts
- src/types/api.ts
- src/types/user.ts
- tests/integration/api.test.ts
```

**Good**:
```
### 필요한 파일
- `src/controllers/UserController.ts` - 리팩토링 완료된 참조 패턴
- `src/controllers/PostController.ts` - 다음 작업 대상
- `src/utils/errorHandler.ts` - 공통 에러 핸들러
```

## Edge Cases

### Session with Many Small Tasks

If "What We Did" has 15+ small items:
- **Group** related tasks: "5개 컴포넌트 리팩토링" instead of listing each
- **Highlight** most significant milestones
- **Omit** trivial tasks (typo fixes, formatting, etc.)

### Session with One Large Task

If only one major task was completed:
- Break it into **logical sub-components** for completed work
- Example: "사용자 인증 시스템 구현" →
  - ✅ JWT 토큰 발급/검증 로직
  - ✅ 로그인/로그아웃 API 엔드포인트
  - ✅ 인증 상태 관리 컨텍스트

### Session with No Clear Next Steps

If "Next Steps" section is empty or vague:
- **Infer** from work goal what logically comes next
- **Ask user** if unclear (before generating handoff)
- **Provide general guidance**: "다음 세션에서 작업 범위를 결정하세요"

### Session with Critical Bug Fix

If session was about urgent bug fixing:
- **Prioritize** root cause and fix in completed work
- **Include decision** if workaround vs proper fix was chosen
- **Next task**: Verification, adding tests to prevent regression

## Quality Checklist

Before finalizing extraction:

- [ ] Work goal is 20-40 words and includes **what** and **why**
- [ ] Completed work has 3-5 items, each a **discrete milestone**
- [ ] Remaining tasks has 3-5 items, **ordered by priority**
- [ ] Key decisions includes 0-2 items, **only critical choices**
- [ ] Essential files has 3-5 items with **purpose descriptions**
- [ ] Total extraction is 150-300 words
- [ ] No code snippets, no detailed explanations
- [ ] All file paths are **absolute** (not relative)
- [ ] All items are **specific** and **actionable**

## Integration with Handoff Format

After extraction, use `handoff_format.md` to:
1. Structure extracted components into the standard template
2. Add session file reference
3. Expand first task with additional context
4. Validate final message length (250-400 words total)
