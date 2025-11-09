---
name: commit-review
description: Analyze commit history to identify refactoring opportunities (unnecessary complexity, YAGNI violations, code smells) and verify alignment between documented work (sessions, ADRs) and actual code changes. Use when users request "커밋 리뷰", "작업 리뷰", or "리뷰해줘" with time ranges like "오늘", "지난 한주", "마지막 리뷰 이후", or "마지막 릴리즈 이후". Creates review documents in .dev-docs/reviews/ with progressive disclosure analysis.
---

# Commit Review Skill

## Overview

Analyze git commit history to identify refactoring opportunities and verify work-documentation alignment. Use progressive disclosure: start with lightweight metadata analysis, then deepen investigation as needed. Focus on detecting unnecessary complexity (YAGNI violations, cognitive overload, code smells) rather than style preferences. Generate structured review documents that chain together, enabling continuous improvement tracking across releases.

## When to Use This Skill

Trigger this skill when users request commit or work reviews with phrases like:

- "커밋 리뷰해줘" / "작업 리뷰해줘" / "리뷰해줘"
- Time-based: "오늘 작업 리뷰", "지난 한주 리뷰", "지난 N일 리뷰"
- Reference-based: "마지막 리뷰 이후", "마지막 릴리즈 이후", "v1.0.0 이후"
- Explicit commit range: "abc1234..def5678 리뷰"

## Core Principles

