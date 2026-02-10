#!/usr/bin/env python3
"""
MD Home Care - SEO Recovery Dry Run
Checks PostHog for traffic drops (24h vs same 24h last week)
and GSC for keyword/position context.
"""

import requests
import json
from datetime import datetime, timedelta, timezone

# PostHog config
POSTHOG_API_KEY = "phx_aaY9c0iM3ln1CN6Pgs77w7XhveMqROqRqKjGm2gQ43OJy8E"
POSTHOG_PROJECT_ID = "154606"
POSTHOG_URL = f"https://us.i.posthog.com/api/projects/{POSTHOG_PROJECT_ID}/query/"

HEADERS = {
    "Authorization": f"Bearer {POSTHOG_API_KEY}",
    "Content-Type": "application/json"
}

# Current time in AEDT (UTC+11)
now_utc = datetime.now(timezone.utc)
# Compare last 24h vs same 24h one week ago
end_this = now_utc
start_this = end_this - timedelta(hours=24)
end_last = end_this - timedelta(days=7)
start_last = start_this - timedelta(days=7)

def fmt(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def query_posthog(start, end, label):
    query = f"""
    SELECT
        properties.$pathname AS path,
        count() AS views
    FROM events
    WHERE event = '$pageview'
      AND timestamp >= '{fmt(start)}'
      AND timestamp < '{fmt(end)}'
      AND properties.$pathname NOT LIKE '%?%'
      AND properties.$pathname != '/'
    GROUP BY path
    HAVING views >= 2
    ORDER BY views DESC
    LIMIT 500
    """
    
    resp = requests.post(POSTHOG_URL, headers=HEADERS, json={
        "query": {"kind": "HogQLQuery", "query": query}
    })
    
    if resp.status_code != 200:
        print(f"PostHog error ({label}): {resp.status_code} - {resp.text[:200]}")
        return {}
    
    data = resp.json()
    results = data.get("results", [])
    return {row[0]: row[1] for row in results}

print(f"=== MD Home Care SEO Recovery Dry Run ===")
print(f"This period:  {fmt(start_this)} -> {fmt(end_this)} UTC")
print(f"Last period:  {fmt(start_last)} -> {fmt(end_last)} UTC")
print()

this_week = query_posthog(start_this, end_this, "this week")
last_week = query_posthog(start_last, end_last, "last week")

if not this_week and not last_week:
    print("No PostHog data returned. Check API key / project ID.")
    exit(1)

# Site totals
total_this = sum(this_week.values())
total_last = sum(last_week.values())
site_change = ((total_this - total_last) / total_last * 100) if total_last > 0 else 0

print(f"Site total this period: {total_this} views")
print(f"Site total last period: {total_last} views")
print(f"Site change: {site_change:+.1f}%")
print()

# Find drops
drops = []
for path, last_views in last_week.items():
    this_views = this_week.get(path, 0)
    if last_views < 3:
        continue
    drop_pct = ((this_views - last_views) / last_views) * 100
    abs_drop = last_views - this_views
    if drop_pct < -10 and abs_drop > 2:
        # Relative drop = page drop minus site drop
        relative_drop = drop_pct - site_change
        drops.append({
            "path": path,
            "this_views": this_views,
            "last_views": last_views,
            "drop_pct": drop_pct,
            "abs_drop": abs_drop,
            "relative_drop": relative_drop
        })

drops.sort(key=lambda x: x["abs_drop"], reverse=True)

# Apply seasonal logic
seasonal_mode = site_change < -5
if seasonal_mode:
    threshold = 20  # relative drop must be >20pp worse than site
    filtered = [d for d in drops if d["relative_drop"] < -threshold]
    print(f"⚠️  SEASONAL MODE: Site down {site_change:.1f}%. Only showing pages dropping >20pp worse than site.")
    print(f"   Raw drops: {len(drops)} -> After seasonal filter: {len(filtered)}")
    drops = filtered
else:
    print(f"✅ Normal mode (site {'up' if site_change > 0 else 'flat'} {site_change:+.1f}%)")
    
print(f"\nTotal drops found: {len(drops)}")
print()

# Map paths to content files
def path_to_content_file(path):
    """Map URL path to src/content file."""
    path = path.rstrip('/')
    if path.startswith('/blog/'):
        slug = path.replace('/blog/', '')
        return f"src/content/blog/{slug}.md"
    elif path.startswith('/services/'):
        slug = path.replace('/services/', '')
        return f"src/content/services/{slug}.md"
    elif path.startswith('/providers/'):
        slug = path.replace('/providers/', '')
        return f"src/content/providers/{slug}.md"
    return None

# Show top 30
print("=" * 90)
print(f"{'#':<4} {'Path':<55} {'Last':>6} {'Now':>6} {'Drop%':>7} {'Rel%':>7}")
print("=" * 90)

optimizable = []
for i, d in enumerate(drops[:50]):
    content_file = path_to_content_file(d["path"])
    marker = "📝" if content_file else "  "
    print(f"{i+1:<4} {d['path']:<55} {d['last_views']:>6} {d['this_views']:>6} {d['drop_pct']:>6.1f}% {d['relative_drop']:>6.1f}%  {marker}")
    if content_file:
        optimizable.append({**d, "content_file": content_file})

print()
print(f"📝 = has content file we can optimize")
print(f"Optimizable pages (top 30): {min(len(optimizable), 30)}")
print()

# Show what skill each page would use
print("=== OPTIMIZATION PLAN (DRY RUN) ===")
print()
for i, p in enumerate(optimizable[:30]):
    path = p["path"]
    if "/blog/" in path:
        skill = "Blog Creator"
    elif "/services/" in path:
        skill = "SEO + AEO"
    elif "/providers/" in path:
        skill = "SEO + AEO"
    else:
        skill = "SEO"
    print(f"  {i+1}. {path}")
    print(f"     File: {p['content_file']}")
    print(f"     Skill: {skill}")
    print(f"     Drop: {p['last_views']} -> {p['this_views']} ({p['drop_pct']:.1f}%, relative: {p['relative_drop']:.1f}%)")
    print()

# Save results
output = {
    "timestamp": now_utc.isoformat(),
    "site_change_pct": round(site_change, 1),
    "seasonal_mode": seasonal_mode,
    "total_drops": len(drops),
    "optimizable_count": min(len(optimizable), 30),
    "pages": optimizable[:30]
}

with open("scripts/seo_recovery_dryrun_results.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"Results saved to scripts/seo_recovery_dryrun_results.json")
