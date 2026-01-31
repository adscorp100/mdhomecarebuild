#!/usr/bin/env python3
"""
Analyze traffic specifically for /tools/ pages on MD Home Care
"""

import os
import sys
from dotenv import load_dotenv
import requests

load_dotenv()

POSTHOG_API_KEY = os.getenv('POSTHOG_API_KEY')
POSTHOG_PROJECT_ID = os.getenv('POSTHOG_PROJECT_ID')

if not POSTHOG_API_KEY or not POSTHOG_PROJECT_ID:
    print("❌ Error: POSTHOG_API_KEY or POSTHOG_PROJECT_ID not found in .env")
    sys.exit(1)

BASE_URL = "https://us.posthog.com"


def query_posthog(query):
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


def get_tools_traffic(days=30):
    """Get traffic for all tools pages"""

    query = f"""
    SELECT
      properties.$pathname AS tool_page,
      count(DISTINCT person_id) AS unique_users,
      count() AS total_pageviews,
      round(count() * 1.0 / count(DISTINCT person_id), 2) AS views_per_user
    FROM events
    WHERE
      event = '$pageview'
      AND properties.$pathname LIKE '/tools/%'
      AND timestamp >= now() - INTERVAL {days} DAY
    GROUP BY tool_page
    ORDER BY unique_users DESC
    """

    print(f"\n🛠️  Tools Traffic Analysis (Last {days} Days)")
    print("=" * 100)

    result = query_posthog(query)

    if result and 'results' in result:
        results = result['results']

        if not results:
            print("No tools traffic found")
            return

        print(f"\n{'Tool Page':<45} {'Unique Users':<15} {'Total Views':<15} {'Views/User':<15}")
        print("-" * 90)

        total_users = 0
        total_views = 0

        for row in results:
            tool = row[0]
            users = row[1]
            views = row[2]
            views_per_user = row[3]

            total_users += users
            total_views += views

            # Clean up tool name
            tool_name = tool.replace('/tools/', '')

            print(f"{tool_name:<45} {users:<15} {views:<15} {views_per_user:<15}")

        print("-" * 90)
        print(f"{'TOTAL':<45} {total_users:<15} {total_views:<15} {'-':<15}")

        return results
    else:
        print("Failed to retrieve data")
        return None


def get_tools_traffic_sources(days=30):
    """Get traffic sources for tools pages"""

    query = f"""
    SELECT
      properties.$pathname AS tool_page,
      CASE
        WHEN properties.$referring_domain ILIKE '%google%' THEN 'Google'
        WHEN properties.$referring_domain ILIKE '%bing%' THEN 'Bing'
        WHEN properties.$referring_domain ILIKE '%chatgpt%' THEN 'ChatGPT'
        WHEN properties.$referring_domain ILIKE '%perplexity%' THEN 'Perplexity'
        WHEN properties.$referring_domain IS NULL THEN 'Direct'
        ELSE 'Other'
      END AS source,
      count(DISTINCT person_id) AS unique_users
    FROM events
    WHERE
      event = '$pageview'
      AND properties.$pathname LIKE '/tools/%'
      AND timestamp >= now() - INTERVAL {days} DAY
    GROUP BY tool_page, source
    ORDER BY tool_page, unique_users DESC
    """

    print(f"\n📊 Traffic Sources by Tool (Last {days} Days)")
    print("=" * 100)

    result = query_posthog(query)

    if result and 'results' in result:
        results = result['results']

        current_tool = None
        for row in results:
            tool = row[0]
            source = row[1]
            users = row[2]

            if tool != current_tool:
                if current_tool:
                    print()
                tool_name = tool.replace('/tools/', '')
                print(f"\n{tool_name}:")
                print("-" * 50)
                current_tool = tool

            print(f"  {source:<20} {users:>10} users")


def get_tools_engagement(days=30):
    """Get engagement metrics for tools"""

    query = f"""
    SELECT
      properties.$pathname AS tool_page,
      count(DISTINCT person_id) AS unique_users,
      quantile(0.5)(events.properties.$session_duration) AS median_session_duration,
      quantile(0.5)(events.properties.$scroll_depth_percentage) AS median_scroll_depth
    FROM events
    WHERE
      event = '$pageview'
      AND properties.$pathname LIKE '/tools/%'
      AND timestamp >= now() - INTERVAL {days} DAY
    GROUP BY tool_page
    ORDER BY unique_users DESC
    """

    print(f"\n📈 Tools Engagement Metrics (Last {days} Days)")
    print("=" * 100)

    result = query_posthog(query)

    if result and 'results' in result:
        results = result['results']

        print(f"\n{'Tool Page':<45} {'Users':<10} {'Median Duration (s)':<20} {'Median Scroll %':<20}")
        print("-" * 95)

        for row in results:
            tool = row[0]
            users = row[1]
            duration = row[2] if len(row) > 2 and row[2] else 0
            scroll = row[3] if len(row) > 3 and row[3] else 0

            tool_name = tool.replace('/tools/', '')

            print(f"{tool_name:<45} {users:<10} {duration:<20.1f} {scroll:<20.0f}%")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Analyze MD Home Care Tools Traffic')
    parser.add_argument('--days', type=int, default=30, help='Number of days to analyze (default: 30)')
    parser.add_argument('--sources', action='store_true', help='Show traffic sources breakdown')
    parser.add_argument('--engagement', action='store_true', help='Show engagement metrics')

    args = parser.parse_args()

    print(f"\n🏥 MD Home Care - Tools Traffic Analysis")
    print(f"📅 Period: Last {args.days} days")
    print("=" * 100)

    # Always show basic traffic
    get_tools_traffic(args.days)

    if args.sources:
        get_tools_traffic_sources(args.days)

    if args.engagement:
        get_tools_engagement(args.days)

    print("\n" + "=" * 100)
    print("✅ Analysis complete!\n")


if __name__ == "__main__":
    main()
