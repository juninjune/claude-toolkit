# Commit Guidelines

This reference provides guidelines for analyzing git changes and creating logical, well-structured commits.

## Commit Message Format

Use Conventional Commits format with Korean descriptions:

```
<type>(<scope>): <description in Korean>

<optional body in Korean>
```

### Types

- **feat**: 새로운 기능 추가
- **fix**: 버그 수정
- **docs**: 문서 변경
- **refactor**: 코드 리팩토링 (기능 변경 없음)
- **test**: 테스트 추가 또는 수정
- **chore**: 빌드, 설정 파일 변경
- **style**: 코드 스타일 변경 (formatting, 세미콜론 등)
- **perf**: 성능 개선

### Scope

The scope should represent the main area or feature affected. Examples:
- `ocr`: OCR 관련 기능
- `pdf-viewer`: PDF 뷰어 관련
- `ui`: UI 컴포넌트
- `config`: 설정 파일
- `docs`: 문서
- `journal`: 개발 저널

## Commit Grouping Strategy

### Primary Grouping Principles

1. **Issue/Feature Cohesion**: Changes related to the same issue or feature should be grouped together, even if they span multiple file types (code + docs).

2. **Logical Atomicity**: Each commit should represent one logical change that:
   - Has a clear purpose
   - Could be reverted independently
   - Passes tests (if applicable)

3. **File Type Separation (Secondary)**: Only separate by file type (docs, code, config) when changes are NOT closely related to the same issue.

### Grouping Decision Tree

```
For each set of changes:
1. Is there a clear feature/issue that these changes address together?
   YES → Group them in one commit (even if mixed file types)
   NO → Continue to #2

2. Are these changes in the same category?
   - Documentation only → Group as docs commit
   - Code changes only → Group by feature/module
   - Configuration only → Group as config commit
   - Mixed with no clear connection → Separate by type

3. Would separating these changes make the history harder to understand?
   YES → Keep them together
   NO → Separate them
```

### Examples of Good Grouping

**Example 1: Feature with Mixed Files**
```
feat(ocr): 해상도 최적화 로직 구현

- PDF를 고해상도(300 DPI)로 렌더링하도록 개선
- OCR 성능 테스트 결과를 문서에 기록
- 개발 저널에 최적화 과정 추가

Files: lib/screens/text_extraction_test.dart, .dev-journal/20251109_0111_ocr-resolution-optimization.md
```

**Example 2: Documentation Update**
```
docs(journal): OCR 구현 과정 정리

- 바운딩 박스 시각화 과정 문서화
- 이슈 해결 과정 및 결과 추가

Files: .dev-journal/20251108_0620_ocr-bounding-box-visualization.md, .dev-journal/README.md
```

**Example 3: Configuration Changes**
```
chore(config): Claude Code 설정 업데이트

Files: .claude/settings.local.json
```

## Commit Message Body Guidelines

### Writing Style
- Write for junior developers who need to understand the context
- Explain the "why" and "what", not just the "what"
- Use 2-4 sentences for meaningful changes
- Include problem context and solution approach
- Avoid excessive detail

### Good Body Example
```
feat(ocr): 한글 텍스트 인식 폴백 로직 추가

PDF에서 텍스트 추출 시 한글 비율이 10% 미만이면
garbled text로 판단하고 자동으로 OCR을 시도합니다.
iOS/Android에서만 Google ML Kit을 사용하여
이미지 기반 텍스트 인식을 수행합니다.
```

### Avoid
- Too brief: "fix bug" ❌
- Too verbose: Step-by-step implementation details ❌
- Redundant: Repeating what's obvious from the diff ❌

## Special Cases

### Journal Files
- Multiple journal files related to the same work session can be grouped
- Separate journal updates from code if they document different phases
- Use `docs(journal):` scope consistently

### Test Files
- Group tests with the feature they test
- Use `feat(scope):` if the test is part of new functionality
- Use `test(scope):` only for standalone test improvements

### Configuration Files
- Small config changes related to a feature can be included in the feature commit
- Large or unrelated config changes should be separate `chore(config):` commits
