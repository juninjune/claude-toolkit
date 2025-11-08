#!/usr/bin/env python3
"""
Find related sessions based on keyword matching.

This script searches through existing session files to find related ones
based on keyword overlap.
"""

import sys
import os
import re
from pathlib import Path
from typing import List, Dict, Set


def extract_metadata_from_file(filepath: Path) -> Dict:
    """
    Extract metadata (keywords, summary) from a session markdown file.
    
    Args:
        filepath: Path to the session markdown file
        
    Returns:
        Dictionary with 'keywords', 'summary', 'context', 'next_steps'
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    metadata = {
        'keywords': [],
        'summary': '',
        'context': '',
        'next_steps': ''
    }
    
    # Extract keywords
    keywords_match = re.search(r'\*\*Keywords\*\*:\s*(.+)', content)
    if keywords_match:
        keywords_str = keywords_match.group(1)
        metadata['keywords'] = [k.strip() for k in keywords_str.split(',')]
    
    # Extract summary
    summary_match = re.search(r'## Summary\n(.+?)(?=\n##|\Z)', content, re.DOTALL)
    if summary_match:
        metadata['summary'] = summary_match.group(1).strip()
    
    # Extract context
    context_match = re.search(r'## Context\n(.+?)(?=\n##|\Z)', content, re.DOTALL)
    if context_match:
        metadata['context'] = context_match.group(1).strip()
    
    # Extract next steps
    next_match = re.search(r'## Next Steps\n(.+?)(?=\n##|\Z)', content, re.DOTALL)
    if next_match:
        metadata['next_steps'] = next_match.group(1).strip()
    
    return metadata


def calculate_keyword_overlap(keywords1: List[str], keywords2: List[str]) -> int:
    """
    Calculate the number of overlapping keywords between two lists.
    
    Args:
        keywords1: First list of keywords
        keywords2: Second list of keywords
        
    Returns:
        Number of overlapping keywords
    """
    set1 = set(k.lower() for k in keywords1)
    set2 = set(k.lower() for k in keywords2)
    return len(set1 & set2)


def is_semantically_related(current_meta: Dict, other_meta: Dict) -> bool:
    """
    Determine if two sessions are semantically related based on their metadata.
    
    Args:
        current_meta: Metadata of current session
        other_meta: Metadata of other session
        
    Returns:
        True if sessions are related, False otherwise
    """
    # Check if summary/context/next_steps contain overlapping concepts
    current_text = ' '.join([
        current_meta.get('summary', ''),
        current_meta.get('context', ''),
        current_meta.get('next_steps', '')
    ]).lower()
    
    other_text = ' '.join([
        other_meta.get('summary', ''),
        other_meta.get('context', ''),
        other_meta.get('next_steps', '')
    ]).lower()
    
    # Check for keyword mentions in text
    current_keywords = set(k.lower() for k in current_meta.get('keywords', []))
    other_keywords = set(k.lower() for k in other_meta.get('keywords', []))
    
    # If current session's keywords appear in other session's text
    for keyword in current_keywords:
        if keyword in other_text:
            return True
    
    # If other session's keywords appear in current session's text
    for keyword in other_keywords:
        if keyword in current_text:
            return True
    
    return False


def find_related_sessions(
    journal_dir: Path,
    current_keywords: List[str],
    current_metadata: Dict = None,
    exclude_file: str = None
) -> List[Dict]:
    """
    Find related sessions based on keyword matching and semantic analysis.
    
    Args:
        journal_dir: Path to .dev-journal directory
        current_keywords: Keywords of current session
        current_metadata: Optional metadata dict of current session for deeper analysis
        exclude_file: Optional filename to exclude from results (current session)
        
    Returns:
        List of dictionaries with 'filename', 'overlap_count', 'related'
    """
    related = []
    
    # Get all markdown files except README.md
    session_files = [
        f for f in journal_dir.glob('*.md')
        if f.name != 'README.md' and f.name != exclude_file
    ]
    
    for filepath in session_files:
        try:
            metadata = extract_metadata_from_file(filepath)
            overlap = calculate_keyword_overlap(current_keywords, metadata['keywords'])
            
            if overlap > 0:
                is_related = False
                
                # If we have current metadata, do deeper semantic analysis
                if current_metadata:
                    is_related = is_semantically_related(current_metadata, metadata)
                else:
                    # Without metadata, just use keyword overlap threshold
                    is_related = overlap >= 1
                
                if is_related:
                    related.append({
                        'filename': filepath.name,
                        'overlap_count': overlap,
                        'keywords': metadata['keywords'],
                        'summary': metadata['summary']
                    })
        except Exception as e:
            print(f"Warning: Could not process {filepath.name}: {e}", file=sys.stderr)
            continue
    
    # Sort by overlap count (descending)
    related.sort(key=lambda x: x['overlap_count'], reverse=True)
    
    return related


def main():
    """Main entry point for the script."""
    if len(sys.argv) < 3:
        print("Usage: find_related_sessions.py <journal_dir> <keyword1,keyword2,...> [exclude_filename]")
        sys.exit(1)
    
    journal_dir = Path(sys.argv[1])
    keywords = [k.strip() for k in sys.argv[2].split(',')]
    exclude_file = sys.argv[3] if len(sys.argv) >= 4 else None
    
    if not journal_dir.exists():
        print(f"Error: Journal directory {journal_dir} does not exist", file=sys.stderr)
        sys.exit(1)
    
    related_sessions = find_related_sessions(journal_dir, keywords, exclude_file=exclude_file)
    
    # Print results as JSON-like format
    for session in related_sessions:
        print(f"{session['filename']}|{session['overlap_count']}|{','.join(session['keywords'])}")


if __name__ == "__main__":
    main()
