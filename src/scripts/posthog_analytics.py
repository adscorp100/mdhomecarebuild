#!/usr/bin/env python3
"""
PostHog Analytics Query Script for MD Home Care

Query PostHog API for traffic analysis, AI referral tracking, and user behavior insights.
"""

import os
import sys
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

POSTHOG_API_KEY = os.getenv('POSTHOG_API_KEY')
POSTHOG_PROJECT_ID = os.getenv('POSTHOG_PROJECT_ID', '99267')  # Default project ID, update if needed

if not POSTHOG_API_KEY:
    print("❌ Error: POSTHOG_API_KEY not found in .env file")
    sys.exit(1)

BASE_URL = "https://us.posthog.com"  # or "https://eu.posthog.com" if EU instance


def query_posthog(query, params=None):
    """Execute a PostHog SQL query"""
    url = f"{BASE_URL}/api/projects/{POSTHOG_PROJECT_ID}/query/"

    headers = {
        "Authorization": f"Bearer {POSTHOG_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "query": {
            "kind": "HogQLQuery",
            "query": query
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None


def get_ai_referral_traffic(days=7):
    """Get AI referral traffic (ChatGPT, Perplexity, Claude, etc.)"""

    query = f"""
    SELECT
      properties.$pathname AS page,
      count(DISTINCT person_id) AS unique_users,
      count() AS total_pageviews,
      properties.$referring_domain AS referrer
    FROM events
    WHERE
      event = '$pageview'
      AND timestamp >= now() - INTERVAL {days} DAY
      AND (
        properties.$referring_domain ILIKE '%chatgpt%'
        OR properties.$referring_domain ILIKE '%perplexity%'
        OR properties.$referring_domain ILIKE '%claude.ai%'
        OR properties.$referring_domain ILIKE '%gemini%'
        OR properties.$referring_domain ILIKE '%copilot%'
      )
    GROUP BY page, referrer
    ORDER BY unique_users DESC
    LIMIT 20
    """

    print(f"\n📊 AI Referral Traffic (Last {days} Days)")
    print("=" * 80)

    result = query_posthog(query)

    if result and 'results' in result:
        results = result['results']

        if not results:
            print("No AI referral traffic found in the specified period.")
            return

        print(f"\n{'Page':<50} {'Referrer':<20} {'Users':<10} {'Views':<10}")
        print("-" * 90)

        total_users = 0
        total_views = 0

        for row in results:
            page = row[0] if row[0] else "(homepage)"
            referrer = row[3] if len(row) > 3 and row[3] else "Unknown"
            users = row[1]
            views = row[2]

            total_users += users
            total_views += views

            # Truncate long paths
            if len(page) > 47:
                page = page[:44] + "..."

            print(f"{page:<50} {referrer:<20} {users:<10} {views:<10}")

        print("-" * 90)
        print(f"{'TOTAL':<50} {'':<20} {total_users:<10} {total_views:<10}")
    else:
        print("Failed to retrieve data from PostHog")


def get_top_pages(days=7):
    """Get top pages by traffic"""

    query = f"""
    SELECT
      properties.$pathname AS page,
      count(DISTINCT person_id) AS unique_users,
      count() AS total_pageviews
    FROM events
    WHERE
      event = '$pageview'
      AND timestamp >= now() - INTERVAL {days} DAY
    GROUP BY page
    ORDER BY unique_users DESC
    LIMIT 20
    """

    print(f"\n📈 Top Pages (Last {days} Days)")
    print("=" * 80)

    result = query_posthog(query)

    if result and 'results' in result:
        results = result['results']

        print(f"\n{'Page':<60} {'Unique Users':<15} {'Total Views':<15}")
        print("-" * 90)

        for row in results:
            page = row[0] if row[0] else "(homepage)"
            users = row[1]
            views = row[2]

            if len(page) > 57:
                page = page[:54] + "..."

            print(f"{page:<60} {users:<15} {views:<15}")
    else:
        print("Failed to retrieve data from PostHog")


def get_referrer_breakdown(days=7):
    """Get traffic source breakdown"""

    query = f"""
    SELECT
      CASE
        WHEN properties.$referring_domain ILIKE '%google%' THEN 'Google'
        WHEN properties.$referring_domain ILIKE '%bing%' THEN 'Bing'
        WHEN properties.$referring_domain ILIKE '%chatgpt%' THEN 'ChatGPT'
        WHEN properties.$referring_domain ILIKE '%perplexity%' THEN 'Perplexity'
        WHEN properties.$referring_domain ILIKE '%claude%' THEN 'Claude'
        WHEN properties.$referring_domain ILIKE '%facebook%' THEN 'Facebook'
        WHEN properties.$referring_domain ILIKE '%linkedin%' THEN 'LinkedIn'
        WHEN properties.$referring_domain IS NULL THEN 'Direct'
        ELSE 'Other'
      END AS source,
      count(DISTINCT person_id) AS unique_users,
      count() AS total_pageviews
    FROM events
    WHERE
      event = '$pageview'
      AND timestamp >= now() - INTERVAL {days} DAY
    GROUP BY source
    ORDER BY unique_users DESC
    """

    print(f"\n🔍 Traffic Sources (Last {days} Days)")
    print("=" * 80)

    result = query_posthog(query)

    if result and 'results' in result:
        results = result['results']

        print(f"\n{'Source':<20} {'Unique Users':<15} {'Total Views':<15} {'% of Total':<15}")
        print("-" * 65)

        total_users = sum(row[1] for row in results)

        for row in results:
            source = row[0]
            users = row[1]
            views = row[2]
            percentage = (users / total_users * 100) if total_users > 0 else 0

            print(f"{source:<20} {users:<15} {views:<15} {percentage:<14.1f}%")

        print("-" * 65)
        print(f"{'TOTAL':<20} {total_users:<15} {sum(row[2] for row in results):<15} {'100.0%':<15}")
    else:
        print("Failed to retrieve data from PostHog")


def get_page_traffic(page_path, days=7):
    """Get detailed traffic for a specific page"""

    query = f"""
    SELECT
      toDate(timestamp) AS date,
      count(DISTINCT person_id) AS unique_users,
      count() AS total_pageviews,
      properties.$referring_domain AS referrer
    FROM events
    WHERE
      event = '$pageview'
      AND properties.$pathname = '{page_path}'
      AND timestamp >= now() - INTERVAL {days} DAY
    GROUP BY date, referrer
    ORDER BY date DESC, unique_users DESC
    """

    print(f"\n📄 Traffic for: {page_path} (Last {days} Days)")
    print("=" * 80)

    result = query_posthog(query)

    if result and 'results' in result:
        results = result['results']

        if not results:
            print(f"No traffic found for {page_path}")
            return

        print(f"\n{'Date':<15} {'Referrer':<30} {'Users':<10} {'Views':<10}")
        print("-" * 65)

        for row in results:
            date = row[0]
            users = row[1]
            views = row[2]
            referrer = row[3] if len(row) > 3 and row[3] else "Direct"

            if len(referrer) > 27:
                referrer = referrer[:24] + "..."

            print(f"{date:<15} {referrer:<30} {users:<10} {views:<10}")
    else:
        print("Failed to retrieve data from PostHog")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Query PostHog Analytics for MD Home Care')
    parser.add_argument('--ai-referrals', action='store_true', help='Show AI referral traffic (ChatGPT, Perplexity, etc.)')
    parser.add_argument('--top-pages', action='store_true', help='Show top pages by traffic')
    parser.add_argument('--sources', action='store_true', help='Show traffic source breakdown')
    parser.add_argument('--page', type=str, help='Get traffic for specific page path')
    parser.add_argument('--days', type=int, default=7, help='Number of days to analyze (default: 7)')
    parser.add_argument('--all', action='store_true', help='Run all reports')

    args = parser.parse_args()

    # If no specific report requested, show all
    if not any([args.ai_referrals, args.top_pages, args.sources, args.page, args.all]):
        args.all = True

    print(f"\n🏥 MD Home Care - PostHog Analytics Report")
    print(f"📅 Period: Last {args.days} days")
    print("=" * 80)

    if args.all or args.ai_referrals:
        get_ai_referral_traffic(args.days)

    if args.all or args.top_pages:
        get_top_pages(args.days)

    if args.all or args.sources:
        get_referrer_breakdown(args.days)

    if args.page:
        get_page_traffic(args.page, args.days)

    print("\n" + "=" * 80)
    print("✅ Analysis complete!\n")


if __name__ == "__main__":
    main()
