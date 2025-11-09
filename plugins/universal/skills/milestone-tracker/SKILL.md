---
name: milestone-tracker
description: Track project milestones and goals in .dev-docs/MILESTONES.md with structured progress tracking. Use when user mentions milestones ("마일스톤 추가", "마일스톤 업데이트", "마일스톤 완료", "milestone") or during session reviews when significant progress toward a goal is detected. Supports both manual milestone management and auto-detection from session-journal. Creates bidirectional links with sessions and ADRs. Maintains milestone status, subtasks, and completion tracking in Korean format.
---

# Milestone Tracker

## 개요

Milestone Tracker는 `.dev-docs/MILESTONES.md` 파일에서 프로젝트 마일스톤을 중앙집중식으로 관리하며, 개발 세션 전반에 걸친 구조화된 진행 상황 추적을 제공합니다. 이 스킬은 상태 표시, 하위 작업, 관련 세션/ADR, 기술적 성과를 통해 마일스톤을 체계화하여 프로젝트 진행 상황과 목표 달성을 명확하게 시각화합니다.

## 사용 시기

**수동 트리거** (사용자 명시적 요청):
- "마일스톤 추가해줘" / "마일스톤 생성"
- "마일스톤 업데이트" / "마일스톤 수정"
- "마일스톤 완료 처리" / "마일스톤 완료"
- "마일스톤 상태 변경"

**자동 트리거** (session-journal에서):
- 세션 리뷰 중 중요한 기능 완료 감지
- 주요 기술 마일스톤 달성
- 프로젝트 로드맵에 영향을 주는 중요한 결정
- 명시된 목표에 대한 상당한 진전

## 워크플로우

### 1. MILESTONES.md 초기화

**.dev-docs/MILESTONES.md 존재 여부 확인:**

```bash
if [ -f .dev-docs/MILESTONES.md ]; then
  echo "MILESTONES.md exists"
else
  echo "MILESTONES.md does not exist"
fi
```

**파일이 존재하지 않는 경우:**
1. 필요시 `.dev-docs/` 디렉토리 생성: `mkdir -p .dev-docs`
2. Read 도구로 `references/milestone_template.md` 로드
3. 대화 컨텍스트에서 프로젝트별 정보로 템플릿 조정
4. Write 도구를 사용하여 초기화된 MILESTONES.md 작성

**파일이 존재하는 경우:**
1. Read 도구로 현재 MILESTONES.md 로드
2. 기존 구조 및 마일스톤 번호 파싱

### 2. 마일스톤 작업 결정

**사용자 의도에 따라 다음 중 하나 수행:**

#### A. 새 마일스톤 추가
1. 기존 마일스톤 분석하여 다음 마일스톤 번호 결정
2. 사용자에게 마일스톤 세부사항 질문:
   - 제목 및 목표 설명
   - 상태 (PLANNED, NEXT, IN PROGRESS)
   - 예상 시작일
   - 주요 기능 또는 하위 작업
3. Read 도구로 `references/milestone_entry_template.md` 로드
4. 제공된 정보로 템플릿 채우기
5. MILESTONES.md의 적절한 위치에 삽입
6. 양방향 링크 업데이트 (4단계 참조)

#### B. 기존 마일스톤 업데이트
1. 번호 또는 제목으로 마일스톤 식별
2. 업데이트할 내용 결정:
   - 하위 작업 추가/체크
   - 상태 업데이트
   - 관련 세션/ADR 추가
   - 기술적 성과 추가
   - 핵심 의사결정 업데이트
3. Edit 도구로 특정 섹션 수정
4. 새 세션/ADR 추가 시 양방향 링크 업데이트

#### C. 마일스톤 완료 처리
1. 번호 또는 제목으로 마일스톤 식별
2. 상태 아이콘을 `✅ COMPLETED`로 업데이트
3. 완료일 추가: `**완료일**: YYYY-MM-DD`
4. 모든 하위 작업이 체크되었는지 확인 (그렇지 않으면 사용자에게 의도 확인)
5. 완료 통계 계산 (선택사항):
   - 관련 세션 수
   - 관련 ADR 수
   - 소요 기간 (시작일부터 완료일까지)

#### D. 마일스톤 상태 변경
1. 마일스톤 식별
2. 상태 라벨 및 아이콘 업데이트:
   - `🎯 ... ✅ COMPLETED` - 마일스톤 완전히 달성
   - `🎯 ... (IN PROGRESS)` - 현재 작업 중
   - `🚀 ... (NEXT)` - 다음 시작 예정
   - `📋 ... (PLANNED)` - 향후 작업
   - `⏸️ ... (DEFERRED)` - 연기됨
3. 적절하게 날짜 필드 추가/업데이트

### 3. 세션 리뷰에서 자동 감지

**다음 경우 session-journal에 의해 호출됨:**
- 대화에 중요한 기능 완료 키워드 포함
- 기술적 마일스톤이 명시적으로 논의됨
- 사용자가 목표 달성 또는 단계 완료 언급

**프로세스:**
1. session-journal로부터 세션에 대한 컨텍스트 수신
2. MILESTONES.md 존재 여부 확인 및 로드
3. 세션이 기존 마일스톤의 진전인지 새로운 마일스톤인지 분석
4. 사용자에게 마일스톤 업데이트 제안:
   - "이 세션은 [Milestone N]에 상당한 진전을 보여줍니다. 업데이트할까요?"
   - 또는 "이 세션은 [목표]를 달성했습니다. 새 마일스톤 항목을 생성할까요?"
5. 사용자 확인에 따라 업데이트 또는 생성 진행
6. 양방향 링크를 위해 session-journal에 마일스톤 정보 반환

