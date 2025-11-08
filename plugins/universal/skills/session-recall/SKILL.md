---
name: session-recall
description: Retrieve and analyze past work sessions from .dev-docs/sessions/ based on contextual keywords, time ranges, or work continuity. Use when users ask about previous work ("이전에 [맥락] 관련해서...", "어제 뭐 했었지?", "오늘 뭐 하면 될까?"), need to find past sessions, or want to continue incomplete tasks. Performs intelligent keyword matching even when users don't remember exact terms.
---

# Session Recall

## Overview

Retrieve and analyze past work sessions from `.dev-docs/sessions/` to maintain context across Claude Code sessions. This skill enables finding relevant sessions through contextual keyword matching, time-based filtering, and work continuity analysis—even when users don't remember exact keywords.

## When to Use This Skill

Use session-recall when users ask about past work or need session context:

**Keyword-based queries** (with inexact/contextual keywords):
- "이전에 커밋 관련 작업 뭐 했었지?" (user says "커밋" → find `smart-commit`, `commit-agent` sessions)
- "[키워드] 작업했던 거 찾아줘"
- "스킬 만들 때 어떤 구조로 했었지?"

**Work continuity queries**:
- "어제 어디까지 작업했지?"
- "오늘 뭐 작업하면 될까?"
- "미완료 작업 뭐가 있지?"

**Time-based queries**:
- "지난주에 뭐 했었지?"
- "최근에 작업한 내용 보여줘"

**DO NOT use this skill for**:
- Creating new session documents (use session-journal skill)
- Tracking decisions/ADRs (use decision-tracker skill)
- Unrelated searches (use Grep or other tools)

## Core Workflow

### 1. Identify Query Type

Analyze the user's request to determine the search strategy:

| Query Pattern | Search Type | Example |
|---------------|-------------|---------|
| "이전에 [맥락]..." / "[맥락] 작업했던..." | Keyword-based | "커밋 관련 작업 뭐 했었지?" |
| "어제/지난주..." / "[기간]에 뭐..." | Time-based | "지난주에 뭐 했었지?" |
| "어디까지 작업했지?" / "오늘 뭐 하면..." | Continuation | "오늘 뭐 작업하면 될까?" |

### 2. Execute Search Strategy

#### A. Keyword-Based Search (Contextual Matching)

The most common use case. Users often provide inexact or contextual keywords.

**Process**:

1. **Extract contextual terms** from user query:
   - "커밋 관련 작업" → extract: `커밋`, `작업`
   - "스킬 만들 때" → extract: `스킬`, `만들다`

2. **Expand to related keywords** using domain knowledge:
   ```
   "커밋" → [commit, git, smart-commit, commit-agent, version-control]
   "스킬" → [skill, skill-development, skill-creator, skill-architecture]
   "에이전트" → [agent, subagent, task-tool, autonomous]
   "문서화" → [documentation, session-journal, adr, markdown]
   ```

3. **Search using the script**:
   ```bash
   python scripts/search_sessions.py \
     --keywords "smart-commit,commit-agent,git" \
     --journal-dir /path/to/.dev-docs/sessions \
     --max-results 5
   ```

4. **Analyze results**:
   - Review top 3-5 sessions by relevance score
   - Read the "Summary" and "What We Did" sections
   - Identify most relevant sessions for the user's context

5. **Present findings**:
   - Session title and date
   - Brief summary of what was done
   - Link to full session file for deeper exploration

**Example**:

User: "이전에 커밋 정리 관련해서 뭐 했었지?"

Steps:
1. Extract: `커밋`, `정리`
2. Expand: `commit`, `smart-commit`, `commit-agent`, `git`, `organization`
3. Run search: `--keywords "smart-commit,commit-agent,git,organization"`
4. Find: `20251109_0503_agent-only-smart-commit.md` (highest score)
5. Present:
   ```
   2025-11-09 05:03에 "smart-commit을 에이전트 전용 스킬로 전환" 작업을 하셨습니다.

   요약: smart-commit 스킬을 에이전트 전용으로 전환하고 commit-agent를 신규 생성하여,
   커밋 작업이 메인 세션 컨텍스트를 소비하지 않도록 아키텍처 개선.

   자세한 내용: .dev-docs/sessions/20251109_0503_agent-only-smart-commit.md
   ```

**Edge case - No results**: If no sessions match, suggest alternative keywords from the Keywords Index in README.md or show recent sessions as fallback.

#### B. Time-Based Search

Find sessions within a specific time period.

**Time expression mapping**:
- "어제" → Yesterday (calculate YYYYMMDD)
- "지난주" → Last 7 days
- "최근" → Last 3-7 days

**Process**:

1. **Calculate date range**:
   ```python
   from datetime import datetime, timedelta
   today = datetime.now()
   week_ago = today - timedelta(days=7)
   start_date = week_ago.strftime('%Y%m%d')
   end_date = today.strftime('%Y%m%d')
   ```

2. **Search by date range**:
   ```bash
   python scripts/search_sessions.py \
     --date-range "20251102,20251109" \
     --journal-dir /path/to/.dev-docs/sessions
   ```

