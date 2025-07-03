# Blog Post Creation Playbook

## Overview
You are the world's best SEO professional, tasked with creating high-ranking, high-converting blog posts from scratch. This playbook guides you through a systematic process, starting from a list of keywords and ending with a published, optimized blog post.

This playbook uses a combination of Google Search Console (GSC) analysis to prevent keyword cannibalization and AI-powered research with Groq to ensure content is comprehensive, accurate, and tailored to user intent.

### Standard Blog Post vs. Pillar Page
This playbook can be used for two types of content.

-   **Standard Blog Post:** A focused article on a specific topic. Use the standard structure for this.
-   **Pillar Page:** A comprehensive, in-depth guide covering a major topic from all angles. For high-volume, high-competition keywords (like the ones this guide was tested on), **you must create a Pillar Page to rank effectively.**

## Step 1: Foundational Research & Keyword Analysis

The starting point for any new blog post is a list of target keywords. Your goal in this step is to validate the opportunity, check for existing content, and build a deep understanding of the topic.

### Environment Setup: Using the Virtual Environment (VENV)
**CRITICAL**: All Python scripts **MUST** be run using the project's virtual environment to avoid dependency errors. This ensures you are using the correct versions of all required packages.

- **DO NOT** use `python3 ...`
- **INSTEAD, USE** `venv/bin/python3 ...`

All commands in this playbook assume you are running them from the **root directory** of the project.

### Input: Target Keywords
You will be provided with a primary keyword and a list of secondary keywords.

**Example:**
- **Primary Keyword:** "aged care for pensioners with no assets"
- **Secondary Keywords:** "government funded aged care facilities", "who pays for nursing home care in australia", "financial hardship aged care"

### Phase 1A: GSC Cannibalization Check & Next Steps
**CRITICAL**: Before creating new content, you must check if other pages on `mdhomecare.com.au` already rank for your target keywords. Creating a new post for a keyword you already rank for can harm your SEO through "keyword cannibalization."

1.  **Check Primary Keyword in GSC:** Use the `advanced_gsc_analyzer.py` script with the `--keyword` flag to search for your primary keyword directly in Google Search Console. This will show you which pages (if any) are already getting impressions for it.

    ```bash
    # Example: Check who ranks for "aged care for pensioners with no assets"
    venv/bin/python3 src/scripts/advanced_gsc_analyzer.py --keyword "aged care for pensioners with no assets"
    ```

2.  **Analyze the Output & Determine Action:**
    -   **If no pages are found:** Excellent. This confirms there is no keyword cannibalization. You can proceed with creating a new blog post from scratch. **Continue to Phase 1B of this playbook.**
    -   **If pages are found:** The script will list the ranking pages, sorted by impressions. This means you already have content targeting this keyword. Creating a new article is the wrong strategy. Instead, you must optimize the existing page.
        -   **Identify the Target URL:** The page with the most impressions is your "true" ranking page for this keyword.
        -   **Switch Playbooks:** Instead of creating a new post, your task is now to optimize an existing one. You must **stop using this playbook** and switch to the **AUTOMATED BLOG OPTIMIZATION WITH GSC.md** playbook.

3.  **Executing the Correct Strategy:**
    -   **For a New Post:** Proceed to **Phase 1B: Deep Topic Research with Groq AI**.
    -   **For an Existing Post:**
        1.  Take the URL of the ranking page identified in the previous step.
        2.  Open the **AUTOMATED BLOG OPTIMIZATION WITH GSC.md** playbook.
        3.  Start at Step 1 of that playbook, using the identified URL as your target for GSC analysis. This will give you a full picture of *all* the keywords the existing page ranks for, allowing for a much more effective optimization.

### Phase 1B: Deep Topic Research with Groq AI (Pillar Page Method)
**CRITICAL**: For a pillar page, a single research query is not enough. You must perform multiple, targeted queries to gather comprehensive information.

**Step 1: Prepare for Research**
```bash
cd src/scripts
CURRENT_DATE=$(date +"%B %Y")
PRIMARY_KEYWORD="[Your Primary Keyword]"
```
**Note**: The following research commands are run from the `src/scripts` directory, so the path to the python executable is `../../venv/bin/python3`.

**Step 2: Multi-Query Core Topic Research**
```bash
# Query 1: The "How-To" Process. Get the official steps.
../../venv/bin/python3 groq_research.py "Provide a detailed, step-by-step guide on '${PRIMARY_KEYWORD}' as of ${CURRENT_DATE}. For all facts, figures, and processes, you MUST provide URLs to the specific pages on My Aged Care, Services Australia, or other official .gov.au resources."

# Query 2: The "Deeper Details". Ask for specifics on complex parts of the process.
../../venv/bin/python3 groq_research.py "Provide a deep dive into the financial and legal aspects related to '${PRIMARY_KEYWORD}'. Explain concepts like the 'means test', 'financial hardship provisions', and define official terms like 'fully supported resident'. Include official government source URLs."

# Query 3: The "Human Element". Find the real-world questions and fears.
../../venv/bin/python3 groq_research.py "Search Reddit and Australian forums for discussions about '${PRIMARY_KEYWORD}'. What are the common questions, fears, and real-world experiences people share regarding this topic? What are they most worried about?"
```

