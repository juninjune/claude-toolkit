# 0001 - Integrate decision-tracker with session-journal for Automatic Invocation

**Status**: Accepted
**Date**: 2025-11-09
**Decision Makers**: Claude Code + User
**Tags**: architecture, skill-integration, automation

## Context

이전 세션(20251109_0434)에서 세션간 컨텍스트 유지를 위한 6개 스킬 아이디어를 도출했고, 초기 우선순위는 session-recall이었음. 하지만 실제 사용을 고려했을 때, 사용자가 정확한 키워드를 기억하지 못하는 문제가 있었고, 프로젝트에서 발생하는 "굵직한 이슈"를 트래킹하는 것이 더 근본적으로 중요하다는 것을 발견함.

session-journal은 모든 작업 세션을 기록하지만, 중요한 결정사항이나 critical issue가 일반 세션 문서에 묻혀버리는 문제가 있었음. 중요한 결정은 별도로 추적하고 쉽게 조회할 수 있어야 장기적인 컨텍스트 유지가 가능함.

## Decision

**decision-tracker 스킬을 session-journal과 자동 통합하는 구조로 구현**

- session-journal이 세션 리뷰 중에 중요한 결정이나 이슈를 감지하면 자동으로 decision-tracker를 호출
- 사용자는 "세션 리뷰해"만 하면 되고, 중요한 결정은 자동으로 `.dev-decisions/`에 ADR/Issue 문서로 승격
- session 문서와 decision 문서는 양방향 링크로 연결

## Alternatives Considered

- **Option A: session-recall을 먼저 구현** - 즉시 유용하지만, 근본적인 문제(중요 결정 추적)를 해결하지 못함. 또한 정확한 키워드 기억 필요.

- **Option B: decision-tracker를 수동 호출만 지원** - 사용자가 "이 결정 기록해줘"라고 명시적으로 요청해야 함. 중요한 결정을 놓칠 가능성이 높고, 사용자 부담 증가.

- **Option C: session-recall에 우선순위 필터 추가** - 빠르게 구현 가능하지만, session 문서와 decision이 분리되지 않아 장기적으로 관리가 어려움.

## Consequences

### Positive

- 사용자는 "세션 리뷰해"만 하면 되고, 중요한 결정은 자동으로 별도 추적됨
- 중요한 결정이 세션 문서에 묻히지 않고 `.dev-decisions/`에서 쉽게 조회 가능
- ADR (Architecture Decision Record) 표준 형식 사용으로 체계적 관리
- session-journal과 decision-tracker가 상호 보완적으로 작동 (일상 작업 vs 중요 결정)
- 양방향 링크로 맥락 추적 가능

### Negative

- session-journal의 복잡도 증가 (detection 로직 추가)
- 자동 감지가 완벽하지 않을 수 있음 (false positive/negative)
- 두 스킬 간 의존성 발생

## Implementation Notes

**session-journal SKILL.md 수정사항:**
- Step 3에 "Detect Significant Decisions/Issues" 단계 추가
- Detection 기준: 기술적 결정, 아키텍처 변경, critical issue, 정책 결정
- Detection signals: 키워드 패턴 (결정, 선택, 채택, critical, 3일 등)
- Step 6의 "Key Decisions" 섹션에 ADR 링크 추가 로직

**decision-tracker 구성요소:**
- `references/adr_template.md`: ADR 표준 템플릿
- `references/issue_template.md`: Critical issue 템플릿
- `references/readme_template.md`: .dev-decisions/README.md 초기화
- SKILL.md: 자동 호출 workflow 및 수동 조회 기능

**디렉토리 구조:**
```
.dev-decisions/        # Decision documents (milestone)
  ├── README.md
  └── NNNN-slug.md
.dev-journal/          # Session documents (daily work)
  ├── README.md
  └── YYYYMMDD_HHMM_slug.md
```

## Related Sessions

- [20251109_0434](../.dev-journal/20251109_0434_context-retention-planning.md) - 세션간 컨텍스트 유지를 위한 스킬 확장 계획
- [20251109_0447](../.dev-journal/20251109_0447_decision-tracker-implementation.md) - decision-tracker 스킬 구현

## Related Decisions

(첫 번째 ADR)
