#!/usr/bin/env python3
"""
Fix bogus 2026 dates that should be 2025 in MDH blog posts.
Changes body content only (preserves frontmatter).
"""

import re
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

def fix_body_dates(body_text):
    """Replace 2026 with 2025 in specific patterns in body text."""
    original = body_text
    fixes = []
    
    # Pattern 1: "Last updated: Month DD, 2026" -> 2025
    pattern = r'((?:Last|last)\s+updated:?\s+[A-Za-z]+\s+\d{1,2},?\s+)2026'
    matches = list(re.finditer(pattern, body_text))
    for match in matches:
        fixes.append(f"Last updated date: {match.group()}")
    body_text = re.sub(pattern, r'\g<1>2025', body_text)
    
    # Pattern 2: "Updated: Month DD, 2026" -> 2025
    pattern = r'((?:Updated|updated):?\s+[A-Za-z]+\s+\d{1,2},?\s+)2026'
    matches = list(re.finditer(pattern, body_text))
    for match in matches:
        fixes.append(f"Updated date: {match.group()}")
    body_text = re.sub(pattern, r'\g<1>2025', body_text)
    
    # Pattern 3: "Published: Month DD, 2026" -> 2025
    pattern = r'((?:Published|published):?\s+[A-Za-z]+\s+\d{1,2},?\s+)2026'
    matches = list(re.finditer(pattern, body_text))
    for match in matches:
        fixes.append(f"Published date: {match.group()}")
    body_text = re.sub(pattern, r'\g<1>2025', body_text)
    
    # Pattern 4: "DD Month 2026" (e.g., "24 November 2026") -> 2025
    pattern = r'(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+)2026'
    matches = list(re.finditer(pattern, body_text))
    for match in matches:
        fixes.append(f"DD Month 2026: {match.group()}2026")
    body_text = re.sub(pattern, r'\g<1>2025', body_text)
    
    # Pattern 5: "Month 2026" (e.g., "February 2026") -> 2025
    # But be careful - only fix if it looks like it's referencing past dates
    # Check context for words like "updated", "effective", "as of", "in", "from", "report"
    pattern = r'((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+)2026'
    matches = list(re.finditer(pattern, body_text))
    for match in matches:
        # Get context around the match
        start = max(0, match.start() - 100)
        end = min(len(body_text), match.end() + 50)
        context = body_text[start:end].lower()
        
        # Look for indicators this is a past/current date reference
        indicators = ['updated', 'effective', 'as of', 'in ', 'from ', 'report', 
                      'published', 'released', 'survey', 'data', 'source:', 'current']
        
        if any(ind in context for ind in indicators):
            fixes.append(f"Month 2026: {match.group()}2026")
    
    body_text = re.sub(pattern, r'\g<1>2025', body_text)
    
    # Pattern 6: Abbreviated months "Jan 2026", "Feb 2026", etc. -> 2025
    pattern = r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+)2026'
    matches = list(re.finditer(pattern, body_text))
    for match in matches:
        fixes.append(f"Abbreviated month: {match.group()}2026")
    body_text = re.sub(pattern, r'\g<1>2025', body_text)
    
    # Pattern 7: "as of 2026" or "As of 2026" -> 2025
    pattern = r'([Aa]s of\s+)2026'
    matches = list(re.finditer(pattern, body_text))
    for match in matches:
        fixes.append(f"as of 2026: {match.group()}")
    body_text = re.sub(pattern, r'\g<1>2025', body_text)
    
    # Pattern 8: ISO dates "2026-MM-DD" -> "2025-MM-DD"
    pattern = r'2026-(\d{2}-\d{2})'
    matches = list(re.finditer(pattern, body_text))
    for match in matches:
        fixes.append(f"ISO date: 2026-{match.group(1)}")
    body_text = re.sub(pattern, r'2025-\1', body_text)
    
    return body_text, fixes, body_text != original

