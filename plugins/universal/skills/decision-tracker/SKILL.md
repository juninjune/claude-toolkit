---
name: decision-tracker
description: Track critical technical decisions, architecture changes, and major issues using ADR (Architecture Decision Record) format. Automatically invoked by session-journal when significant decisions or critical issues are detected during session review. Also supports manual queries like "이전에 [주제] 관련해서 무슨 결정 내렸지?" to recall past decisions.
---

# Decision Tracker

## Overview

Capture and track milestone decisions that shape the project's long-term direction. Unlike session-journal which logs all work sessions, decision-tracker focuses on **significant decisions, critical issues, and architecture changes** that require long-term visibility.

Decision documents are stored in `.dev-docs/adr/` using ADR (Architecture Decision Record) format, with automatic cross-linking to related sessions.

## When to Use

This skill is primarily **automatically invoked** by session-journal during session review. Manual invocation is rare but supported.

### Automatic Invocation (Primary)

session-journal automatically calls decision-tracker when detecting:

1. **Technical Decisions**
   - Library/framework selection (e.g., "Riverpod vs GetX → chose Riverpod")
   - Design pattern adoption (e.g., "switching to Repository pattern")
   - Database/architecture choices (e.g., "PostgreSQL vs MongoDB")

2. **Architecture Changes**
   - System structure modifications (e.g., "moving PDF rendering to server-side")
   - Module separation/integration
   - API design changes (e.g., "REST → GraphQL migration")

3. **Critical Issues**
   - Bugs requiring 3+ days to resolve
   - System-wide impact issues
   - Performance/security critical problems

4. **Policy/Convention Decisions**
   - Coding style guides
   - Branch strategies
   - Deployment strategies

### Manual Invocation (Rare)

Users may explicitly request decision tracking:
- "이 결정 기록해줘"
- "decision track"
- "ADR 만들어줘"

Or query past decisions:
- "이전에 상태관리 라이브러리 선택할 때 왜 Riverpod 골랐지?"
- "GraphQL 관련 결정 뭐였지?"

## Workflow

### 1. Detection (Automatic)

When session-journal analyzes a session and detects significant decisions or critical issues, it automatically invokes decision-tracker.

**Detection signals:**
- Keywords: "결정", "선택", "채택", "decided", "chose", "adopted"
- Issue severity: "critical", "버그", "3일", "시스템 전체"
- Architecture terms: "아키텍처 변경", "마이그레이션", "리팩토링"

### 2. Classification

Determine document type:
- **ADR**: For decisions (library choices, architecture, patterns)
- **Issue**: For critical problems and their resolutions

### 3. Initialize `.dev-docs/adr/` Structure

If `.dev-docs/adr/` doesn't exist:
```bash
mkdir -p .dev-docs/adr
```

If `README.md` doesn't exist, create it using `references/readme_template.md`.

### 4. Determine Next Number

Find the highest existing number in `.dev-docs/adr/`:
```bash
ls .dev-docs/adr/ | grep -E '^[0-9]{4}-' | sort -r | head -1
```

Increment by 1 (e.g., if highest is `0003-`, next is `0004-`).

### 5. Generate Document

#### For ADR (Decision)

Create filename: `NNNN-slug.md` (e.g., `0001-adopt-riverpod.md`)

Use template from `references/adr_template.md` and populate:
- **Number**: Zero-padded 4 digits
- **Title**: Clear, action-oriented (e.g., "Adopt Riverpod for State Management")
- **Status**:
  - `Proposed`: Under consideration
  - `Accepted`: Active decision
  - `Deprecated`: No longer recommended
  - `Superseded`: Replaced by another decision
- **Date**: Full date (YYYY-MM-DD)
- **Tags**: Relevant categories (architecture, library-choice, performance, etc.)
- **Context**: Why this decision was needed
- **Decision**: What was decided
- **Alternatives Considered**: Other options and why they were rejected
- **Consequences**: Positive and negative impacts
- **Implementation Notes**: Technical details for implementation
- **Related Sessions**: Links to session files discussing this decision
- **Related Decisions**: Links to other ADRs

#### For Issue (Critical Problem)

Create filename: `NNNN-slug.md` (e.g., `0002-impeller-memory-leak.md`)

Use template from `references/issue_template.md` and populate:
- **Number**: Zero-padded 4 digits
- **Title**: Problem-focused (e.g., "Impeller Memory Leak Issue")
- **Status**:
  - `Investigating`: Problem being analyzed
  - `Resolved`: Problem fixed
  - `Monitoring`: Fix deployed, observing
  - `Recurring`: Problem reappeared
