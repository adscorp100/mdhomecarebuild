#!/usr/bin/env python3
"""
Advanced GSC SEO Analyzer
=========================
This tool provides a comprehensive SEO analysis for a given page, including
momentum tracking, striking distance opportunities, and SERP feature analysis.

Usage:
    python scripts/advanced_gsc_analyzer.py --page "/fr/features/ai-summarizer"
"""

import argparse
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlparse

try:
    from googleapiclient.discovery import build
    from google.oauth2 import service_account
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install google-api-python-client google-auth-oauthlib google-auth-httplib2 requests beautifulsoup4")
    sys.exit(1)


def find_credentials_file(default_path: str) -> str:
    """
    Smart credential file detection.
    Checks multiple paths to handle running from different directories.
    """
    # Paths to check in order of preference
    paths_to_check = [
        default_path,  # User-provided or default path
        'gsc_credentials.json',  # If running from scripts directory
        'src/scripts/gsc_credentials.json',  # If running from project root
    ]
    
    for path in paths_to_check:
        if os.path.exists(path):
            return path
    
    # If none found, provide helpful error message
    print("❌ Credentials file not found. Checked the following paths:")
    for path in paths_to_check:
        print(f"   - {path}")
    print("\nMake sure gsc_credentials.json exists in either:")
    print("   - Current directory (if running from scripts/)")
    print("   - scripts/ directory (if running from project root)")
    print("   - Or specify custom path with --credentials parameter")
    sys.exit(1)


