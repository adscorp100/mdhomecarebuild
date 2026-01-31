#!/usr/bin/env python3
"""
Tool Intent Gap Analyzer - GSC Edition

Analyzes Google Search Console data for each tool to identify:
1. What keywords the tool ranks for
2. Intent gaps - searches that land on the tool but may not be fully satisfied
3. Content gaps - features/info users want but the tool doesn't provide
4. Optimization opportunities
"""

import os
import sys
import argparse
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

# GSC API setup
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
CREDENTIALS_FILE = 'src/scripts/gsc_credentials.json'


def get_gsc_service():
    """Authenticate and return GSC service using service account"""

    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ Error: {CREDENTIALS_FILE} not found")
        print("Please ensure gsc_credentials.json is in src/scripts/")
        sys.exit(1)

    try:
        credentials = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE, scopes=SCOPES
        )
        service = build('searchconsole', 'v1', credentials=credentials, cache_discovery=False)
        return service
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        sys.exit(1)


def get_tool_keywords(service, site_url, tool_path, days=90):
    """Get all keywords that a specific tool ranks for"""

    end_date = datetime.now().date() - timedelta(days=3)  # GSC has 2-3 day lag
    start_date = end_date - timedelta(days=days)

    request = {
        'startDate': start_date.strftime('%Y-%m-%d'),
        'endDate': end_date.strftime('%Y-%m-%d'),
        'dimensions': ['query'],
        'dimensionFilterGroups': [{
            'filters': [{
                'dimension': 'page',
                'operator': 'contains',
                'expression': tool_path
            }]
        }],
        'rowLimit': 1000
    }

    try:
        response = service.searchanalytics().query(siteUrl=site_url, body=request).execute()

        if 'rows' not in response:
            return []

        keywords = []
        for row in response['rows']:
            keywords.append({
                'query': row['keys'][0],
                'clicks': row.get('clicks', 0),
                'impressions': row.get('impressions', 0),
                'ctr': row.get('ctr', 0) * 100,
                'position': row.get('position', 0)
            })

        return sorted(keywords, key=lambda x: x['clicks'], reverse=True)

    except Exception as e:
        print(f"❌ GSC query failed: {e}")
        return []


def analyze_intent_gaps(tool_name, keywords):
    """Analyze keywords to identify intent gaps"""

    gaps = {
        'high_value_mismatches': [],  # High traffic, but intent may not match
        'feature_requests': [],        # Users looking for features tool may not have
        'content_gaps': [],            # Users wanting info/guidance not in tool
        'comparison_queries': [],      # Users comparing or looking for alternatives
        'how_to_queries': [],          # Users wanting instructions/guidance
        'pricing_queries': [],         # Users asking about costs/rates
        'location_queries': [],        # Users wanting location-specific info
        'qualification_queries': []    # Users asking about requirements/eligibility
    }

    for kw in keywords:
        query = kw['query'].lower()

        # High impressions but low CTR = potential intent mismatch
        if kw['impressions'] > 50 and kw['ctr'] < 3:
            gaps['high_value_mismatches'].append({
                'query': kw['query'],
                'impressions': kw['impressions'],
                'ctr': kw['ctr'],
                'position': kw['position'],
                'issue': 'Low CTR despite good impressions - title/description may not match intent'
            })

        # Feature-related queries
        if any(term in query for term in ['calculator', 'tool', 'checker', 'estimator', 'planner']):
            if kw['clicks'] > 5:  # Only if getting actual traffic
                gaps['feature_requests'].append({
                    'query': kw['query'],
                    'clicks': kw['clicks'],
                    'note': 'User expecting specific calculator/tool features'
                })

        # How-to queries
        if any(term in query for term in ['how to', 'how do i', 'how can i', 'what is', 'guide']):
            gaps['how_to_queries'].append({
                'query': kw['query'],
                'clicks': kw['clicks'],
                'note': 'User wants instructions or explanation, not just calculator'
            })

        # Pricing/rate queries
        if any(term in query for term in ['pay rate', 'salary', 'cost', 'price', 'rates', 'wage', 'payment']):
            gaps['pricing_queries'].append({
                'query': kw['query'],
                'clicks': kw['clicks'],
                'note': 'User seeking specific pricing/rate information'
            })

        # Location queries
        if any(term in query for term in ['sydney', 'melbourne', 'nsw', 'vic', 'near me', 'australia']):
            gaps['location_queries'].append({
                'query': kw['query'],
                'clicks': kw['clicks'],
                'note': 'User wants location-specific information'
            })

        # Qualification/eligibility queries
        if any(term in query for term in ['qualify', 'eligible', 'requirements', 'need', 'apply']):
            gaps['qualification_queries'].append({
                'query': kw['query'],
                'clicks': kw['clicks'],
                'note': 'User asking about eligibility or requirements'
            })

        # Comparison queries
        if any(term in query for term in ['vs', 'versus', 'compare', 'difference', 'alternative', 'better']):
            gaps['comparison_queries'].append({
                'query': kw['query'],
                'clicks': kw['clicks'],
                'note': 'User comparing options or looking for alternatives'
            })

    return gaps


