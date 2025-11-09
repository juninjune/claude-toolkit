---
name: research-topic
description: Research technical topics, algorithms, libraries, or implementation approaches and generate structured documentation in .dev-docs/research/. Use when users request investigation of technologies ("~에 대해 조사해줘", "~이 뭐고 어떻게 사용하는지", "~어떻게 개발해야할지") for algorithms, frameworks, libraries, design patterns, or feature implementation methods. Creates comprehensive research documents with examples and references.
---

# Research Topic Skill

Research technical topics and generate structured documentation in `.dev-docs/research/`.

## Purpose

Enable comprehensive investigation of technical topics including algorithms, libraries, frameworks, design patterns, and implementation approaches. Generate well-structured research documents that serve as references for future development work.

## When to Use

Trigger this skill when users request investigation or research:
- "~에 대해 조사해줘" (investigate/research X)
- "~이 뭐고 어떻게 사용하는 건지 조사해줘" (what is X and how to use it)
- "~어떻게 개발해야할지 모르겠네" (how should I develop/implement X)

**Topic types**:
- Algorithms and data structures (e.g., Myers diff algorithm, A* search)
- Libraries and frameworks (e.g., Google ML Kit, React Query)
- Feature implementation approaches (e.g., how to implement real-time sync)
- Architecture and design patterns (e.g., CQRS, Event Sourcing)

## Research Workflow

### 1. Extract Research Topic

Identify the core topic from the user's request. Examples:
- "Myers diff 알고리즘에 대해 조사해줘" → Topic: "Myers diff algorithm"
- "Google ML Kit이 뭐고 어떻게 사용하는지" → Topic: "Google ML Kit usage"
- "실시간 동기화 기능 어떻게 개발해야할지" → Topic: "real-time synchronization implementation"

### 2. Gather Information

Use WebSearch and WebFetch tools to collect information:

**WebSearch queries** (run 2-3 searches):
- Overview: "[topic] overview tutorial"
- Technical details: "[topic] how it works implementation"
- Practical usage: "[topic] examples best practices"

**WebFetch targets** (select 2-4 high-quality sources):
- Official documentation
- In-depth technical articles
- Tutorial with code examples
- Comparative analysis or discussion

**Information to collect**:
- What: Core concept and purpose
- Why: Problem it solves, use cases
- How: Key mechanisms, workflow, architecture
- Usage: Code examples, API patterns, configuration
- Comparisons: Alternatives, trade-offs
- References: Official docs, articles, repos

### 3. Structure Research Document

Create document at `.dev-docs/research/YYYYMMDD_topic-slug.md` with this structure:

```markdown
---
date: YYYY-MM-DD
topic: [Main topic name]
keywords: [keyword1, keyword2, keyword3]
---

# [Topic Title]

> [One-sentence summary of what this topic is about]

## 개요 (Overview)

### 무엇인가? (What)
[2-3 paragraphs explaining what the topic is, its purpose, and why it exists]

### 왜 필요한가? (Why)
[Problems it solves, use cases, benefits]

## 핵심 개념 (Core Concepts)

### 동작 원리 (How It Works)
[Technical explanation of how it works - architecture, algorithms, key mechanisms]

### 주요 특징 (Key Features)
- Feature 1: [description]
- Feature 2: [description]
- Feature 3: [description]

## 사용 방법 (Usage)

### 기본 사용법 (Basic Usage)
[Step-by-step guide or code examples for common use cases]

```[language]
// Example code
```

### 고급 패턴 (Advanced Patterns)
[More complex usage patterns, configurations, or techniques if applicable]

## 비교 및 선택 기준 (Comparisons)

### 대안 기술 (Alternatives)
- Alternative 1: [brief comparison]
- Alternative 2: [brief comparison]

### 언제 사용해야 하나? (When to Use)
[Guidelines for when this approach/tool is appropriate vs alternatives]

## 참고 자료 (References)

- [Official Documentation](URL)
- [Tutorial/Article Title](URL)
- [Related Resource](URL)
```

### 4. Document Naming Convention

Use `YYYYMMDD_topic-slug.md` format:
- `20250109_myers-diff-algorithm.md`
- `20250109_google-ml-kit-usage.md`
- `20250109_realtime-sync-implementation.md`

Create slug from topic by:
1. Converting to lowercase
2. Replacing spaces with hyphens
3. Removing special characters
4. Keeping only alphanumeric and hyphens

### 5. Maintain Research Index

After creating research document, ensure `.dev-docs/research/README.md` exists and update it:

```markdown
# Research Documents

Index of technical research documents.

## By Date

- [YYYY-MM-DD: Topic Title](YYYYMMDD_topic-slug.md) - Brief description

## By Category

### Algorithms
- [Myers Diff Algorithm](YYYYMMDD_myers-diff-algorithm.md)

### Libraries & Frameworks
- [Google ML Kit](YYYYMMDD_google-ml-kit.md)

### Implementation Approaches
- [Real-time Sync](YYYYMMDD_realtime-sync.md)
```

## Quality Guidelines

**Research depth**: Target 15-20 minutes reading time (medium depth)
- Include concept explanations with examples
- Provide practical code samples
- Balance breadth and depth appropriately

**Writing style**:
- Use Korean for section headers and explanations
- Use English for technical terms and code
- Write clearly and concisely
- Focus on practical applicability

**Source quality**:
- Prefer official documentation
- Use reputable technical blogs and articles
- Include recent sources (check dates)
- Verify information across multiple sources

**Completeness**:
- All major sections should have content
- Include at least 2-3 code examples
- Provide 3-5 reference links
- Extract 3-5 relevant keywords

## Output

After generating the research document:
1. Inform user of the created file path
2. Provide a 2-3 sentence summary of key findings
3. Suggest related topics if applicable