def main():
    print("🔧 Fixing bogus 2026 dates in MDH blog posts...\n")
    
    # Files to fix (from our scan results)
    files_to_fix = [
        'accc-ndis-provider-exploitation-report.md',
        'accho-aboriginal-community-controlled-health-organisations-complete-guide.md',
        'autism-school-holiday-programs-melbourne.md',
        'chsp-providers-complete-guide-australia.md',
        'disability-support-worker-salary-pay-rates-australia.md',
        'guide-buying-selling-donating-second-hand-disability-equipment-australia.md',
        'home-care-package-level-2.md',
        'how-to-choose-a-good-provider.md',
        'how-to-find-ndis-clients-occupational-therapy.md',
        'how-to-get-physiotherapy-clients-ndis.md',
        'how-to-get-support-worker-insurance-in-australia.md',
        'how-to-start-a-successful-ndis-business-in-australia.md',
        'mable-support-workers-ndis-complete-guide.md',
        'myplace-portal-ndis-complete-guide.md',
        'ndis-application-support-help-guide.md',
        'ndis-capacity-building-supports-complete-guide.md',
        'ndis-improved-daily-living-cb-daily-activity-guide.md',
        'ndis-invoice-template-guide.md',
        'ndis-key-worker-model-complete-guide.md',
        'ndis-line-items-guide-2024-25.md',
        'ndis-news-latest-updates-australia.md',
        'ndis-pace-system-participant-guide.md',
        'ndis-podiatry-client-acquisition.md',
        'ndis-price-guide.md',
        'ndis-psychology-practice-growth-without-ads.md',
        'ndis-reportable-incidents-complete-guide.md',
        'ndis-reports-carer-impact-statements-templates-examples.md',
        'ndis-respite-sta-accommodation-guide.md',
        'ndis-schedule-of-supports-template-guide.md',
        'ndis-social-community-participation-guide.md',
        'ndis-support-worker-hourly-rate.md',
        'ndis-support-worker-pay-rates.md',
        'new-aged-care-support-at-home-program.md',
        'personal-accident-insurance-sole-trader-support-workers.md',
        'refundable-accommodation-deposit-rad-guide.md',
        'sda-calculator-specialist-disability-accommodation.md',
        'self-managed-home-care-packages-australia.md',
        'selling-deceased-estate-property-australia.md',
        'support-at-home-prices.md',
        'support-at-home-program-complete-guide.md',
        'support-coordinator-ndis-client-base-building.md',
        'support-coordinator-progress-report-template-ndis.md',
        'top-20-ndis-providers-melbourne.md',
        'what-makes-a-truly-great-disability-support-worker-australia.md',
    ]
    
    files_fixed = 0
    total_changes = 0
    all_fixes = defaultdict(list)
    
    for filename in files_to_fix:
        filepath = BLOG_DIR / filename
        
        if not filepath.exists():
            print(f"⚠️  {filename} not found, skipping")
            continue
        
        try:
            # Read file
            content = filepath.read_text(encoding='utf-8')
            frontmatter, body = split_frontmatter(content)
            
            # Fix dates in body only
            fixed_body, fixes, changed = fix_body_dates(body)
            
            if changed:
                # Write back
                new_content = frontmatter + fixed_body
                filepath.write_text(new_content, encoding='utf-8')
                
                files_fixed += 1
                total_changes += len(fixes)
                all_fixes[filename] = fixes
                
                print(f"✅ {filename}")
                print(f"   Fixed {len(fixes)} date(s)")
                
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
    
    print(f"\n{'='*80}")
    print(f"📊 SUMMARY")
    print(f"{'='*80}")
    print(f"Files fixed: {files_fixed}")
    print(f"Total changes: {total_changes}")
    
    # Save fix log
    log_path = BLOG_DIR.parent.parent.parent / "date_fixes_applied.txt"
    with open(log_path, 'w') as f:
        f.write("MDH Blog Date Fixes Applied\n")
        f.write("="*80 + "\n\n")
        f.write(f"Files fixed: {files_fixed}\n")
        f.write(f"Total changes: {total_changes}\n\n")
        
        for filename, fixes in sorted(all_fixes.items()):
            f.write(f"\n{filename}\n")
            f.write("-" * len(filename) + "\n")
            for fix in fixes:
                f.write(f"  • {fix}\n")
    
    print(f"\n💾 Fix log saved to: {log_path}")
    print("\n✨ All fixes complete!")

if __name__ == "__main__":
    main()