def generate_recommendations(tool_name, gaps, keywords):
    """Generate specific recommendations based on intent gaps"""

    recommendations = []

    # High-value mismatches
    if gaps['high_value_mismatches']:
        top_mismatches = sorted(gaps['high_value_mismatches'], key=lambda x: x['impressions'], reverse=True)[:5]
        recommendations.append({
            'priority': 'HIGH',
            'category': 'Title/Description Optimization',
            'issue': f"Found {len(gaps['high_value_mismatches'])} keywords with high impressions but low CTR",
            'action': 'Update meta title and description to better match search intent',
            'specific_queries': [m['query'] for m in top_mismatches],
            'details': 'These users are seeing your tool in search results but not clicking - your title/description may not clearly communicate what the tool does'
        })

    # How-to queries
    if gaps['how_to_queries'] and len(gaps['how_to_queries']) > 3:
        recommendations.append({
            'priority': 'MEDIUM',
            'category': 'Content Addition',
            'issue': f"Found {len(gaps['how_to_queries'])} 'how-to' queries",
            'action': 'Add instructional content above or below calculator',
            'specific_queries': [q['query'] for q in gaps['how_to_queries'][:5]],
            'details': 'Users want guidance/instructions, not just a calculator. Add step-by-step guide or FAQ section explaining how to use results'
        })

    # Pricing queries
    if gaps['pricing_queries'] and len(gaps['pricing_queries']) > 3:
        recommendations.append({
            'priority': 'MEDIUM',
            'category': 'Calculator Enhancement',
            'issue': f"Found {len(gaps['pricing_queries'])} pricing-related queries",
            'action': 'Add pricing breakdown or rate explanation to calculator output',
            'specific_queries': [q['query'] for q in gaps['pricing_queries'][:5]],
            'details': 'Users want specific pricing/rate info. Calculator results should include breakdown of rates, not just final number'
        })

    # Location queries
    if gaps['location_queries'] and len(gaps['location_queries']) > 2:
        recommendations.append({
            'priority': 'LOW',
            'category': 'Localization',
            'issue': f"Found {len(gaps['location_queries'])} location-specific queries",
            'action': 'Add location-specific information or state-based variations',
            'specific_queries': [q['query'] for q in gaps['location_queries'][:5]],
            'details': 'Users searching for location-specific info. Consider adding NSW vs VIC rate differences or regional information'
        })

    # Qualification queries
    if gaps['qualification_queries'] and len(gaps['qualification_queries']) > 2:
        recommendations.append({
            'priority': 'MEDIUM',
            'category': 'Content Addition',
            'issue': f"Found {len(gaps['qualification_queries'])} eligibility/requirement queries",
            'action': 'Add FAQ section explaining who qualifies or requirements',
            'specific_queries': [q['query'] for q in gaps['qualification_queries'][:5]],
            'details': 'Users asking about eligibility before using calculator. Add "Who qualifies?" or "Requirements" section'
        })

    # Comparison queries
    if gaps['comparison_queries']:
        recommendations.append({
            'priority': 'LOW',
            'category': 'Content Addition',
            'issue': f"Found {len(gaps['comparison_queries'])} comparison queries",
            'action': 'Add comparison section or alternative options',
            'specific_queries': [q['query'] for q in gaps['comparison_queries'][:3]],
            'details': 'Users comparing options. Consider adding "Alternatives" or "Compare with X" section'
        })

    return sorted(recommendations, key=lambda x: {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}[x['priority']])


