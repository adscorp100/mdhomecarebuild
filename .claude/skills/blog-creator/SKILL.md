# Blog Creator Skill

This skill creates SEO-optimized blog posts for MD Home Care following the GSC optimization playbook.

## When to Use

Activate this skill when the user asks to:
- Create a new blog post
- Write content for a keyword
- Generate blog content for MD Home Care

## Workflow

### Step 1: Cannibalization Check (MANDATORY)

**STOP! Before creating any new content, you MUST check if existing pages already rank for the target keyword.**

Run the cannibalization check:

```bash
cd /Users/andredeansmith/mdhomecarebuild/src/scripts
python3 advanced_gsc_analyzer.py --keyword "[USER_KEYWORD]"
```

**Interpret the results:**

1. **If pages ARE found ranking for the keyword:**
   - DO NOT create a new blog post
   - Instead, update the existing top-ranking page
   - Run a full page analysis on the existing page:
     ```bash
     python3 advanced_gsc_analyzer.py --page "/blog/[existing-slug]"
     ```
   - Inform the user: "I found existing pages ranking for this keyword. To avoid cannibalization, I recommend updating [existing page] instead of creating a new post."

2. **If NO pages are found ranking:**
   - Proceed to Step 2 to create new content
   - The script will output: "No pages found ranking for this keyword. It's safe to create a new post."

**Why this matters:** Creating multiple pages targeting the same keyword splits ranking signals and hurts SEO performance. Always consolidate content on a single authoritative page.

---

### Step 2: GSC Page Analysis (for existing pages)

If Step 1 found existing pages, analyze the top-ranking page to understand what keywords it already ranks for:

```bash
python3 advanced_gsc_analyzer.py --page "/blog/[existing-slug]"
```

Extract:
- Primary keyword (highest traffic)
- Rising star keywords (improving positions)
- Opportunity keywords (high impressions, low CTR)
- Striking distance keywords (positions 11-20)

Use this data to enhance the existing page with the new keyword while preserving its existing ranking signals.

---

### Step 3: Groq Research

Use current date context:
```bash
cd /Users/andredeansmith/mdhomecarebuild/src/scripts
CURRENT_DATE=$(date +"%B %Y")

python3 groq_research.py "What are the latest developments about '[PRIMARY_KEYWORD]' as of ${CURRENT_DATE}? Include recent changes and updates."

python3 groq_research.py "When people search for '[PRIMARY_KEYWORD]', what information are they trying to find? What problems are they solving?"

python3 groq_research.py "Search Reddit discussions about '[PRIMARY_KEYWORD]' in ${CURRENT_DATE} - what questions and concerns are people discussing?"
```

### Step 4: Blog Structure

**Frontmatter:**
```yaml
---
title: "[Primary Keyword]: Complete Guide 2025"
description: "Hook + keywords + benefit"
pubDate: [YYYY-MM-DD]
author: "Camila"
tags: []
image: "/assets/carer.webp"
---
```

**Required Sections:**
1. Key Points (bullet summary)
2. Definition/Overview (What is [topic]?)
3. Main content sections (H2: 2-6 words max)
4. Tables for comparisons/data
5. FAQ section (H3 questions)
6. Key Resources (external links)
7. CTA to MD Home Care

**Formatting Rules:**
- Use `---` dividers between major sections
- Use `>` blockquotes for important callouts
- Tables with left-aligned columns
- Internal links to related blog posts
- No emojis
- Minimum 2000 words

### Step 5: Save File

Location: `/Users/andredeansmith/mdhomecarebuild/src/content/blog/[slug].md`

Slug format: `lowercase-hyphenated-keywords.md`

## Quality Checklist

- [ ] **Cannibalization check completed** (Step 1 - MANDATORY)
- [ ] Decided: Create new OR update existing page
- [ ] GSC page analysis completed (if updating existing)
- [ ] Groq research with correct year (2025)
- [ ] Primary keyword in title
- [ ] H2s are 2-6 words
- [ ] Tables properly formatted
- [ ] Blockquotes for key info
- [ ] FAQ section included
- [ ] Internal links added
- [ ] MD Home Care CTA at end
- [ ] No emojis