1. **Progressive Disclosure**: Start lightweight (metadata), deepen only when needed (diffs, full files, project-wide search)
2. **Evidence-Based Analysis**: Ground refactoring suggestions in established principles (Google's code review standards, YAGNI, cognitive complexity research)
3. **Chain Review System**: Each review references previous review, enabling continuous tracking of proposals and their resolution
4. **Context-Aware**: Integrate with existing .dev-docs ecosystem (sessions, ADRs, milestones)

## Workflow

### Step 1: Determine Review Scope

Identify the commit range to analyze:

1. **Check for previous reviews**:
   ```bash
   # If .dev-docs/reviews/README.md exists
   # Read it to find last review's commit range
   # Start from previous review's end commit
   ```

2. **Parse user's time specification**:
   - "오늘": commits since 00:00 today
   - "지난 한주": commits from 7 days ago
   - "마지막 릴리즈 이후": find most recent tag, use `git describe --tags --abbrev=0`, then `tag..HEAD`
   - Explicit range: use as-is (e.g., `abc1234..def5678`)

3. **Extract commit list**:
   ```bash
   git log --oneline --no-merges <range>
   ```

4. **Confirm scope with user**:
   "Found N commits from YYYY-MM-DD to YYYY-MM-DD (커밋 범위: `abc1234..def5678`). Proceed with review?"

### Step 2: Lightweight Metadata Analysis

Perform fast pattern recognition without reading code:

1. **Collect commit statistics**:
   ```bash
   git log --stat --no-merges <range>
   ```

2. **Analyze patterns**:
   - Total commits, average size (lines changed)
   - Commit type distribution (feat/fix/refactor/docs/etc.)
   - Scope distribution (which modules changed most)
   - Top 5 most-changed files
   - Outliers: unusually large commits, reverts, scope inconsistencies

3. **Generate metrics table**:
   Use data to populate "분석 메트릭스" section of review template

### Step 3: Load Related Sessions

Find session documents overlapping with commit date range:

1. **Search sessions by date**:
   ```bash
   # List sessions in date range
   ls .dev-docs/sessions/ | grep "^YYYYMMDD"
   ```

2. **Read relevant session documents**:
   - Extract "What We Did" sections
   - Extract "Key Decisions" sections
   - Extract "Next Steps" sections
   - Note related ADRs mentioned

3. **Create session-commit mapping**:
   - For each session, find commits in same date range
   - Build table: session → commits
   - Identify sessions with no commits (work not committed?)
   - Identify commits with no session (work not documented?)

### Step 4: Progressive Code Analysis

Start shallow, go deeper only when suspicious patterns emerge:

#### Level 1: Diff Statistics (Always Perform)

For each commit:
```bash
git show --stat <commit-hash>
```

Look for:
- Commits touching >5 files (potential "shotgun surgery")
- Commits with very high additions (>500 lines in single file)
- Commits mixing unrelated file types (potential grouping issues)

#### Level 2: Diff Content (Suspicious Commits Only)

When Level 1 flags issues, read actual diff:
```bash
git show <commit-hash>
```

Apply `references/review_principles.md` checks:

**Complexity Signals**:
- Functions >50 lines (Google: "too complex")
- Nesting >3 levels (cognitive complexity warning)
- Files >500 lines (Blob Class smell)
- Complex boolean logic (>3 conditions combined)

**YAGNI Violations**:
- Abstract interfaces with single implementation
- Generic parameters always same value
- "Helper"/"Util" classes with unrelated methods
- Configuration options never used

**Code Smells**:
- Duplicated code patterns (same logic repeated)
- Long methods without structure (Spaghetti Code)
- God classes (multiple unrelated responsibilities)

#### Level 3: Full File Context (When Level 2 Needs Context)

When diff isn't enough to understand complexity:
```bash
# Read the full file to understand context
```

Use Read tool to load complete file, analyze:
- How new code fits into existing structure
- Whether new code increases or decreases overall complexity
- Surrounding code quality (is this adding to existing mess or cleaning up?)

#### Level 4: Project-Wide Search (When Duplication Suspected)

When code patterns look like they might exist elsewhere:
```bash
# Search for similar patterns across codebase
```

Use Grep tool to find:
- Similar function names
- Similar logic patterns
- Potential consolidation opportunities

### Step 5: Generate Refactoring Proposals

For each issue identified in Step 4:

1. **Classify priority**:
   - **🔴 High**: High-change area + critical smell (Blob Class, Spaghetti Code, YAGNI violation)
   - **🟡 Medium**: Medium-change area + moderate smell, or low-change + critical smell
   - **🟢 Low**: Low-change area + minor smell, or cosmetic improvements

2. **Structure proposal**:
   ```markdown
   #### [Priority]-[Number]: [Title]

   **위치**: `file.ts:123-145`
   **관련 커밋**: `abc1234`

   **문제 유형**: YAGNI 위반 / 과도한 추상화 / 인지적 복잡도 증가 / 코드 스멜

   **현재 상황**:
   [Code example showing the problem]

   **제안**:
   [Specific refactoring approach]

   **근거**:
   - [Reference to review_principles.md]
   - [Specific violation: e.g., "인지적 복잡도 15 (권장: 10 이하)"]

   **예상 효과**:
   - [Concrete benefits]
   ```

3. **Ground in principles**:
   Always cite `references/review_principles.md`:
   - Google's complexity definition
   - YAGNI costs (build, delay, carry, repair)
   - Cognitive complexity thresholds
   - Technical debt research findings

4. **Be specific and actionable**:
   - Point to exact file and line numbers
   - Provide code examples (current vs. proposed)
   - Explain why, not just what
   - Estimate impact (lines reduced, complexity decrease)

### Step 6: Verify Work-Documentation Alignment

Cross-reference commits with sessions and ADRs:

#### Session Alignment

For each session found in Step 3:

1. **Compare "What We Did" with actual commits**:
   - ✅ Complete match: all work documented and committed
   - ⚠️ Partial match: some work documented but not all committed
   - ❌ No match: work documented but no related commits

2. **Check "Next Steps" resolution**:
   - Read session's "Next Steps" checklist
   - Search subsequent commits for evidence of completion
   - Flag unresolved next steps for future tracking

#### ADR Implementation Tracking

For each ADR mentioned in sessions or commit messages:

1. **Read ADR document**:
   - Extract "Decision" section (what was decided)
   - Extract "Implementation Notes" (how to implement)

2. **Find implementation commits**:
   - Search commit messages for ADR references
   - Search diffs for code matching implementation notes
   - Classify: 🟢 Implemented / 🟡 Partial / ⭕ Not yet

3. **Add implementation tracking to ADR**:
   If ADR document lacks implementation tracking, suggest updating it with:
   ```markdown
   ## Implementation Status

   🟢 Implemented in commits:
   - `abc1234` - feat(scope): implementation description
   ```

#### Milestone Contribution

If MILESTONES.md exists:

1. **Identify active milestones**:
   - Read MILESTONES.md
   - Find milestones without "완료일" (in progress)

2. **Map commits to milestones**:
   - Check commit scopes against milestone features
   - Track completion percentage changes

### Step 7: Track Previous Review Proposals

If previous review exists (from Step 1):

1. **Read previous review document**:
   - Extract all refactoring proposals (High, Medium, Low)
   - Note proposal numbers and titles

2. **Check each proposal's resolution**:
   - Search current commit range for evidence of refactoring
   - Classify: ✅ Implemented / ⭕ Not yet / ❌ Rejected

3. **Create tracking table**:
   ```markdown
   ### ✅ [이전 제안 HP-1]: 반영됨
   - **제안 내용**: [original proposal]
   - **반영 커밋**: `abc1234`
   - **평가**: [how it was addressed]
   ```

### Step 8: Assess Overall Code Health

Provide high-level evaluation:

1. **Determine health direction**:
   - ✅ **개선**: Refactoring commits > feature commits, complexity decreased
   - ➖ **유지**: Roughly balanced, no significant change
   - ⚠️ **경고**: Some complexity increases, but not critical
   - ❌ **악화**: Significant complexity increases, high-priority issues introduced

2. **Provide evidence**:
   - Cite specific metrics (line counts, function lengths, file sizes)
   - Reference commits that improved or degraded health
   - Compare to previous review if available

3. **Trend analysis**:
   - Total code size trend
   - Average function length trend
   - Test coverage trend (if measurable)

### Step 9: Create Review Document

Generate review document using `references/review_template.md`:

1. **Determine filename**:
   ```
   YYYYMMDD_HHMM_review-[period-slug].md

   Examples:
   - 20251109_1430_review-last-week.md
   - 20251109_1430_review-since-last-review.md
   - 20251109_1430_review-v1.0.0-to-v1.1.0.md
   ```

2. **Populate all sections**:
   - Metadata (date, range, previous review link)
   - 요약 (1-2 sentence overview)
   - 분석 메트릭스 (from Step 2)
   - 리팩토링 기회 (from Step 5)
   - 작업-문서 정합성 (from Step 6)
   - 이전 리뷰 추적 (from Step 7)
   - 코드 건강도 평가 (from Step 8)
   - 다음 리뷰 시 확인 사항 (actionable checklist)
   - 관련 세션/ADR/마일스톤 (cross-links)
   - 메타데이터 (keywords, duration, proposal counts)

3. **Write document**:
   ```bash
   # Create review document
   Write to: .dev-docs/reviews/YYYYMMDD_HHMM_review-slug.md
   ```

### Step 10: Update Cross-Links and Indexes

Maintain bidirectional links:

1. **Update or create .dev-docs/reviews/README.md**:

   If doesn't exist, create with:
   ```markdown
   # Commit Reviews Index

   This directory contains periodic reviews of commit history, identifying refactoring opportunities and tracking work-documentation alignment.

   ## Reviews (Reverse Chronological)

   - [YYYYMMDD_HHMM](./YYYYMMDD_HHMM_review-slug.md) - Period: YYYY-MM-DD ~ YYYY-MM-DD, N commits

   ## Review Chain

   Each review references the previous review to track proposal resolution:

   ```
   [Latest] ← [Previous] ← [Earlier] ← [Oldest]
   ```

   ## Keywords Index

   ### refactoring (N회)
   - YYYYMMDD_HHMM_review-slug

   ### code-health (N회)
   - YYYYMMDD_HHMM_review-slug
   ```

   If exists, prepend new review to list.

2. **Add review reference to related sessions**:

   For each session with commits analyzed, add to session document:
   ```markdown
   **Related Reviews**:
   - [Commit Review YYYY-MM-DD](../reviews/YYYYMMDD_HHMM_review-slug.md)
   ```

3. **Add review reference to related ADRs**:

   For ADRs with implementation tracking, add to ADR document:
   ```markdown
   ## Related Reviews
   - [YYYYMMDD_HHMM](../reviews/YYYYMMDD_HHMM_review-slug.md) - Implementation status tracked
   ```

### Step 11: Present Review Summary to User

Provide concise summary:

```
✅ Commit review completed: [period description]

📊 **Analysis**:
- Analyzed: N commits (YYYY-MM-DD ~ YYYY-MM-DD)
- Commit range: `abc1234..def5678`

🔍 **Findings**:
- High priority refactoring opportunities: X
- Medium priority: Y
- Low priority: Z

📈 **Code Health**: ✅ 개선 / ➖ 유지 / ⚠️ 경고 / ❌ 악화

📄 **Review document**: [YYYYMMDD_HHMM_review-slug.md](file://.dev-docs/reviews/YYYYMMDD_HHMM_review-slug.md)

[If high-priority items exist]
⚠️ **Attention needed**:
- HP-1: [Title] (`file.ts:123`)
- HP-2: [Title] (`file2.py:456`)

[If previous review proposals were addressed]
✅ **Progress**: M of N previous proposals implemented
```

## Analysis Guidelines

### Progressive Disclosure Decision Tree

```
Start: Commit metadata analysis
    ↓
Found suspicious patterns? (large commits, many files, scope inconsistencies)
    ↓ YES → Read commit diffs
    │         ↓
    │       Found complexity issues? (long functions, deep nesting, duplication)
    │         ↓ YES → Read full file context
    │         │         ↓
    │         │       Need to check for duplication?
    │         │         ↓ YES → Project-wide grep search
    │         │         ↓ NO → Skip
    │         │
    │         ↓ NO → Skip deeper analysis
    │
    ↓ NO → Skip diff analysis, proceed to Step 6
```

### When to Stop Deepening

Limit analysis depth to manage token usage:

- **Stop after Level 1** if: <10 commits, all small (<100 lines each), no obvious issues
- **Stop after Level 2** if: No complexity issues found, all commits look clean
- **Stop after Level 3** if: Issues are localized, no patterns suggesting wider problems
- **Proceed to Level 4** only if: Strong evidence of duplication across multiple commits

### Refactoring Priority Calibration

Use this rubric:

| Issue Type | Change Frequency | Lines Affected | Priority |
|------------|------------------|----------------|----------|
| YAGNI violation | High (weekly+) | Any | 🔴 HIGH |
| Blob Class (>500 lines) | High | >100 | 🔴 HIGH |
| Spaghetti Code (function >100 lines) | High | >50 | 🔴 HIGH |
| Cognitive Complexity >15 | High | >30 | 🔴 HIGH |
| YAGNI violation | Medium | Any | 🟡 MEDIUM |
| Blob Class | Medium | >100 | 🟡 MEDIUM |
| Duplication (3+ instances) | High | >30 | 🟡 MEDIUM |
| Cognitive Complexity 11-15 | Medium | >30 | 🟡 MEDIUM |
| Minor duplication | Any | <30 | 🟢 LOW |
| Style inconsistencies | Any | Any | 🟢 LOW |
| Naming improvements | Any | Any | 🟢 LOW |

**Change frequency** = How often this file/module is modified:
- High: 5+ commits in analyzed period
- Medium: 2-4 commits
- Low: 1 commit or less

### Balancing Depth vs. Speed

Adjust analysis depth based on review purpose:

- **Quick health check** (e.g., daily review): Stop after Level 2, focus on critical issues only
- **Weekly review**: Level 2-3, propose high/medium priorities
- **Release retrospective**: Full Level 4 analysis, comprehensive refactoring roadmap
- **Post-major-feature**: Level 3-4 for new code, Level 1-2 for unchanged areas

User can always request deeper analysis: "Can you analyze [specific file] more deeply?"

## References

This skill includes reference documentation with evidence-based principles:

### `references/review_principles.md`

Comprehensive guide covering:

1. **Complexity and Code Health** (Google Engineering Practices)
   - Definition of "too complex"
   - Continuous improvement over perfection
   - System-level thinking

2. **YAGNI: Avoiding Over-Engineering** (Martin Fowler)
   - Four costs of ignoring YAGNI
   - When YAGNI applies vs. doesn't apply
   - Detection strategies

3. **Cognitive Complexity**
   - Calculation method
   - Differences from cyclomatic complexity
   - Patterns that increase cognitive load
   - Threshold guidelines

4. **Technical Debt Prioritization** (Scientific Research)
   - Most critical code smells (Blob Class, Spaghetti Code)
   - When technical debt actually matters
   - Detection timing insights

5. **When to Refactor** (Martin Fowler)
   - Rule of Three
   - Best timing for refactoring
   - Two Hats philosophy

Load this reference when performing Level 2-4 analysis to ground proposals in established principles.

### `references/review_template.md`

Template for review document structure. Use this to ensure consistency across all reviews. Contains sections for:

- Metadata and commit range
- 분석 메트릭스 (metrics)
- 리팩토링 기회 (proposals by priority)
- 작업-문서 정합성 (session/ADR alignment)
- 이전 리뷰 추적 (previous proposal tracking)
- 코드 건강도 평가 (overall health assessment)
- Cross-links to sessions, ADRs, milestones

## Best Practices

### Writing Effective Refactoring Proposals

1. **Be specific**: Point to exact files and line numbers
2. **Show, don't just tell**: Include code examples (current state)
3. **Explain why**: Ground in `review_principles.md`, not personal preference
4. **Quantify impact**: "Reduces cognitive complexity from 15 to 8"
5. **Provide actionable steps**: "Extract lines 123-145 into separate function"
6. **Consider context**: High-change files need immediate attention, low-change can wait

### Maintaining Review Chain Integrity

1. **Always link to previous review**: Enables tracking across time
2. **Track all previous proposals**: Shows continuous improvement (or lack thereof)
3. **Update proposal status honestly**: If not addressed, mark ⭕ not ✅
4. **Carry forward unresolved items**: Add to "다음 리뷰 시 확인 사항"

### Balancing Criticism with Encouragement

1. **Acknowledge good practices**: If commits show refactoring, praise it
2. **Frame proposals as opportunities**: "Opportunity to simplify" not "This is bad"
3. **Provide context for decisions**: "Research shows class length matters most"
4. **Prioritize ruthlessly**: Don't overwhelm with dozens of low-priority items

### Integration with Existing Ecosystem

1. **Cross-link generously**: Connect reviews to sessions, ADRs, milestones
2. **Respect existing formats**: Match markdown style of sessions/ADRs
3. **Update indexes promptly**: Keep README.md files current
4. **Use consistent keywords**: Match session keyword patterns for searchability

## Common Patterns

### Pattern 1: Daily Quick Check

**Scenario**: User runs daily review at end of workday

**Approach**:
- Start from last review's end commit (or start of day if no review)
- Level 1-2 analysis only (fast)
- Focus on high-priority issues only
- Brief summary format

**Expected duration**: 2-5 minutes for <10 commits

### Pattern 2: Weekly Retrospective

**Scenario**: Team reviews week's work every Friday

**Approach**:
- Full week's commits (last review to now)
- Level 2-3 analysis (moderate depth)
- All priority levels (High, Medium, Low)
- Comprehensive documentation

**Expected duration**: 5-15 minutes for 20-50 commits

### Pattern 3: Pre-Release Audit

**Scenario**: Before major release, audit all changes since last release

**Approach**:
- Tag-to-tag range (e.g., `v1.0.0..v1.1.0`)
- Level 3-4 analysis (deep, thorough)
- Project-wide duplication search
- Focus on code health trend

**Expected duration**: 15-30 minutes for 100+ commits

### Pattern 4: Feature Branch Review

**Scenario**: Before merging feature branch, review its commits

**Approach**:
- Branch-specific range (e.g., `main..feature-branch`)
- Level 2-3 analysis
- Focus on feature-specific complexity
- Verify feature doesn't degrade main branch health

**Expected duration**: 5-10 minutes for 10-20 commits

## Troubleshooting

### Issue: "Too many commits to analyze"

**Solution**: Narrow scope or increase abstraction level
- Suggest smaller time range: "100+ commits found. Review last 2 weeks instead of month?"
- Use Level 1 only for bulk, Level 2-3 for flagged items only
- Focus on high-impact files (most changed files from stats)

### Issue: "No previous review found, can't chain"

**Solution**: This is the first review
- Omit "이전 리뷰 추적" section from template
- Note in README.md: "First review in series"
- Establish baseline: "This review establishes health baseline for future tracking"

### Issue: "Sessions don't align with commits"

**Possible causes**:
1. Work done but not documented → Flag for user: "Found commits without session docs"
2. Session documented but not committed → Verify with user: "Session mentions X but no related commits found. Work in progress?"
3. Date mismatch → Session dated wrong, or commits made later

**Solution**: Report mismatches honestly, ask user for clarification

### Issue: "Can't determine if ADR is implemented"

**Solution**: Mark as 🟡 Partial with caveat
- "ADR-XXXX implementation unclear from commit diffs alone"
- "Recommendation: Add explicit ADR reference in future commits (e.g., 'Implements ADR-XXXX')"

### Issue: "Previous proposal was rejected, not just unimplemented"

**Solution**: Distinguish explicitly
- ✅ Implemented: Refactoring done
- ⭕ Not yet: Still pending, carry forward
- ❌ Rejected: User decided not to do it (note reason if known)

## Limitations

1. **No static analysis tools**: Relies on git diffs and Claude's code understanding, not AST parsing or linters
2. **Subjective judgment**: Complexity assessment based on heuristics (line counts, nesting), not computed metrics
3. **Context window constraints**: Very large commits or many files may require selective sampling
4. **Language-agnostic principles**: Uses general principles (YAGNI, cognitive complexity) rather than language-specific idioms
5. **No automated testing**: Cannot verify refactoring proposals are safe without breaking tests

## Future Enhancements

Potential improvements for future iterations:

- Integration with test coverage tools (track coverage trends)
- Automated cognitive complexity calculation (if AST parsing available)
- Pattern library of common refactorings (extract function, introduce parameter object, etc.)
- Diffstat visualization (charts showing change distribution)
- Smart commit message analysis (detect conventional commit compliance)
