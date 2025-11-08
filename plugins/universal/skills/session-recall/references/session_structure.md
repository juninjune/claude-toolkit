# Session Document Structure

This document describes the structure of session documents created by the session-journal skill.

## File Naming Convention

```
YYYYMMDD_HHMM_topic-slug.md
```

Example: `20251109_0503_agent-only-smart-commit.md`

## Document Structure

Each session document follows this structure:

### 1. Title (H1)
Human-readable title summarizing the session's main accomplishment.

Example: `# smart-commit을 에이전트 전용 스킬로 전환`

### 2. Metadata
```markdown
**Date**: YYYY-MM-DD HH:MM
**Keywords**: keyword1, keyword2, keyword3, ...
**Related Sessions**:
- [YYYYMMDD_HHMM](./filename.md) - Brief description
```

**Keywords**: Comma-separated list of domain-specific terms that describe the session's topics, features, modules, or issues. These are the primary search targets.

**Related Sessions**: Links to previous sessions with overlapping keywords or continuing work threads.

### 3. Summary (H2)
1-2 sentence high-level summary of what was accomplished.

### 4. Context (H2)
Background information, motivation, and problem statement that led to this session's work.

### 5. What We Did (H2)
Detailed chronological breakdown of actions taken, organized with H3 subheadings for major steps.

### 6. Key Decisions (H2)
Important technical decisions made during the session, often with links to ADR documents.

Format:
```markdown
- **Decision title**
  - Reason: Why this decision was made
  - **Decision**: [ADR-NNNN: Title](path/to/adr.md) (if applicable)
```

### 7. Next Steps (H2)
Checklist of follow-up tasks, both completed and pending.

Format:
```markdown
- [x] Completed task
- [ ] Pending task
```

**Important**: This section is critical for work continuity. When users ask "What should I work on next?", this section from recent sessions should be prioritized.

### 8. References (H2)
List of relevant files, documents, or resources referenced during the session.

## Keywords Index (README.md)

The `.dev-journal/README.md` maintains a Keywords Index that tracks:

1. **Keyword frequency**: How many times each keyword appears across sessions
2. **Session mapping**: Which sessions contain each keyword

Format:
```markdown
### keyword-name (N회)
- YYYYMMDD_HHMM_session-slug
- YYYYMMDD_HHMM_another-session
```

**Usage**: This index is the primary data structure for keyword-based session searching.