- **Date**: Issue discovered date
- **Severity**: `Critical/High/Medium/Low`
- **Duration**: Time spent resolving
- **Tags**: Issue categories (bug, performance, security, etc.)
- **Problem Description**: Clear description of symptoms
- **Impact**: Affected functions, users, business impact
- **Root Cause**: Why the problem occurred
- **Investigation Timeline**: Chronological log of debugging attempts
- **Solution**: Final resolution
- **Prevention**: Measures to prevent recurrence
- **Lessons Learned**: Key takeaways
- **Related Sessions**: Links to session files
- **Related Decisions**: Links to ADRs
- **Related Issues**: Links to similar issues

### 6. Update Cross-Links

#### In Decision Document

Add link to the session that triggered this decision:
```markdown
## Related Sessions
- [20251109_0434](../sessions/20251109_0434_riverpod-setup.md) - Riverpod 초기 설정 및 테스트
```

#### In Session Document

Add link to the decision document in the session file's appropriate section:
```markdown
## Key Decisions
- Riverpod를 상태관리 라이브러리로 채택
  - **Decision**: [ADR-0001: Adopt Riverpod](../adr/0001-adopt-riverpod.md)
```

Create **bidirectional links** - both session → decision and decision → session.

### 7. Update README.md

Update `.dev-docs/adr/README.md` with:

#### Index by Status

Add to appropriate section:
```markdown
### Active Decisions
- [0001](./0001-adopt-riverpod.md) - Adopt Riverpod for State Management
```

#### Tag Index

Update tag groupings:
```markdown
## By Tag

### library-choice
- 0001-adopt-riverpod

### performance
- 0002-impeller-memory-leak
```

#### Timeline

Add to chronological list:
```markdown
## Timeline

- 2025-11-09: [0001](./0001-adopt-riverpod.md) - Adopt Riverpod
```

### 8. Return to session-journal

After creating the decision document, return control to session-journal to complete the session document creation.

## Querying Past Decisions

When users query past decisions:

1. **Parse Query**: Extract keywords from user request
2. **Search `.dev-docs/adr/`**: Use grep or file listing
3. **Read Relevant Documents**: Load decision documents
4. **Summarize**: Provide concise summary of:
   - What was decided
   - Why (context)
   - Trade-offs (consequences)
   - Current status
5. **Provide Links**: Give file paths for detailed reading

**Example query handling:**
```
User: "이전에 상태관리 선택할 때 왜 Riverpod 골랐지?"

1. Keywords: ["상태관리", "Riverpod", "선택"]
2. Search: grep -r "Riverpod" .dev-docs/adr/
3. Found: 0001-adopt-riverpod.md
4. Read and summarize:
   "Riverpod를 선택한 이유는 GetX에 비해 type-safe하고,
    compile-time 에러 감지가 가능하며, 테스트하기 쉽기 때문입니다.
    Trade-off는 초기 학습 곡선이 있다는 점입니다."
5. Link: .dev-docs/adr/0001-adopt-riverpod.md
```

## File Organization

```
/.dev-docs/adr/
├── README.md                              # Index by status, tags, timeline
├── 0001-adopt-riverpod.md                # ADR document
├── 0002-impeller-memory-leak.md          # Issue document
└── 0003-migrate-to-graphql.md            # Architecture change ADR
```

Keep all decision files flat in `.dev-docs/adr/` - no subdirectories.

## Decision Status Lifecycle

**For ADRs:**
- `Proposed` → `Accepted` (decision implemented)
- `Accepted` → `Deprecated` (no longer recommended, but not replaced)
- `Accepted` → `Superseded` (replaced by another ADR)

**For Issues:**
- `Investigating` → `Resolved` (problem fixed)
- `Resolved` → `Monitoring` (observing fix stability)
- `Monitoring` → `Resolved` (stable) or `Recurring` (problem returned)

When updating status, add a note at the end of the document explaining the status change and date.

## Integration with session-journal

session-journal's workflow includes a decision detection step:

```
User: "세션 리뷰해"
    ↓
session-journal: Analyze conversation
    ↓
[Detect significant decision/issue?]
    ↓
YES → Invoke decision-tracker
    → Create ADR/Issue document
    → Update cross-links
    → Continue session-journal
    ↓
NO  → Complete session document normally
```

This integration ensures important decisions are never lost in session documents and always elevated to dedicated ADR/Issue tracking.

## Resources

### references/adr_template.md
Standard ADR template following Architecture Decision Record format.

### references/issue_template.md
Template for documenting critical issues and their resolutions.

### references/readme_template.md
Template for initializing `.dev-docs/adr/README.md` with index structure.