**Step 3: Targeted Research to Address Community Questions**

After understanding the real-world questions from your community research, you may uncover specific concerns that your initial research didn't fully address. This final research step ensures you close those gaps with authoritative information.

```bash
# Query 4: Address the Gaps. Get official answers to community questions.
# Analyze the output from Query 3. Identify the top 1-2 questions or fears that need a definitive, official answer.
# Example: If people are worried about how selling their home affects their pension.
../../venv/bin/python3 groq_research.py "Explain in simple terms how [Specific Question from Community Research] works, according to official Australian government sources like Services Australia or the My Aged Care website. Provide direct URLs to the relevant pages."
```

## Step 2: Content Scaffolding & Structure

With your deep research complete, it's time to structure your Pillar Page.

### 1. Create the File
- **Slug:** Create a short, descriptive, keyword-rich slug (e.g., `aged-care-for-pensioners-with-no-assets`).
- **Filename:** Create a new markdown file in `src/content/blog/` using the slug.

### 2. Define the Frontmatter
```yaml
---
title: "[Compelling Title with Primary Keyword and Year]"
description: "[Hook + top 3 keywords + clear benefit (what user will learn/get)]"
pubDate: YYYY-MM-DD # Use today's date
author: "MD Home Care"
tags: ["Keyword 1", "Keyword 2", "Keyword 3"]
image: "/assets/[image-name].webp" # Choose a relevant image from the public/assets/ directory.
---
```

### 3. Structure the Pillar Page Content
**CRITICAL**: A Pillar Page requires more depth than a standard post. Use this proven structure.

```markdown
<!-- INTRODUCTION -->
A short introduction (2-3 paragraphs). Acknowledge the user's core problem and fear directly. Promise a comprehensive, clear solution.

<!-- ADDRESS THE CORE QUESTION (H2) -->
## [Rephrase the Primary Keyword as a Question]

Immediately answer the user's main question directly and empathetically. E.g., "Yes, you can absolutely get aged care with no money."

<!-- STEP-BY-STEP GUIDE (H2) -->
## Step-by-Step Guide: [The Process]

Break down the entire process into numbered steps with H3s for each major stage (e.g., "Step 1: The My Aged Care Assessment", "Step 2: The Centrelink Means Test"). This adds immense value and targets long-tail keywords.

<!-- DEMYSTIFYING THE DETAILS (H2) -->
## Demystifying the Costs: [Explain the Financials]

This is where you build trust and authority. Use a markdown table to break down the cost components clearly (e.g., Basic Daily Fee, Means-Tested Fee, Accommodation Costs). Explain who pays for what, based on your research.

<!-- FAQ SECTION (H2) -->
## Frequently Asked Questions

Use H3s for each question. Address the specific fears and real-world questions you discovered in your community research. Go beyond basic questions and tackle the tough ones ("Will my pension be affected?", "What are my rights?").

<!-- CONCLUSION & CTA (NO HEADER) -->
A concluding paragraph that summarizes the key takeaway and reinforces the message of hope and support. End with a strong, clear call to action (CTA).

At MD Home Care, we believe in [value proposition]. We can help you [solve the problem].

If you have questions about [topic] or need help, **[contact MD Home Care today](/contact)**.
```

## Step 3: Content Creation & Optimization

Now, write the content using your research and the structure above.

-   **Synthesize Research:** Combine the "official process" with the "human element." Use the step-by-step details and address the fears you found.
-   **Add Authoritative Links:** **CRITICAL**: Link out to the official `.gov.au` source URLs you gathered during research. This is a powerful trust signal for both users and search engines. Use descriptive anchor text, e.g., `[My Aged Care website](https://www.myagedcare.gov.au)`.
-   **Use Keywords Naturally:** Place your primary and secondary keywords in headings and body content where they make sense. Don't force them.
-   **Internal Linking:** Link to other relevant pages on `mdhomecare.com.au` where it adds value.
-   **No Emojis:** Maintain a professional tone.

## Step 4: Final Quality Check

### Pillar Page Checklist:
- [ ] **Depth & Comprehensiveness:** Does the post fully cover the topic? Is it the best resource on the internet for this query?
- [ ] **Authoritative Links:** Are there at least 2-3 links to official `.gov.au` sources?
- [ ] **Structure:** Does it follow the Pillar Page structure with a step-by-step guide and detailed cost breakdown?
- [ ] **Title (H1):** The frontmatter `title` is compelling and contains the primary keyword.
- [ ] **Keywords:** Primary and secondary keywords are integrated naturally.
- [ ] **CTA:** There is a clear call to action at the end linking to the `/contact` page.
- [ ] **Image:** A relevant image from `public/assets/` has been selected.
- [ ] **Accuracy:** All information has been cross-verified with your research from official sources. 