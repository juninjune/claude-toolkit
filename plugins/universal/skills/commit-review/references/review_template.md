# 커밋 리뷰: [기간 설명]

**Date**: YYYY-MM-DD HH:MM
**Commit Range**: `abc1234..def5678`
**Period**: YYYY-MM-DD ~ YYYY-MM-DD
**Commits Analyzed**: N개
**Previous Review**: [YYYYMMDD_HHMM](./YYYYMMDD_HHMM_review-slug.md) _(첫 리뷰인 경우 생략)_

---

## 요약

전체 기간 동안의 작업 개요를 1-2문장으로 요약합니다.

---

## 분석 메트릭스

### 커밋 통계
- **총 커밋 수**: N개
- **평균 커밋 크기**: N lines changed (±M additions, -K deletions)
- **가장 큰 커밋**: `abc1234` (N lines)
- **가장 작은 커밋**: `def5678` (N lines)

### 스코프 분포
| Type | Count | Percentage |
|------|-------|------------|
| feat | X | XX% |
| refactor | Y | YY% |
| fix | Z | ZZ% |
| docs | W | WW% |
| 기타 | V | VV% |

### 주요 변경 파일 (Top 5)
1. `path/to/file1.ts` - N commits, M lines changed
2. `path/to/file2.md` - N commits, M lines changed
3. `path/to/file3.py` - N commits, M lines changed
4. `path/to/file4.json` - N commits, M lines changed
5. `path/to/file5.sh` - N commits, M lines changed

---

## 리팩토링 기회

### 🔴 High Priority

#### HP-1: [제목]

**위치**: `file.ts:123-145`
**관련 커밋**: `abc1234`

**문제 유형**: YAGNI 위반 / 과도한 추상화 / 인지적 복잡도 증가 / 코드 스멜

**현재 상황**:
```typescript
// 문제가 되는 코드 예시
function exampleFunction() {
  // ...
}
```

**제안**:
[구체적인 리팩토링 방법 설명]

**근거**:
- [Google 리뷰 원칙 / YAGNI / 인지적 복잡도 / 기술 부채 연구 중 어떤 원칙에 근거하는지]
- [구체적인 위반 내용: 예: "인지적 복잡도 15 (권장: 10 이하)", "단일 구현만 있는 추상 인터페이스"]

**예상 효과**:
- 코드 라인 수 N줄 감소
- 인지적 복잡도 N → M로 감소
- 유지보수성 향상

---

### 🟡 Medium Priority

#### MP-1: [제목]

_(같은 형식)_

---

### 🟢 Low Priority

#### LP-1: [제목]

_(같은 형식)_

---

## 작업-문서 정합성

### 세션 일치도

#### ✅ [20251109_0656](../sessions/20251109_0656_slug.md): 완전 일치
- **세션에서 언급**: "session-journal에 milestone 통합"
- **실제 커밋**:
  - `abc1234` - feat(journal): milestone-tracker 통합
  - `def5678` - docs(journal): milestone 크로스 링크 문서화
- **평가**: 세션에 기록된 작업이 모두 커밋에 반영됨

#### ⚠️ [20251108_1430](../sessions/20251108_1430_slug.md): 부분 일치
- **세션에서 언급**: "decision-tracker 리팩토링 및 테스트 추가"
- **실제 커밋**:
  - `ghi9012` - refactor(decision): 템플릿 구조 개선
- **평가**: 리팩토링은 완료되었으나 "테스트 추가"는 커밋되지 않음
- **Next Steps 확인**: 세션의 "Next Steps"에 "테스트 작성" 항목이 남아있음 → 다음 리뷰에서 추적 필요

#### ❌ [20251107_0900](../sessions/20251107_0900_slug.md): 불일치
- **세션에서 언급**: "context-bridge 성능 최적화"
- **실제 커밋**: 해당 내용 없음
- **평가**: 세션에 기록된 작업이 커밋되지 않았거나, 다른 브랜치/작업 공간에서 진행 중일 가능성

---