def print_audit_report(tool_name, tool_path, keywords, gaps, recommendations):
    """Print comprehensive audit report"""

    print(f"\n{'='*100}")
    print(f"🔍 Tool Intent Gap Audit: {tool_name}")
    print(f"{'='*100}")

    print(f"\n📊 Overview:")
    print(f"Tool Path: {tool_path}")
    print(f"Total Keywords Ranking: {len(keywords)}")
    print(f"Total Clicks (90 days): {sum(k['clicks'] for k in keywords)}")
    print(f"Total Impressions (90 days): {sum(k['impressions'] for k in keywords)}")

    # Top performing keywords
    print(f"\n🏆 Top 10 Keywords by Clicks:")
    print(f"{'Keyword':<60} {'Clicks':<10} {'Impr':<10} {'CTR%':<8} {'Pos':<8}")
    print("-" * 96)
    for kw in keywords[:10]:
        print(f"{kw['query']:<60} {kw['clicks']:<10} {kw['impressions']:<10} {kw['ctr']:<8.1f} {kw['position']:<8.1f}")

    # Intent gaps
    print(f"\n⚠️  Intent Gap Analysis:")

    if gaps['high_value_mismatches']:
        print(f"\n❌ High Impressions, Low CTR (Intent Mismatch):")
        print(f"   Found {len(gaps['high_value_mismatches'])} keywords - title/description may not match search intent")
        for gap in gaps['high_value_mismatches'][:5]:
            print(f"   • {gap['query']} - {gap['impressions']} impressions, {gap['ctr']:.1f}% CTR")

    if gaps['how_to_queries']:
        print(f"\n📚 How-To Queries ({len(gaps['how_to_queries'])} found):")
        print(f"   Users want instructions/guidance, not just calculator")
        for gap in gaps['how_to_queries'][:5]:
            print(f"   • {gap['query']} - {gap['clicks']} clicks")

    if gaps['pricing_queries']:
        print(f"\n💰 Pricing Queries ({len(gaps['pricing_queries'])} found):")
        print(f"   Users seeking specific rate/pricing information")
        for gap in gaps['pricing_queries'][:5]:
            print(f"   • {gap['query']} - {gap['clicks']} clicks")

    if gaps['qualification_queries']:
        print(f"\n✅ Eligibility Queries ({len(gaps['qualification_queries'])} found):")
        print(f"   Users asking about requirements/qualifications")
        for gap in gaps['qualification_queries'][:5]:
            print(f"   • {gap['query']} - {gap['clicks']} clicks")

    if gaps['location_queries']:
        print(f"\n📍 Location Queries ({len(gaps['location_queries'])} found):")
        for gap in gaps['location_queries'][:3]:
            print(f"   • {gap['query']} - {gap['clicks']} clicks")

    if gaps['comparison_queries']:
        print(f"\n🔄 Comparison Queries ({len(gaps['comparison_queries'])} found):")
        for gap in gaps['comparison_queries'][:3]:
            print(f"   • {gap['query']} - {gap['clicks']} clicks")

    # Recommendations
    print(f"\n{'='*100}")
    print(f"💡 RECOMMENDATIONS:")
    print(f"{'='*100}")

    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. [{rec['priority']}] {rec['category']}")
        print(f"   Issue: {rec['issue']}")
        print(f"   Action: {rec['action']}")
        print(f"   Details: {rec['details']}")
        if rec['specific_queries']:
            print(f"   Example Queries:")
            for q in rec['specific_queries'][:3]:
                print(f"      • {q}")

    print(f"\n{'='*100}")
    print(f"✅ Audit complete!")
    print(f"{'='*100}\n")


def main():
    parser = argparse.ArgumentParser(description='Audit tool for intent gaps using GSC data')
    parser.add_argument('--tool', type=str, required=True, help='Tool path (e.g., /tools/ndis-pay-rate-calculator/)')
    parser.add_argument('--site', type=str, default='sc-domain:mdhomecare.com.au', help='GSC site URL')
    parser.add_argument('--days', type=int, default=90, help='Days of data to analyze (default: 90)')

    args = parser.parse_args()

    # Get GSC service
    print("🔐 Authenticating with Google Search Console...")
    service = get_gsc_service()

    # Get keywords
    print(f"📥 Fetching keywords for {args.tool}...")
    keywords = get_tool_keywords(service, args.site, args.tool, args.days)

    if not keywords:
        print(f"❌ No keywords found for {args.tool}")
        print("   This tool may not be indexed or has no search traffic")
        sys.exit(1)

    # Extract tool name from path
    tool_name = args.tool.strip('/').split('/')[-1].replace('-', ' ').title()

    # Analyze intent gaps
    print(f"🔍 Analyzing intent gaps...")
    gaps = analyze_intent_gaps(tool_name, keywords)

    # Generate recommendations
    print(f"💡 Generating recommendations...")
    recommendations = generate_recommendations(tool_name, gaps, keywords)

    # Print report
    print_audit_report(tool_name, args.tool, keywords, gaps, recommendations)


if __name__ == "__main__":
    main()
