# Repository Structure

이 저장소는 **이중 목적**을 가집니다:
1. **마켓플레이스**: GitHub에 배포되어 사용자가 설치하는 Claude Code 플러그인 카탈로그
2. **워크스페이스**: 플러그인을 개발하고 테스트하는 개발 환경

## 배포 vs 로컬 구분

### GitHub에 배포되는 내용 (Public)
```
claude-toolkit/
├── .claude-plugin/
│   └── marketplace.json          # 마켓플레이스 정의
├── plugins/
│   └── universal/
│       ├── .claude-plugin/
│       │   └── plugin.json       # 플러그인 매니페스트
│       └── skills/               # 스킬 정의
│           ├── smart-commit/
│           └── session-journal/
├── README.md                      # 마켓플레이스 사용 가이드
└── docs/
    └── claude-code-guide.md      # 참고 문서
```

### 로컬에만 존재 (Not in Git)
```
claude-toolkit/
├── .dev-journal/                  # 개발 세션 문서
├── .claude/                       # 로컬 Claude Code 설정
│   ├── settings.json
│   ├── commands/                  # 개발용 커맨드
│   ├── agents/                    # 개발용 에이전트
│   └── skills/                    # 개발용 스킬 (테스트)
├── workspace/                     # 플러그인 개발 작업 공간
│   ├── drafts/                    # 작업 중인 플러그인
│   ├── experiments/               # 실험적 기능
│   └── templates/                 # 재사용 템플릿
└── node_modules/                  # npm 의존성 (있다면)
```

## 폴더 역할

### 배포 폴더

#### `.claude-plugin/`
마켓플레이스 정의. 사용자가 `/plugin marketplace add` 할 때 읽는 파일.

#### `plugins/`
배포 준비된 플러그인들. 각 플러그인은:
- `.claude-plugin/plugin.json`: 플러그인 메타데이터
- `skills/`, `commands/`, `agents/` 등: 기능 컴포넌트

### 로컬 전용 폴더

#### `.dev-journal/`
이 저장소를 개발하면서 생성되는 세션 문서. 개발 과정 기록.

#### `.claude/`
이 저장소 자체를 개발할 때 사용하는 Claude Code 설정:
- 플러그인 개발을 돕는 커스텀 커맨드
- 개발 에이전트
- 테스트용 스킬

#### `workspace/`
새 플러그인을 만들거나 실험하는 작업 공간:
```
workspace/
├── drafts/
│   └── new-plugin/               # 작업 중인 플러그인
│       └── skills/
├── experiments/
│   └── mcp-test/                 # MCP 서버 실험
├── templates/
│   ├── skill-template/           # 스킬 템플릿
│   └── plugin-template/          # 플러그인 템플릿
└── docs/
    └── claude-code-guide.md      # 개발 참고 문서
```

플러그인이 완성되면 `workspace/drafts/` → `plugins/`로 이동.

## 개발 워크플로우

### 1. 새 플러그인 개발
```bash
# workspace/drafts/에서 작업
mkdir -p workspace/drafts/my-new-plugin

# 개발 및 테스트
...

# 완성되면 plugins/로 이동
mv workspace/drafts/my-new-plugin plugins/

# marketplace.json 업데이트
# git commit & push
```

### 2. 로컬 테스트
```bash
# 이 저장소를 로컬 마켓플레이스로 추가
/plugin marketplace add ./

# 플러그인 설치 테스트
/plugin install universal@jun-toolkit
```

### 3. 배포
```bash
# Git에는 plugins/, README, STRUCTURE.md만 포함
git add plugins/ README.md STRUCTURE.md .claude-plugin/
git commit -m "feat: add new plugin"
git push
```

## 주의사항

- **절대 커밋하지 말 것**:
  - `.dev-journal/`: 개인 개발 로그
  - `.claude/`: 로컬 개발 설정
  - `workspace/`: 작업 중인 미완성 코드, 개발 참고 자료
  - `.env`: 환경 변수 (있다면)

- **반드시 커밋할 것**:
  - `plugins/`: 배포할 플러그인
  - `.claude-plugin/marketplace.json`: 마켓플레이스 정의
  - `README.md`: 마켓플레이스 소개
  - `STRUCTURE.md`: 저장소 구조 설명

## 예시: 전체 디렉토리 트리

```
claude-toolkit/
├── .claude-plugin/
│   └── marketplace.json          ✅ Git
├── plugins/
│   ├── universal/                ✅ Git
│   └── flutter/                  ✅ Git (향후)
├── README.md                      ✅ Git
│
├── .dev-journal/                  ❌ Git (로컬)
├── .claude/                       ❌ Git (로컬)
├── workspace/                     ❌ Git (로컬)
│   ├── drafts/
│   ├── experiments/
│   ├── templates/
│   └── docs/                      # 개발 참고 자료
│       └── claude-code-guide.md
├── .gitignore                     ✅ Git
└── STRUCTURE.md                   ✅ Git (이 파일)
```