### ADR 구현 추적

#### 🟢 [ADR-0001](../adr/0001-integrate-decision-tracker.md): 구현 완료
- **결정 내용**: "session-journal이 중요 결정을 감지하면 자동으로 decision-tracker 호출"
- **구현 커밋**:
  - `abc1234` - feat(journal): decision-tracker 자동 호출 로직 추가
  - `def5678` - test(journal): decision detection 테스트 추가
- **평가**: ADR에 명시된 결정이 완전히 구현됨

#### 🟡 [ADR-0002](../adr/0002-agent-only-smart-commit.md): 부분 구현
- **결정 내용**: "smart-commit을 [AGENT-ONLY]로 변경하여 메인 컨텍스트에서 직접 호출 방지"
- **구현 커밋**:
  - `ghi9012` - refactor(commit): smart-commit을 agent-only로 변경
- **평가**: 스킬 마크다운은 업데이트되었으나, 문서화 및 테스트는 아직 미완료

#### ⭕ [ADR-0003](../adr/0003-future-feature.md): 미구현
- **결정 내용**: "worktree 자동 정리 기능 추가"
- **평가**: 아직 구현되지 않음 (예정된 작업)

---

## 이전 리뷰 추적

_이전 리뷰가 없는 경우 이 섹션 생략_

### ✅ [이전 제안 HP-1]: 반영됨
- **제안 내용**: "session-journal의 keyword extraction 로직을 별도 함수로 분리"
- **반영 커밋**: `abc1234` - refactor(journal): keyword extraction 함수 분리
- **평가**: 제안이 완전히 반영되어 코드 가독성 향상

### ⭕ [이전 제안 MP-2]: 미반영
- **제안 내용**: "decision-tracker의 ADR 번호 생성 로직 간소화"
- **상태**: 아직 반영되지 않음
- **권장 사항**: Medium Priority이므로 다음 리팩토링 기회에 고려

---

## 코드 건강도 평가

### 전반적 평가

**✅ 코드 건강도 개선** / **➖ 코드 건강도 유지** / **⚠️ 코드 건강도 경고** / **❌ 코드 건강도 악화**

### 근거
- [구체적인 개선/악화 내용]
- 예: "session-journal 리팩토링으로 함수 평균 길이 80줄 → 45줄로 감소"
- 예: "새로 추가된 feature X가 과도한 추상화로 복잡도 증가"

### 추세 분석
- 총 코드 라인 수: 이전 대비 ±N% (증가/감소)
- 평균 함수 길이: 이전 대비 ±M줄
- 테스트 커버리지: 이전 대비 ±X% _(측정 가능한 경우)_

---

## 다음 리뷰 시 확인 사항

- [ ] HP-1: [제목] - 제안된 리팩토링이 반영되었는지
- [ ] HP-2: [제목] - 제안된 리팩토링이 반영되었는지
- [ ] MP-1: [제목] - 제안 고려 여부
- [ ] 세션 20251108_1430의 "테스트 추가" Next Step이 완료되었는지
- [ ] ADR-0002 구현이 완료되었는지
- [ ] 새로운 복잡도가 추가되지 않았는지
- [ ] 이전 리뷰의 미반영 제안들이 반영되었는지

---

## 관련 세션

- [20251109_0656](../sessions/20251109_0656_slug.md) - Session title
- [20251108_1430](../sessions/20251108_1430_slug.md) - Session title
- [20251107_0900](../sessions/20251107_0900_slug.md) - Session title

---

## 관련 ADR

- [ADR-0001](../adr/0001-slug.md) - ADR title
- [ADR-0002](../adr/0002-slug.md) - ADR title

---

## 관련 마일스톤

- [Milestone 1: Title](../MILESTONES.md#milestone-1-title)

---

## 메타데이터

**Keywords**: commit-review, refactoring, code-health, [추가 키워드]
**Review Duration**: N minutes _(분석에 소요된 시간)_
**Refactoring Proposals**: N개 (High: X, Medium: Y, Low: Z)
