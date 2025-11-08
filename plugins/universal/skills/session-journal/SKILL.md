---
name: session-journal
description: Automatic session documentation system for Claude Code workflows. Use when the user says "세션 리뷰", "세션 리뷰해", "세션 정리", "작업 내용 문서화", or similar requests to document the current session. Creates timestamped markdown files in .dev-docs/sessions/ with automatic keyword extraction, related session linking, and maintains a searchable index. Automatically invokes decision-tracker skill when significant decisions or critical issues are detected. Prevents CLAUDE.md bloat while preserving cross-session context.
---

# Session Journal

## Overview

Automate session documentation to maintain context across Claude Code sessions without bloating CLAUDE.md. Each session is captured as a timestamped markdown file with keywords, summaries, and automatic cross-linking to related sessions.

## Workflow

### 1. Trigger Detection

Watch for these phrases:
- "세션 리뷰해" / "세션 리뷰"
- "세션 정리"  
- "작업 내용 문서화"
- "session review"

### 2. Keyword Extraction

Analyze the conversation directly and extract 3-8 contextual keywords. **No external scripts needed** - Claude understands context better than NLP algorithms.

**Process**:
1. Read `.dev-docs/sessions/README.md` to load existing keywords and their usage counts
2. Analyze the conversation to identify session topics:
   - **Features**: `ocr-resolution-optimization`, `pdf-viewer-performance`, `subtitle-sync`
   - **Issues**: `impeller-memory-error`, `korean-text-garbled`, `scroll-bug`
   - **Modules**: `text-extraction-test`, `viewer-test`, `pdf-service`
   - **Domain**: `mlkit-text-recognition`, `bounding-box-visualization`, `theater-ops`
3. Prefer existing keywords (especially 3+ occurrences) for consistency
4. Create new keywords only when necessary to describe new topics
5. User-provided keywords are always included and take priority

**If user provides keywords**: "세션 리뷰해 [keyword1, keyword2]"
- Use both auto-extracted AND user-provided keywords
- User keywords take priority

**If user just says "세션 리뷰해"**:
- Auto-extract only
- Do NOT prompt - just proceed

**Keyword format**:
- Lowercase, hyphenated: `ocr-resolution-testing`
- Specific and descriptive
- Can be Korean or English

**Keyword types to AVOID**:
- Generic tech stack (Flutter, React, Python, etc.) - these are project-wide constants
- Project name - one repo = one project
- Too generic terms (bug, feature, fix) without context
- File extensions or paths without context

### 3. Detect Significant Decisions/Issues

**BEFORE generating session document**, analyze the conversation to detect significant decisions or critical issues that should be elevated to decision-tracker.

**Detection criteria:**

1. **Technical Decisions**
   - Library/framework selection (e.g., "chose Riverpod over GetX")
   - Design pattern adoption (e.g., "switching to Repository pattern")
   - Database/architecture choices

2. **Architecture Changes**
   - System structure modifications (e.g., "moving to microservices")
   - Module separation/integration
   - API design changes (e.g., "migrating to GraphQL")

3. **Critical Issues**
   - Bugs requiring 3+ days to resolve
   - System-wide impact issues
   - Performance/security critical problems

4. **Policy/Convention Decisions**
   - Coding style guides
   - Branch strategies
   - Deployment strategies

**Detection signals:**
- Keywords: "결정", "선택", "채택", "decided", "chose", "adopted"
- Issue severity: "critical", "버그", "3일", "시스템 전체"
- Architecture terms: "아키텍처 변경", "마이그레이션", "리팩토링"

**If detected, invoke decision-tracker:**
1. Use the Skill tool to invoke decision-tracker
2. decision-tracker will create ADR or Issue document
3. decision-tracker will return the document path and number
4. Store this info to add cross-link in session document later

**If not detected:**
- Continue to next step normally

### 4. Initialize Journal Structure

If `.dev-docs/sessions/` doesn't exist:
```bash
mkdir -p .dev-docs/sessions
```

If `README.md` doesn't exist, create it using `references/readme_template.md`.

### 5. Find Related Sessions

Use `scripts/find_related_sessions.py` to find sessions with overlapping keywords:
```bash
python3 scripts/find_related_sessions.py .dev-docs/sessions "keyword1,keyword2,keyword3"
```

For each result:
- Read the session file's Summary, Context, and Next Steps sections
- Determine if truly related based on semantic analysis
- If related: add to cross-linking list

### 6. Generate Session Document

Create filename: `YYYYMMDD_HHMM_topic-slug.md`

**Filename format**:
- Timestamp: `YYYYMMDD_HHMM` (e.g., `20251108_1430`)
- Slug: Generated from session topic (lowercase, hyphens, max 50 chars)

