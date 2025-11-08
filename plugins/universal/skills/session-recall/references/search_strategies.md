# Session Search Strategies

This document outlines strategies for finding relevant sessions based on user queries.

## Search Strategy Selection

Choose the appropriate search strategy based on the user's query type:

| Query Type | Strategy | Example |
|------------|----------|---------|
| Keyword-based | Contextual keyword matching | "커밋 관련 작업 뭐 했었지?" |
| Time-based | Date range filtering | "어제 뭐 했었지?", "지난주에..." |
| Continuation | Recent session analysis | "어디까지 작업했지?", "오늘 뭐 하면 될까?" |
| Topic exploration | Multi-keyword clustering | "스킬 개발 관련해서..." |

## 1. Contextual Keyword Matching

### Problem
Users often don't remember exact keywords. For example:
- User says: "커밋 관련 작업"
- Actual keywords: `smart-commit`, `commit-agent`, `git`, `version-control`

### Solution: Multi-stage matching

#### Stage 1: Direct keyword extraction
Extract nouns and domain terms from the user's query:
- "커밋 관련 작업" → `커밋`, `작업`
- "스킬 만들 때" → `스킬`, `만들다`

#### Stage 2: Semantic expansion
Expand user terms to related keywords based on domain knowledge:

**Common expansions**:
- "커밋" → `commit`, `git`, `smart-commit`, `commit-agent`, `version-control`
- "스킬" → `skill`, `skill-development`, `skill-creator`, `skill-architecture`
- "에이전트" → `agent`, `subagent`, `task-tool`, `autonomous`
- "문서화" → `documentation`, `session-journal`, `adr`, `markdown`
- "정리" → `organization`, `refactoring`, `cleanup`

#### Stage 3: Keywords Index lookup
1. Read `.dev-journal/README.md`
2. Parse the "Keywords Index" section
3. For each expanded keyword, check:
   - Exact match (highest priority)
   - Partial match (substring)
   - Related keywords (same semantic cluster)

#### Stage 4: Session scoring
Score each session based on:
- **Exact keyword matches**: 10 points each
- **Partial keyword matches**: 5 points each
- **Recency**: Decay factor (newer = higher score)
- **Keyword frequency**: More keywords matched = higher score

Return top 3-5 sessions sorted by score.

## 2. Date Range Filtering

### Time expression mapping

| User Expression | Date Range |
|-----------------|------------|
| "어제" | Yesterday (00:00 - 23:59) |
| "오늘" | Today (00:00 - now) |
| "이번 주" | This week (Monday - now) |
| "지난주" | Last week (Monday - Sunday) |
| "최근" | Last 7 days |
| "최근 작업" | Last 2-3 sessions |

### Implementation
1. Parse time expression from user query
2. Calculate date range (start_date, end_date)
3. Filter session files by filename prefix (YYYYMMDD)
4. Sort by timestamp (most recent first)

## 3. Work Continuation Strategy

When users ask "What should I work on next?":

### Step 1: Identify recent sessions
- Get the 1-3 most recent sessions (within 24-48 hours)
- Prioritize sessions with incomplete "Next Steps"

### Step 2: Parse "Next Steps" section
Extract unchecked items:
```markdown
- [ ] Pending task 1
- [ ] Pending task 2
```

### Step 3: Provide context
Return:
1. **Last session summary**: What was accomplished
2. **Pending tasks**: Unchecked items from Next Steps
3. **Suggested next action**: First pending task with context

Example response:
```
지난 세션에서는 smart-commit을 에이전트 전용 스킬로 전환했습니다.

아직 완료하지 않은 작업:
- [ ] commit-agent를 실제로 호출하여 작동 테스트
- [ ] session-journal 완료 후 커밋 제안 플로우 검증

다음으로 commit-agent 작동 테스트를 진행하면 좋을 것 같습니다.
```

## 4. Multi-Session Topic Exploration

When exploring a topic across multiple sessions:

### Step 1: Identify seed keywords
Use contextual keyword matching to find initial relevant keywords.

### Step 2: Follow "Related Sessions" links
Each session has a "Related Sessions" section that links to connected work.

### Step 3: Build session graph
Create a chronological view of related sessions:
```
Session A (2025-11-09 04:34) - context-retention-planning
    ↓ Related Sessions
Session B (2025-11-09 04:47) - decision-tracker-implementation
    ↓ Related Sessions
Session C (2025-11-09 05:03) - agent-only-smart-commit
```

### Step 4: Summarize progression
Provide a narrative summary showing how work evolved across sessions.

## Edge Cases

### No matching sessions found
1. Suggest alternative keywords from the Keywords Index
2. Show the 3 most recent sessions as a fallback
3. Ask the user to clarify what they're looking for

### Too many matching sessions (>10)
1. Apply recency filtering (last 30 days)
2. Increase scoring threshold
3. Offer to refine the search with additional keywords

### Ambiguous keywords
When a keyword appears in many contexts:
- "작업" (work) - too generic
- "구현" (implementation) - too broad

Solution: Require additional context from user or combine with time filtering.
