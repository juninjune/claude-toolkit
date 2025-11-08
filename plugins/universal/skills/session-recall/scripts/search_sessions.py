#!/usr/bin/env python3
"""
Session Search Script

Searches .dev-journal/ sessions based on keywords, date ranges, or recency.
Returns matching sessions with relevance scores.

Usage:
    python search_sessions.py --keywords "smart-commit,git" --journal-dir /path/to/.dev-journal
    python search_sessions.py --date-range "2025-11-08,2025-11-09" --journal-dir /path/to/.dev-journal
    python search_sessions.py --recent 3 --journal-dir /path/to/.dev-journal
"""

import argparse
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional


def parse_session_filename(filename: str) -> Optional[Dict[str, str]]:
    """
    Parse session filename into components.

    Format: YYYYMMDD_HHMM_topic-slug.md
    Returns: {date: YYYYMMDD, time: HHMM, slug: topic-slug}
    """
    pattern = r'(\d{8})_(\d{4})_(.+)\.md$'
    match = re.match(pattern, filename)
    if match:
        return {
            'date': match.group(1),
            'time': match.group(2),
            'slug': match.group(3)
        }
    return None


def parse_session_metadata(filepath: Path) -> Dict[str, Any]:
    """
    Parse metadata from a session file.

    Extracts: title, date, keywords, summary
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')

    # Extract title (first H1)
    title = None
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break

    # Extract keywords
    keywords = []
    for line in lines:
        if line.startswith('**Keywords**:'):
            keywords_str = line.split(':', 1)[1].strip()
            keywords = [k.strip() for k in keywords_str.split(',')]
            break

    # Extract date
    date = None
    for line in lines:
        if line.startswith('**Date**:'):
            date = line.split(':', 1)[1].strip()
            break

    # Extract summary (first line after ## Summary)
    summary = None
    summary_section = False
    for line in lines:
        if line.startswith('## Summary'):
            summary_section = True
            continue
        if summary_section and line.strip():
            summary = line.strip()
            break

    return {
        'title': title,
        'date': date,
        'keywords': keywords,
        'summary': summary
    }


def calculate_recency_score(date_str: str) -> float:
    """
    Calculate recency score (0.0 - 1.0) based on how recent the session is.

    More recent sessions get higher scores with exponential decay.
    """
    try:
        session_date = datetime.strptime(date_str[:8], '%Y%m%d')
        today = datetime.now()
        days_ago = (today - session_date).days

        # Exponential decay: score = e^(-days/7)
        # Sessions from today: 1.0
        # Sessions from 7 days ago: ~0.37
        # Sessions from 30 days ago: ~0.01
        import math
        return math.exp(-days_ago / 7.0)
    except:
        return 0.0


def keyword_match_score(query_keywords: List[str], session_keywords: List[str]) -> int:
    """
    Calculate keyword match score.

    Scoring:
    - Exact match: 10 points
    - Partial match (substring): 5 points
    """
    score = 0
    query_keywords_lower = [k.lower() for k in query_keywords]
    session_keywords_lower = [k.lower() for k in session_keywords]

    for qk in query_keywords_lower:
        for sk in session_keywords_lower:
            if qk == sk:
                score += 10  # Exact match
            elif qk in sk or sk in qk:
                score += 5   # Partial match

    return score


def search_by_keywords(
    journal_dir: Path,
    keywords: List[str],
    max_results: int = 10
) -> List[Dict[str, Any]]:
    """
    Search sessions by keywords with relevance scoring.
    """
    results = []

    # Get all session files (excluding README.md)
    session_files = [
        f for f in journal_dir.glob('*.md')
        if f.name != 'README.md' and parse_session_filename(f.name)
    ]

    for filepath in session_files:
        parsed = parse_session_filename(filepath.name)
        if not parsed:
            continue

        metadata = parse_session_metadata(filepath)

        # Calculate scores
        keyword_score = keyword_match_score(keywords, metadata['keywords'])
        recency_score = calculate_recency_score(parsed['date'])

        # Total score: weighted sum
        total_score = keyword_score + (recency_score * 2)  # Slight recency boost

        if total_score > 0:
            results.append({
                'filename': filepath.name,
                'filepath': str(filepath),
                'title': metadata['title'],
                'date': metadata['date'],
                'keywords': metadata['keywords'],
                'summary': metadata['summary'],
                'score': total_score,
                'keyword_score': keyword_score,
                'recency_score': recency_score
            })

    # Sort by total score (descending)
    results.sort(key=lambda x: x['score'], reverse=True)

    return results[:max_results]


def search_by_date_range(
    journal_dir: Path,
    start_date: str,
    end_date: str
) -> List[Dict[str, Any]]:
    """
    Search sessions within a date range.

    Dates in format: YYYYMMDD
    """
    start = datetime.strptime(start_date, '%Y%m%d')
    end = datetime.strptime(end_date, '%Y%m%d')

    results = []
    session_files = [
        f for f in journal_dir.glob('*.md')
        if f.name != 'README.md' and parse_session_filename(f.name)
    ]

    for filepath in session_files:
        parsed = parse_session_filename(filepath.name)
        if not parsed:
            continue

        session_date = datetime.strptime(parsed['date'], '%Y%m%d')

        if start <= session_date <= end:
            metadata = parse_session_metadata(filepath)
            results.append({
                'filename': filepath.name,
                'filepath': str(filepath),
                'title': metadata['title'],
                'date': metadata['date'],
                'keywords': metadata['keywords'],
                'summary': metadata['summary']
            })

    # Sort by date (most recent first)
    results.sort(key=lambda x: x['filename'], reverse=True)

    return results


def get_recent_sessions(
    journal_dir: Path,
    count: int = 3
) -> List[Dict[str, Any]]:
    """
    Get the N most recent sessions.
    """
    session_files = [
        f for f in journal_dir.glob('*.md')
        if f.name != 'README.md' and parse_session_filename(f.name)
    ]

    # Sort by filename (which includes timestamp)
    session_files.sort(reverse=True)

    results = []
    for filepath in session_files[:count]:
        metadata = parse_session_metadata(filepath)
        results.append({
            'filename': filepath.name,
            'filepath': str(filepath),
            'title': metadata['title'],
            'date': metadata['date'],
            'keywords': metadata['keywords'],
            'summary': metadata['summary']
        })

    return results


def main():
    parser = argparse.ArgumentParser(description='Search .dev-journal sessions')
    parser.add_argument('--journal-dir', required=True, help='Path to .dev-journal directory')
    parser.add_argument('--keywords', help='Comma-separated keywords to search')
    parser.add_argument('--date-range', help='Date range: YYYYMMDD,YYYYMMDD')
    parser.add_argument('--recent', type=int, help='Get N most recent sessions')
    parser.add_argument('--max-results', type=int, default=10, help='Maximum results to return')

    args = parser.parse_args()

    journal_dir = Path(args.journal_dir)
    if not journal_dir.exists():
        print(json.dumps({'error': f'Journal directory not found: {journal_dir}'}))
        return 1

    results = []

    if args.keywords:
        keywords = [k.strip() for k in args.keywords.split(',')]
        results = search_by_keywords(journal_dir, keywords, args.max_results)
    elif args.date_range:
        start, end = args.date_range.split(',')
        results = search_by_date_range(journal_dir, start.strip(), end.strip())
    elif args.recent:
        results = get_recent_sessions(journal_dir, args.recent)
    else:
        print(json.dumps({'error': 'No search criteria provided'}))
        return 1

    # Output as JSON
    print(json.dumps({'results': results}, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    exit(main())
