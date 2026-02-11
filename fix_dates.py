#!/usr/bin/env python3
"""
Scan MDH blog posts for bogus 2026 dates that should be 2025.
Focus on body content only (skip frontmatter).
"""

import re
import os
from pathlib import Path
from collections import defaultdict

BLOG_DIR = Path.home() / "Projects/mdhomecarebuild/src/content/blog"

def split_frontmatter(content):
    """Split content into frontmatter and body."""
    if not content.startswith('---'):
        return "", content
    
    parts = content.split('---', 2)
    if len(parts) >= 3:
        return f"---{parts[1]}---", parts[2]
    return "", content

def find_2026_patterns(body_text, filename):
    """Find instances of 2026 in body that should be 2025."""
    issues = []
    
    # Patterns that likely indicate wrong dates
    patterns = [
        # "Last updated: February 11, 2026" style
        (r'(Last updated:?\s+[A-Za-z]+\s+\d{1,2},?\s+)2026', 'Last updated date'),
        (r'(Updated:?\s+[A-Za-z]+\s+\d{1,2},?\s+)2026', 'Updated date'),
        (r'(Published:?\s+[A-Za-z]+\s+\d{1,2},?\s+)2026', 'Published date'),
        
        # "February 2026" in context that looks like past/current
        (r'(January\s+)2026', 'January 2026'),
        (r'(February\s+)2026', 'February 2026'),
        (r'(March\s+)2026', 'March 2026'),
        (r'(April\s+)2026', 'April 2026'),
        (r'(May\s+)2026', 'May 2026'),
        (r'(June\s+)2026', 'June 2026'),
        (r'(July\s+)2026', 'July 2026'),
        (r'(August\s+)2026', 'August 2026'),
        (r'(September\s+)2026', 'September 2026'),
        (r'(October\s+)2026', 'October 2026'),
        (r'(November\s+)2026', 'November 2026'),
        (r'(December\s+)2026', 'December 2026'),
        
        # "11 February 2026" style
        (r'(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+)2026', 'DD Month 2026'),
        
        # "Feb 2026" abbreviated months
        (r'(Jan\s+)2026', 'Jan 2026'),
        (r'(Feb\s+)2026', 'Feb 2026'),
        (r'(Mar\s+)2026', 'Mar 2026'),
        (r'(Apr\s+)2026', 'Apr 2026'),
        (r'(Jun\s+)2026', 'Jun 2026'),
        (r'(Jul\s+)2026', 'Jul 2026'),
        (r'(Aug\s+)2026', 'Aug 2026'),
        (r'(Sep\s+)2026', 'Sep 2026'),
        (r'(Oct\s+)2026', 'Oct 2026'),
        (r'(Nov\s+)2026', 'Nov 2026'),
        (r'(Dec\s+)2026', 'Dec 2026'),
        
        # Context-based: "as of 2026", "in 2026" when discussing current/past things
        (r'(as of\s+)2026', 'as of 2026'),
        (r'(As of\s+)2026', 'As of 2026'),
        
        # ISO dates
        (r'2026-(\d{2}-\d{2})', '2026-MM-DD format'),
    ]
    
    for pattern, pattern_name in patterns:
        matches = list(re.finditer(pattern, body_text, re.IGNORECASE))
        for match in matches:
            # Get surrounding context (50 chars before and after)
            start = max(0, match.start() - 50)
            end = min(len(body_text), match.end() + 50)
            context = body_text[start:end].replace('\n', ' ')
            
            issues.append({
                'pattern': pattern_name,
                'match': match.group(),
                'context': context,
                'position': match.start()
            })
    
    return issues

def main():
    print("🔍 Scanning MDH blog posts for bogus 2026 dates...\n")
    
    files_scanned = 0
    files_with_2026 = 0
    files_with_issues = 0
    all_issues = defaultdict(list)
    
    # Get list of files with 2026
    md_files = sorted(BLOG_DIR.glob("*.md"))
    
    for filepath in md_files:
        files_scanned += 1
        
        try:
            content = filepath.read_text(encoding='utf-8')
            frontmatter, body = split_frontmatter(content)
            
            # Check if body contains 2026
            if '2026' not in body:
                continue
            
            files_with_2026 += 1
            
            # Find problematic patterns
            issues = find_2026_patterns(body, filepath.name)
            
            if issues:
                files_with_issues += 1
                all_issues[filepath.name] = issues
                
        except Exception as e:
            print(f"❌ Error reading {filepath.name}: {e}")
    
    # Report findings
    print(f"📊 SCAN RESULTS")
    print(f"{'='*80}")
    print(f"Files scanned: {files_scanned}")
    print(f"Files with '2026' in body: {files_with_2026}")
    print(f"Files with problematic 2026 dates: {files_with_issues}")
    print()
    
    if all_issues:
        print(f"🐛 DETAILED FINDINGS")
        print(f"{'='*80}\n")
        
        pattern_counts = defaultdict(int)
        
        for filename, issues in sorted(all_issues.items()):
            print(f"📄 {filename}")
            print(f"   Found {len(issues)} issue(s):")
            for issue in issues:
                print(f"   • {issue['pattern']}: {issue['match']}")
                print(f"     Context: ...{issue['context']}...")
                pattern_counts[issue['pattern']] += 1
            print()
        
        print(f"\n📈 PATTERN SUMMARY")
        print(f"{'='*80}")
        for pattern, count in sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {pattern}: {count} occurrences")
    else:
        print("✅ No problematic 2026 dates found in body content!")
    
    # Save detailed report
    report_path = BLOG_DIR.parent.parent.parent / "date_fix_report.txt"
    with open(report_path, 'w') as f:
        f.write(f"MDH Blog Date Fix Report\n")
        f.write(f"="*80 + "\n\n")
        f.write(f"Files scanned: {files_scanned}\n")
        f.write(f"Files with '2026' in body: {files_with_2026}\n")
        f.write(f"Files with problematic dates: {files_with_issues}\n\n")
        
        for filename, issues in sorted(all_issues.items()):
            f.write(f"\n{filename}\n")
            f.write("-" * len(filename) + "\n")
            for issue in issues:
                f.write(f"  Pattern: {issue['pattern']}\n")
                f.write(f"  Match: {issue['match']}\n")
                f.write(f"  Context: ...{issue['context']}...\n\n")
    
    print(f"\n💾 Full report saved to: {report_path}")
    return files_scanned, files_with_2026, files_with_issues, all_issues

if __name__ == "__main__":
    main()