class AdvancedGSCAnalyzer:
    """Advanced GSC query and SEO analysis tool."""
    
    def __init__(self, credentials_path: str):
        self.credentials_path = credentials_path
        self.service = None

    def authenticate(self):
        """Authenticate with GSC API."""
        try:
            scopes = ['https://www.googleapis.com/auth/webmasters.readonly']
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path, scopes=scopes
            )
            self.service = build('searchconsole', 'v1', credentials=credentials, cache_discovery=False)
            print("✅ Connected to Google Search Console")
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            sys.exit(1)

    def get_sites(self) -> List[str]:
        """Get available sites."""
        if not self.service:
            return []
        sites = self.service.sites().list().execute()
        return [site['siteUrl'] for site in sites.get('siteEntry', [])]

    def query_gsc_data(self, site: str, start_date: str, end_date: str, page_filter: str, limit: int = 250) -> List[Dict]:
        """Query GSC data for a specific date range."""
        request_body = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': ['query'],
            'dimensionFilterGroups': [{'filters': [{'dimension': 'page', 'operator': 'contains', 'expression': page_filter}]}],
            'rowLimit': limit
        }
        try:
            if not self.service:
                return []
            response = self.service.searchanalytics().query(siteUrl=site, body=request_body).execute()
            return response.get('rows', [])
        except Exception as e:
            print(f"❌ GSC query failed: {e}")
            return []

    def query_gsc_data_by_keyword(self, site: str, start_date: str, end_date: str, keyword_filter: str, limit: int = 50) -> List[Dict]:
        """Query GSC data for a specific keyword to find ranking pages."""
        request_body = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': ['page'],
            'dimensionFilterGroups': [{'filters': [{'dimension': 'query', 'operator': 'contains', 'expression': keyword_filter}]}],
            'rowLimit': limit
        }
        try:
            if not self.service:
                return []
            response = self.service.searchanalytics().query(siteUrl=site, body=request_body).execute()
            # Sort by impressions before returning
            rows = response.get('rows', [])
            rows.sort(key=lambda x: x['impressions'], reverse=True)
            return rows
        except Exception as e:
            print(f"❌ GSC query for keyword '{keyword_filter}' failed: {e}")
            return []

    def analyze_momentum(self, data_90d: List[Dict], data_7d: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """Identify rising and fading keywords based on position changes, weighted by volume."""
        query_data_90d = {row['keys'][0]: row for row in data_90d}
        query_data_7d = {row['keys'][0]: row for row in data_7d}

        rising_stars = []
        fading_giants = []

        for query, data_7 in query_data_7d.items():
            if query in query_data_90d:
                data_90 = query_data_90d[query]
                
                pos_7d = data_7['position']
                pos_90d = data_90['position']
                position_change = pos_90d - pos_7d
                
                # Get volume data (prioritize 7-day for recent trends, 90-day for stability)
                clicks_7d = data_7.get('clicks', 0)
                impressions_7d = data_7.get('impressions', 0)
                clicks_90d = data_90.get('clicks', 0)
                impressions_90d = data_90.get('impressions', 0)
                
                # Calculate volume score (blend recent and long-term data)
                volume_score = (impressions_7d * 2 + impressions_90d) / 3 + (clicks_7d * 10 + clicks_90d * 5)
                
                # Only consider keywords with meaningful volume and position change
                if volume_score >= 10 and abs(position_change) > 2:
                    keyword_data = {
                        'query': query,
                        'pos_90d': pos_90d,
                        'pos_7d': pos_7d,
                        'change': position_change,
                        'clicks_7d': clicks_7d,
                        'clicks_90d': clicks_90d,
                        'impressions_7d': impressions_7d,
                        'impressions_90d': impressions_90d,
                        'volume_score': volume_score
                    }
                    
                    if position_change > 2:  # Improved by more than 2 positions
                        rising_stars.append(keyword_data)
                    elif position_change < -2:  # Dropped by more than 2 positions
                        fading_giants.append(keyword_data)
        
        # Sort by volume-weighted impact (position change * volume score)
        rising_stars.sort(key=lambda x: x['change'] * x['volume_score'], reverse=True)
        fading_giants.sort(key=lambda x: abs(x['change']) * x['volume_score'], reverse=True)
        
        return rising_stars, fading_giants

    def find_striking_distance(self, data_90d: List[Dict]) -> List[Dict]:
        """Find keywords with high impressions in positions 11-20."""
        opportunities = [
            row for row in data_90d 
            if 11 <= row['position'] <= 20 and row['impressions'] > 50
        ]
        opportunities.sort(key=lambda x: x['impressions'], reverse=True)
        return opportunities

    def analyze_serp(self, query: str) -> Tuple[List[str], List[str]]:
        """Scrape Google SERP for features and 'People Also Ask' questions."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            response = requests.get(f"https://www.google.com/search?q={query.replace(' ', '+')}&hl=en", headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"❌ SERP analysis failed: {e}")
            return [], []

        soup = BeautifulSoup(response.text, 'html.parser')
        features = []
        paa_questions = []

        if soup.find("div", {"class": "O3Q5dd"}): features.append("Video Carousel")
        if soup.find("div", {"class": "related-question-pair"}): features.append("People Also Ask")
        if soup.find("div", {"class": "ULSxyf"}): features.append("Image Pack")
        if soup.find("g-scrolling-carousel"): features.append("Top Stories/Carousel")
        
        paa_divs = soup.find_all("div", {"class": "related-question-pair"})
        for div in paa_divs:
            question = div.find("div", {"role": "heading"})
            if question:
                paa_questions.append(question.get_text(strip=True))
                
        return features, paa_questions

    def print_analysis(self, page_filter: str, top_keyword: str, momentum: Tuple, striking_distance: List, serp: Tuple, top_keywords: List):
        rising, fading = momentum
        serp_features, paa = serp

        print(f"\n\n📊 Full SEO Analysis for page: {page_filter}")
        print("=" * 120)

        print("\n📈 Momentum Analysis (90 days vs 7 days)")
        print("-" * 120)
        print("🚀 Rising Stars (Position improved >2, volume-weighted)")
        print(f"{'Keyword':<45} {'90d Pos':<8} {'7d Pos':<8} {'Change':<8} {'90d Clicks':<10} {'7d Clicks':<10} {'90d Impr':<10} {'7d Impr':<10}")
        print("-" * 120)
        for r in rising[:8]:
            print(f"{r['query']:<45} {r['pos_90d']:<8.1f} {r['pos_7d']:<8.1f} {r['change']:<+8.1f} {r['clicks_90d']:<10} {r['clicks_7d']:<10} {r['impressions_90d']:<10} {r['impressions_7d']:<10}")
        
        print("\n📉 Fading Giants (Position dropped >2, volume-weighted)")
        print(f"{'Keyword':<45} {'90d Pos':<8} {'7d Pos':<8} {'Change':<8} {'90d Clicks':<10} {'7d Clicks':<10} {'90d Impr':<10} {'7d Impr':<10}")
        print("-" * 120)
        for f in fading[:8]:
            print(f"{f['query']:<45} {f['pos_90d']:<8.1f} {f['pos_7d']:<8.1f} {f['change']:<+8.1f} {f['clicks_90d']:<10} {f['clicks_7d']:<10} {f['impressions_90d']:<10} {f['impressions_7d']:<10}")

        print("\n\n🎯 Striking Distance Opportunities (Positions 11-20, >50 impressions)")
        print("-" * 120)
        print(f"{'Keyword':<50} {'Position':<12} {'Clicks':<8} {'Impressions':<12}")
        print("-" * 120)
        for s in striking_distance[:8]:
            print(f"{s['keys'][0]:<50} {s['position']:<12.1f} {s.get('clicks', 0):<8} {s['impressions']:<12}")
        
        print(f"\n\n🔍 SERP Analysis for top keyword: '{top_keyword}'")
        print("-" * 120)
        if serp_features:
            print("Detected SERP Features:", ", ".join(serp_features))
        else:
            print("No special SERP features detected.")
        
        if paa:
            print("\nPeople Also Ask Questions:")
            for q in paa: print(f"  - {q}")

        print("\n\n📋 Top 15 Keywords (Last 90 days by clicks)")
        print("-" * 120)
        print(f"{'Keyword':<50} {'Clicks':<8} {'Impressions':<12} {'CTR%':<8} {'Position':<10}")
        print("-" * 120)
        for k in top_keywords[:15]:
            ctr = (k.get('clicks', 0) / k.get('impressions', 1)) * 100 if k.get('impressions', 0) > 0 else 0
            print(f"{k['keys'][0]:<50} {k.get('clicks', 0):<8} {k.get('impressions', 0):<12} {ctr:<8.1f} {k.get('position', 0):<10.1f}")

def main():
    parser = argparse.ArgumentParser(
        description='Advanced GSC SEO Analyzer. Use --page for full page analysis or --keyword for cannibalization checks.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--credentials', default='scripts/gsc_credentials.json', help='Credentials file (auto-detects if not specified)')
    parser.add_argument('--site', help='Site URL (e.g., "https://mdhomecare.com.au"). Optional - will use first available.')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--page', help='Page URI to analyze (e.g., "/blog/my-post" or full URL)')
    group.add_argument('--keyword', help='Keyword to check for cannibalization (e.g., "ndis price guide")')

    args = parser.parse_args()

    # Smart credential file detection
    credentials_path = find_credentials_file(args.credentials)
    analyzer = AdvancedGSCAnalyzer(credentials_path)
    analyzer.authenticate()

    site = args.site
    if not site:
        sites = analyzer.get_sites()
        if not sites:
            print("❌ No sites found in GSC account.")
            sys.exit(1)
        # Find the main site automatically. Prioritize domain property.
        domain_property = next((s for s in sites if 'sc-domain:' in s), None)
        if domain_property:
            site = domain_property
        else:
            # Fallback to the first non-domain property if available, otherwise first site
            site = next((s for s in sites if 'sc-domain:' not in s), sites[0])
        print(f"✅ Using auto-detected site: {site}")
    
    start_date_90d = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')

    if args.keyword:
        print(f"\n🔎 Checking for keyword cannibalization for: '{args.keyword}'")
        print(f"   (Data from last 90 days for site: {site})")
        
        keyword_data = analyzer.query_gsc_data_by_keyword(site, start_date_90d, end_date, args.keyword)
        
        if not keyword_data:
            print("\n✅ No pages found ranking for this keyword or similar terms. It's safe to create a new post.")
            sys.exit(0)
            
        print("\n⚠️  The following pages are already ranking for this keyword or similar terms (sorted by impressions):")
        print("-" * 110)
        print(f"{'Page URL':<70} {'Impressions':<15} {'Clicks':<10} {'Position':<10}")
        print("-" * 110)
        
        for row in keyword_data:
            page_url = row['keys'][0] # Keep the full URL for clarity
            impressions = row['impressions']
            clicks = row['clicks']
            position = row['position']
            print(f"{page_url:<70} {impressions:<15} {clicks:<10} {position:<10.1f}")
            
        print("\n💡 Recommendation: Instead of creating a new post, consider updating the top-ranking page with your new content.")
        sys.exit(0)

    if args.page:
        page_filter = args.page
        # If a full URL is provided, extract just the path for filtering.
        # This makes the filter more reliable, especially for domain properties.
        if page_filter.startswith('http'):
            page_filter = urlparse(page_filter).path

        # Proceed with original page analysis logic
        start_date_7d = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

        print(f"\n🚀 Fetching data for page containing path: '{page_filter}'")
        print(f"   (This may take a moment...)")
        
        data_90d = analyzer.query_gsc_data(site, start_date_90d, end_date, page_filter, limit=1000)
        data_7d = analyzer.query_gsc_data(site, start_date_7d, end_date, page_filter, limit=1000)

        if not data_90d:
            print(f"❌ No data found for pages containing '{page_filter}' in the last 90 days.")
            sys.exit(1)
            
        # Get top keyword for SERP analysis
        top_keyword_by_clicks = sorted(data_90d, key=lambda x: x.get('clicks', 0), reverse=True)[0]['keys'][0]
        
        momentum = analyzer.analyze_momentum(data_90d, data_7d)
        striking_distance = analyzer.find_striking_distance(data_90d)
        serp = analyzer.analyze_serp(top_keyword_by_clicks)
        
        # Get top keywords sorted by clicks for the final report
        top_keywords_sorted = sorted(data_90d, key=lambda x: x.get('clicks', 0), reverse=True)

        analyzer.print_analysis(page_filter, top_keyword_by_clicks, momentum, striking_distance, serp, top_keywords_sorted)


if __name__ == '__main__':
    main() 