### 4. 양방향 교차 링크

**마일스톤으로의 링크 (다른 문서에서):**

**세션 문서에서** (`.dev-docs/sessions/YYYYMMDD_HHMM_topic.md`):
```markdown
## 관련 마일스톤
- [Milestone N: 제목](../MILESTONES.md#milestone-n-제목) - 관련성 간단 설명
```

**ADR 문서에서** (`.dev-docs/adr/NNNN-slug.md`):
```markdown
## 관련 마일스톤
- [Milestone N: 제목](../MILESTONES.md#milestone-n-제목) - 관련성 간단 설명
```

**마일스톤으로부터의 링크 (MILESTONES.md 내):**

각 마일스톤 섹션 내:
```markdown
- **관련 세션**: [YYYYMMDD_HHMM_topic](./sessions/YYYYMMDD_HHMM_topic.md)
- **관련 결정**: [ADR-NNNN: 제목](./adr/NNNN-slug.md)
```

**업데이트 프로세스:**
1. 마일스톤에 세션/ADR 링크 추가 시:
   - MILESTONES.md에 전방향 링크 추가
   - Edit 도구로 세션/ADR 문서에 역방향 링크 추가
2. session-journal 또는 decision-tracker가 이 스킬 호출 시:
   - 호출자로부터 문서 경로 수신
   - MILESTONES.md에 링크 추가
   - 역방향 링크를 위해 호출자에게 마일스톤 앵커 정보 반환

### 5. 상태 관리

**상태 생명주기 및 전환:**

```
PLANNED → NEXT → IN PROGRESS → COMPLETED
           ↓           ↓
        DEFERRED ← DEFERRED
```

**상태 표시:**
- `✅ COMPLETED` - 모든 목표 달성, 완료일 기록됨
- `(IN PROGRESS)` - 활발히 개발 중, 시작일 있음
- `(NEXT)` - 즉시 작업 대기 중, 시작일 또는 "TBD"
- `(PLANNED)` - 향후 작업, 일반적으로 "시작 예정: TBD"
- `(DEFERRED)` - 연기됨, 설명에 이유 기록

**상태 업데이트 시:**
1. 상태 텍스트 및 아이콘 변경
2. 날짜 필드 적절히 업데이트
3. 완료 표시 시 하위 작업 모두 체크되었는지 확인
4. 연기 시 선택적으로 이유에 대한 메모 추가

### 6. 진행 상황 추적

**하위 작업 완료:**
- 마크다운 체크박스 문법 사용: `- [ ]` 또는 `- [x]`
- 완료 비율 계산: (체크된 작업 / 전체 작업) × 100
- 마일스톤 헤더에 진행률 표시 (선택 기능)

**관련 산출물 추적:**
- 관련 세션 수 계산 및 나열
- 관련 ADR 수 계산 및 나열
- 파일 변경 추적 (git 또는 수동 입력)

### 7. 한국어 형식

**다음 규칙 준수:**
- 마일스톤 제목 및 설명은 한국어로
- 섹션 헤더는 한국어로: "주요 기능", "기술적 성과", "핵심 의사결정", "참고 자료"
- 날짜 형식: YYYY-MM-DD
- 상태 라벨은 한국어 또는 영어 (둘 다 허용)
- 기술 용어 및 파일 경로는 영어로

**마일스톤 헤더 예시:**
```markdown
## 🎯 Milestone 1: 텍스트 추출 파이프라인 구축 ✅ COMPLETED

**목표**: PDF에서 고품질 텍스트를 정확하게 추출하는 완전한 파이프라인 구축

**시작일**: 2025-11-09
**완료일**: 2025-11-09
```

## 다른 스킬과의 통합

### session-journal과의 통합

**session-journal이 마일스톤 진행 감지 시:**
1. session-journal이 마일스톤 관련 내용에 대해 대화 분석
2. Skill 도구를 사용하여 milestone-tracker 호출: `Skill(skill: "milestone-tracker")`
3. milestone-tracker가 세션 컨텍스트 및 타임스탬프 수신
4. 사용자에게 마일스톤 업데이트 제안
5. session-journal에 마일스톤 정보 (번호, 제목, 앵커) 반환
6. session-journal이 세션 문서에 "관련 마일스톤" 섹션 추가

**감지 기준 (session-journal이 사용):**
- 키워드: "마일스톤", "목표 달성", "완료", "milestone", "goal", "achievement"
- 기능 완료 문구: "기능 구현 완료", "파이프라인 완성", "시스템 통합"
- 단계 전환: "다음 단계", "새로운 단계", "준비 완료"

### decision-tracker와의 통합

**마일스톤 관련 의사결정:**
- decision-tracker가 프로젝트 로드맵에 영향을 주는 ADR 생성 시
- milestone-tracker가 해당 의사결정을 관련 마일스톤에 연결하도록 호출될 수 있음
- 양방향 링크는 의사결정 컨텍스트가 마일스톤 진행과 함께 보존되도록 보장

## 리소스

### references/

**`milestone_template.md`**: MILESTONES.md가 존재하지 않을 때 초기화하기 위한 전체 템플릿. Read 도구로 로드하고 프로젝트 컨텍스트에 따라 조정.

**`milestone_entry_template.md`**: 새 마일스톤 추가 시 개별 마일스톤 항목 템플릿. Read 도구로 로드하고 사용자가 제공한 세부사항으로 채우기.

**참고:** 이 참조 파일들은 일관된 구조와 형식을 제공합니다. 프로젝트 간 일관성을 유지하기 위해 처음부터 구조를 생성하지 말고 항상 이 파일들을 로드하세요.