Use template from `references/session_template.md` and populate:
- **Date**: Full datetime
- **Keywords**: Comma-separated list
- **Related Sessions**: Links to related session files
- **Summary**: One-line accomplishment summary
- **Context**: Background and motivation
- **What We Did**: Bullet list of main tasks
- **Key Decisions**: Important choices made
  - **If decision-tracker was invoked**: Add cross-link to ADR/Issue document here
    ```markdown
    ## Key Decisions
    - [Decision description]
      - **Decision**: [ADR-XXXX: Title](../adr/XXXX-slug.md)
    ```
- **Code Snippets**: Relevant code examples (optional)
- **Next Steps**: Follow-up tasks (optional)
- **References**: External links/files (optional)

### 7. Update Cross-Links

For each related session file:
```markdown
## Related Sessions
- [Current session title](./YYYYMMDD_HHMM_current-slug.md)
```

Add bidirectional links - both in the new session AND in related session files.

### 8. Update README.md

Add entry in reverse chronological order:
```markdown
## Sessions

- [YYYYMMDD_HHMM](./YYYYMMDD_HHMM_topic-slug.md) - keyword1, keyword2, keyword3 | One-line summary
```

Update keywords index with occurrence counts:
```markdown
## Keywords Index

### subtitle-sync (5회)
- YYYYMMDD_HHMM_topic-slug
- YYYYMMDD_HHMM_other-topic

### pdf-viewer (3회)
- YYYYMMDD_HHMM_topic-slug

### scroll-bug (2회)
- YYYYMMDD_HHMM_topic-slug
```

**Keyword evolution rules**:
- Increment count for existing keywords
- Add new keywords with (1회)
- Keywords used 3+ times are "established" - prioritize matching these in future sessions
- Keywords used 1-2 times are "emerging" - may become irrelevant over time
- Consider removing keywords that haven't appeared in 10+ recent sessions

### 9. Optional: Update /memory

For sessions marking significant milestones, offer to update /memory with `--update-memory` flag:

**Criteria for /memory update**:
- New project started
- Major architecture decision
- Tool/technology preference established
- Workflow pattern adopted

**Example memory updates**:
- "User is working on [project]"
- "User prefers [pattern] for [use-case]"
- "User uses [tool] for [purpose]"

Only suggest memory update if the session contains genuinely memorable long-term facts.

### 10. Offer Commit Organization

After successfully creating the session document, check if there are uncommitted changes and offer to organize commits:

**Process**:
1. Run `git status --short` to check for uncommitted changes
2. If changes exist (including the newly created journal file):
   - Inform user: "세션 문서를 생성했습니다. 커밋을 정리할까요?"
   - Wait for user confirmation
   - If confirmed, use the Task tool to launch commit-agent

**Example**:
```
✅ 세션 문서를 생성했습니다: .dev-docs/sessions/20251109_1430_agent-skill-integration.md

현재 커밋되지 않은 변경사항이 있습니다. commit-agent를 실행해서 커밋을 정리할까요?
```

**Task tool invocation**:
```
Task tool:
- description: "Organize git commits"
- subagent_type: "general-purpose"
- prompt: "Use commit-agent to organize uncommitted changes. The agent will invoke smart-commit skill to analyze git diff and create logical commits with Korean Conventional Commits messages."
```

**Important**:
- Only offer if there are actual uncommitted changes
- Always wait for user confirmation before launching agent
- The agent operates independently and will handle the entire commit workflow
- Do not invoke smart-commit skill directly - let commit-agent handle it

## Session Analysis Guide

When writing the session document:

**Summary**: Answer "What did we accomplish?"
- Focus on outcomes, not process
- One clear sentence

**Context**: Answer "Why did we do this?"
- Problem we were solving
- What prompted this work

**What We Did**: Chronological task list
- Start with verbs (Created, Fixed, Refactored, Added)
- Focus on concrete actions

**Key Decisions**: Document WHY, not just WHAT
- Trade-offs considered
- Why this approach over alternatives
- Future implications

**Code Snippets**: Only include if
- Core logic that was tricky
- Pattern that will be reused
- Solution to non-obvious problem

**Next Steps**: Actionable and specific
- Use checkboxes `- [ ]` for clarity
- Include enough context for future self

## File Organization

```
/.dev-docs/sessions/
├── README.md                              # Index with all sessions
├── 20251108_1430_flutter-riverpod.md     # Session document
├── 20251108_1615_stagetext-pdf.md
└── ...
```

Keep all session files flat in `.dev-docs/sessions/` - no subdirectories.

## Resources

### scripts/find_related_sessions.py
Finds related sessions based on keyword overlap and semantic analysis of Summary/Context/Next Steps. Used in Step 4 of the workflow.

### references/session_template.md
Template structure for session documents.

### references/readme_template.md
Template for initializing README.md index file with keyword evolution tracking.