3. **Present chronologically**:
   - List sessions from the period (most recent first)
   - Include title, date, and summary for each

#### C. Work Continuation Strategy

Help users resume work from where they left off.

**Process**:

1. **Get recent sessions** (last 1-3 sessions within 48 hours):
   ```bash
   python scripts/search_sessions.py \
     --recent 3 \
     --journal-dir /path/to/.dev-docs/sessions
   ```

2. **Read the most recent session file** using the Read tool

3. **Parse "Next Steps" section**:
   - Extract unchecked tasks: `- [ ] Task description`
   - Extract checked tasks for context: `- [x] Completed task`

4. **Provide structured response**:
   ```
   지난 세션 요약:
   [Most recent session summary]

   아직 완료하지 않은 작업:
   - [ ] Pending task 1
   - [ ] Pending task 2

   추천 다음 작업:
   [First pending task with context about why it's next]
   ```

**Example**:

User: "어제 어디까지 작업했지? 오늘 뭐 하면 될까?"

Steps:
1. Get recent sessions: `--recent 2`
2. Read most recent: `20251109_0503_agent-only-smart-commit.md`
3. Parse Next Steps:
   ```markdown
   - [ ] commit-agent를 실제로 호출하여 작동 테스트
   - [ ] session-journal 완료 후 커밋 제안 플로우 검증
   ```
4. Present:
   ```
   지난 세션 (2025-11-09 05:03):
   smart-commit을 에이전트 전용 스킬로 전환하고 commit-agent를 신규 생성했습니다.

   아직 완료하지 않은 작업:
   - [ ] commit-agent를 실제로 호출하여 작동 테스트
   - [ ] session-journal 완료 후 커밋 제안 플로우 검증

   오늘은 commit-agent 작동 테스트를 진행하면 좋을 것 같습니다.
   ```

### 3. Provide Context and Next Actions

After retrieving relevant sessions:

- **Summarize findings**: Concise overview of what was found
- **Highlight key decisions**: Link to ADRs if mentioned in "Key Decisions" section
- **Suggest follow-ups**: Based on incomplete "Next Steps" or related work
- **Offer deeper exploration**: Suggest reading full session files if needed

## Using the Search Script

The `scripts/search_sessions.py` script is the primary tool for session retrieval.

**Keyword search**:
```bash
python scripts/search_sessions.py \
  --keywords "keyword1,keyword2,keyword3" \
  --journal-dir /path/to/.dev-docs/sessions \
  --max-results 5
```

**Date range search**:
```bash
python scripts/search_sessions.py \
  --date-range "20251101,20251109" \
  --journal-dir /path/to/.dev-docs/sessions
```

**Recent sessions**:
```bash
python scripts/search_sessions.py \
  --recent 3 \
  --journal-dir /path/to/.dev-docs/sessions
```

**Output format**: JSON with session metadata and scores
```json
{
  "results": [
    {
      "filename": "20251109_0503_agent-only-smart-commit.md",
      "filepath": "/path/to/.dev-docs/sessions/20251109_0503_agent-only-smart-commit.md",
      "title": "smart-commit을 에이전트 전용 스킬로 전환",
      "date": "2025-11-09 05:03",
      "keywords": ["smart-commit", "commit-agent", "agent-only-skill", ...],
      "summary": "smart-commit 스킬을 에이전트 전용으로 전환...",
      "score": 15.8,
      "keyword_score": 15,
      "recency_score": 0.8
    }
  ]
}
```

## Reference Documentation

For detailed information on session structure and search strategies, refer to:

- **`references/session_structure.md`**: Session document format, metadata structure, and Keywords Index
- **`references/search_strategies.md`**: Detailed keyword matching strategies, semantic expansion rules, and edge case handling

Load these references when:
- Unclear about session document structure
- Need guidance on keyword expansion for specific domains
- Handling edge cases (no results, too many results, ambiguous queries)

## Integration with Other Skills

- **session-journal**: Creates the session documents that session-recall searches
- **decision-tracker**: Important decisions can be cross-referenced using session links
- **smart-commit**: Sessions may reference commits; use session-recall to understand commit context

## Best Practices

1. **Always expand contextual keywords**: Don't search for user's exact words; expand to related domain terms
2. **Prioritize recency for continuity queries**: Recent sessions are more relevant for "what's next" questions
3. **Read full session files**: The script provides metadata, but reading the full file gives complete context
4. **Use Keywords Index**: `.dev-docs/sessions/README.md` maintains a keyword frequency index—use it to discover related keywords
5. **Combine strategies**: For complex queries, use keyword + time filtering together
6. **Graceful fallbacks**: If no results, show recent sessions or suggest refining the query

## Common Pitfalls

- **Don't search for generic terms**: "작업", "구현", "변경" are too broad—require additional context
- **Don't skip semantic expansion**: Users rarely remember exact keywords
- **Don't ignore Next Steps**: They're critical for work continuity
- **Don't forget to load references**: Use `references/search_strategies.md` for complex matching scenarios
