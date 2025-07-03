# Automated Service Page GSC Optimization Playbook

## Overview
You are a world-class SEO and Conversion Rate Optimization (CRO) professional. Your task is to optimize service pages not just for traffic, but to maximize leads and client acquisition. Service pages have a direct commercial intent and must connect with users who are actively seeking care solutions, often under stressful circumstances.

**Enhanced with AI-Powered Research & Geo-Data** - This playbook integrates the Groq research tool `groq_research.py` and GSC tool `advanced_gsc_analyzer.py` with geo-location data for comprehensive market analysis and content optimization. **CRITICAL**: The goal is a dual-focus: use GSC for SEO insights and then apply deep user psychology for conversion.

## Service Page Strategy Framework

### Service-Specific Keyword Analysis
Service pages target high-intent commercial and transactional keywords:
1.  **Transactional Keywords**: "[service name] [suburb/city]", "aged care services near me"
2.  **Problem-Aware Keywords**: "help for elderly at home", "ndis disability support"
3.  **Solution-Seeking Keywords**: "in-home nursing care", "respite care options"

### Service Page Opportunity Identification
Prioritize based on **lead generation potential + service profitability**:
-   **High-volume transactional keywords** in key service areas.
-   **Keywords indicating urgent need** where MD Home Care offers an immediate solution.
-   **Competitor-branded keywords** where users are seeking alternatives.

### Advanced Service Page Analysis
Layer these considerations for service page optimization:
1.  **Local SEO Authority**: Strong signals for specific suburbs and regions.
2.  **Service-Level Expertise**: Demonstrating deep knowledge of the specific service.
3.  **Trust & Credibility**: Showcasing qualifications, experience, and client testimonials.

## Step 1: Consolidated GSC Performance Analysis & Geo-Keyword Sanitization

### Phase 1A: GSC Data Collection with Wildcard Filtering
**CRITICAL**: Start with a consolidated GSC analysis to understand performance across all geographic variations of a service page.

### Service URL Pattern Analysis
Service pages follow a unique structure:
-   Australia-wide (default): `mdhomecare.com.au/services/[service-slug]`
-   Suburb-specific: `mdhomecare.com.au/services/[service-slug]/[suburb]`

To analyze a service's total performance, we must aggregate data from all its suburb-specific pages.

**GSC Data Collection Command:**
Use a URL filter to capture data for a service across all suburbs. This command assumes your `advanced_gsc_analyzer.py` script can filter pages by a "contains" operator.

```bash
# Consolidate GSC data for a specific service (e.g., 'respite-care')
python3 src/scripts/advanced_gsc_analyzer.py --page "/services/respite-care/"
```
*This command will fetch all queries for URLs containing `/services/respite-care/`, effectively combining data from the main service page and all its suburb-specific variants.*

### Phase 1B: Geo-Keyword Sanitization
**CRITICAL**: After consolidating GSC data, "sanitize" the queries by stripping out geographic identifiers (suburbs, cities) to reveal the core, non-geo-specific user intent.

**Keyword Sanitization Process:**
This process requires a script to programmatically remove suburb names from the GSC query data using the `data/australian-suburbs.json` file.

**Conceptual Sanitization Script (`sanitize_gsc_queries.py`):**
```python
import json
import pandas as pd

# Load GSC query data (e.g., from a CSV export)
gsc_df = pd.read_csv('gsc_export.csv')

# Load the list of Australian suburbs
with open('data/australian-suburbs.json', 'r') as f:
    suburbs_data = json.load(f)
    suburbs = [suburb['suburb'].lower() for suburb in suburbs_data]

def sanitize_query(query):
    """Removes suburb names from a search query."""
    words = query.lower().split()
    # Remove words that are suburbs
    sanitized_words = [word for word in words if word not in suburbs]
    return ' '.join(sanitized_words)

# Apply the sanitization function to the query column
gsc_df['sanitized_query'] = gsc_df['query'].apply(sanitize_query)

# Aggregate metrics for sanitized queries
aggregated_df = gsc_df.groupby('sanitized_query').agg({
    'clicks': 'sum',
    'impressions': 'sum',
    # Add other metrics to aggregate
}).reset_index().sort_values(by='impressions', ascending=False)

print(aggregated_df.head(20))
# Save the aggregated data to a new file
aggregated_df.to_csv('sanitized_aggregated_queries.csv', index=False)
```
After this step, you will have a list of core, high-intent keywords based on aggregated data.

### Phase 1C: Core Keyword Performance Validation (NEW)
**CRITICAL**: The sanitized data gives you a good *idea* of your core keywords. Now, validate their actual performance with a second, more precise GSC query. This confirms which non-geo terms are truly driving your visibility.

**GSC Core Keyword Validation Command:**
Take the top 1-3 sanitized keywords and run a **keyword-based** query.

```bash
# Validate the performance of your top sanitized keyword (e.g., 'disability home care')
python3 src/scripts/advanced_gsc_analyzer.py --keyword "disability home care"

# Validate another top keyword (e.g., 'disability support services')
python3 src/scripts/advanced_gsc_analyzer.py --keyword "disability support services"
```
*This provides a clean, definitive dataset on the performance of your most important commercial terms, free from the noise of long-tail local queries. Use THIS data as your primary source of truth for optimization.*

**Document Finalized Keyword Insights:**
Use the insights from this second, more accurate query to finalize your targets.
```bash
# Note the top validated keywords for research targeting
echo "Top Validated GSC Keywords for [Service]:" > gsc_research_targets.txt
echo "- Primary Keyword: [top keyword from validation query]" >> gsc_research_targets.txt
echo "- Rising Star Keywords: [list from validation query]" >> gsc_research_targets.txt
echo "- Opportunity Keywords: [list from validation query]" >> gsc_research_targets.txt
```

### Phase 1D: GSC Keyword-Specific Research with Groq AI
**CRITICAL**: Use Groq for targeted research based on the **validated GSC keywords**. This research must focus on the core user intent.

**Step 1: Primary Keyword Deep Research**
```bash
# Use EXACT validated primary keyword from your analysis
PRIMARY_KEYWORD="[insert exact validated keyword here]" # e.g., "ndis respite care"
CURRENT_DATE=$(date +"%B %Y")

# Research the core user need for this service
python3 groq_research.py "When people search for '${PRIMARY_KEYWORD}', what are their biggest challenges and goals? What problems are they trying to solve for themselves or a loved one?"

# Research the decision-making criteria
python3 groq_research.py "What are the most important factors people consider when choosing a provider for '${PRIMARY_KEYWORD}'? Focus on trust, quality, reliability, and cost."
```

**Step 2: Community & Competitor Research**
```bash
# Research community discussions for your primary keyword
python3 groq_research.py "Search Reddit and forum discussions about '${PRIMARY_KEYWORD}' in Australia. What are the common questions, frustrations, and positive experiences people share?"

# Research what competitors are missing
python3 groq_research.py "What questions about '${PRIMARY_KEYWORD}' are people asking that competitor websites fail to answer properly? What information gaps can MD Home Care fill?"
```

## Step 2: Conversion-Focused Content Strategy

This section is completely redesigned to focus on maximizing conversions. SEO gets the user to the page; conversion-focused content gets them to contact you.

### 1. The Core Principle: Empathy Drives Action
Users seeking care are often stressed, overwhelmed, and looking for a trustworthy guide. Your content must show deep empathy for their situation. The goal is to make them feel understood, supported, and confident that you are the right choice.

### 2. Content Structure: The Problem, Agitate, Solve (PAS) Framework
Structure your page to mirror the user's emotional journey.

1.  **Problem (The Headline & Opening Hook)**: Immediately acknowledge their primary problem with an empathetic, benefit-driven headline.
    *   **Old H1**: "Disability Home Care {suburb}"
    *   **New H1**: "Finally, Reliable Disability Home Care in {suburb} That You Can Trust"
    *   **Opening Sentence**: "Finding the right support for yourself or a loved one can be overwhelming. You need a partner who provides compassionate, expert care so you can live independently and with peace of mind."

2.  **Agitate (Address the Pains)**: Gently touch upon the specific frustrations and fears you discovered in your research. This shows you truly understand their situation.
    *   Create a section like: "**The Right Support Makes All the Difference**"
    *   Use bullet points:
        *   Tired of unreliable support workers?
        *   Worried about the quality and consistency of care?
        *   Confused by your NDIS plan?
        *   We're here to solve that.

3.  **Solve (Introduce Your Services as the Solution)**: This is where you introduce your services, framed as direct solutions to their problems.
    *   **Section Title**: `Our Disability Home Care Services: Your Path to Independence`
    *   For each service, lead with the benefit:
        *   **Personal Care Support**: "Maintain your dignity and routine with respectful, professional assistance."
        *   **Household Tasks**: "Free up your time and energy with our practical help around the home."

### 3. Building Unbreakable Trust
Trust is the single most important factor in conversion. Weave these elements throughout the page.

*   **The MD Home Care Difference Section**: A dedicated H2 section that clearly articulates your value proposition.
    *   **Headline**: `Why Families in {suburb} Choose MD Home Care`
    *   **Sub-headings (H3s)**:
        *   `A Team You Can Trust`: Talk about your rigorous vetting, training, and background checks.
        *   `Care That's All About You`: Detail your person-centered approach.
        *   `Local Experts, Community Focused`: Emphasize your local knowledge.
        *   `NDIS Made Simple`: Explain how you help clients navigate their plans.

*   **Humanize Your Team**:
    *   Include high-quality photos and short, friendly bios of your care managers or local team leaders. "Meet Sarah, Your Local Care Advisor in {suburb}." This puts a face to the name and builds an immediate connection.

*   **Powerful Testimonials (Client Stories)**:
    *   Go beyond a simple quote. Frame it as a mini-story.
    *   **Format**: Use a shaded box with a large quote icon.
    *   **Headline**: `John's Story: Finding Independence with MD Home Care`
    *   **Quote**: "Before MD Home Care, we were struggling to find consistent support. Now, my son has a support worker he trusts, and his confidence has soared. I can finally relax knowing he's in safe hands." - *Mary L., {suburb}*

### 4. Simplify the Process: "How It Works"
Reduce user anxiety by making the next steps crystal clear.

*   **Use a simple, 3 or 4-step visual graphic.**
*   **Step 1: Free Consultation.** (Low-risk first step). "A friendly chat with a care advisor to understand your needs. No obligations, just helpful advice."
*   **Step 2: Customised Care Plan.** "We design a personalized support plan that matches your goals and NDIS budget."
*   **Step 3: Meet Your Support Worker.** "We introduce you to a carefully matched support worker who fits your personality and needs."
*   **Step 4: Start Your Service.** "Begin your journey to greater independence with a team that truly cares."

### 5. Conversion-Optimized Calls-to-Action (CTAs)
Your CTAs must be compelling, clear, and low-pressure.

*   **Primary CTA Button (Top of Page & Conclusion)**:
    *   **Text**: "Get Your Free Care Consultation" or "Speak With a Care Advisor"
    *   **Sub-text (optional)**: "No obligation, just friendly advice."

*   **Mid-Page CTAs**: Place them after key sections (like "Why Choose Us" or "How It Works").
    *   Use contextual links: "Ready to build your care plan? `Speak to an advisor today`."

*   **Final CTA Section**: A strong, reassuring closing statement.
    *   **Headline**: "You Don't Have to Figure This Out Alone."
    *   **Body**: "Let our expert team in {suburb} build a care plan that brings you peace of mind and independence. Contact us today to get started."
    *   Follow with the main CTA button.

## Step 3: Page Content and SEO Implementation

### 1. Frontmatter and Title
-   **Title**: Use a benefit-driven, keyword-focused title like `[Benefit] [Service] in {suburb]` (e.g., "Trusted Disability Home Care in {suburb}"). Avoid adding the brand name to keep it concise.
-   **Description**: Empathetic hook + top 2-3 validated keywords + benefit. (e.g., "Feeling overwhelmed finding disability care in {suburb}? MD Home Care offers trusted, expert NDIS support to help you live independently. Get your free consultation.")

### 2. Heading (H1-H4) Structure
-   **H1**: The main "Problem" headline.
-   **H2s**: Major page sections (`Why Choose Us`, `How It Works`, `Our Services`, `FAQs`).
-   **H3s**: Sub-points within a section (e.g., the individual points under `Why Choose Us`).
-   **H4s**: Deeper details if needed, but use sparingly to maintain clarity.

### 3. FAQ Section Optimization
-   Answer questions that address user fears and uncertainties discovered in your research.
-   **New Questions to Add**:
    *   `What happens if I'm not happy with my support worker?` (Addresses the fear of being stuck with a bad match).
    *   `How do you ensure the safety and security of your clients?` (Directly tackles a primary concern).
    *   `Is your pricing transparent? Are there any hidden fees?` (Builds trust around cost).

### 4. Internal Linking Strategy
- Link to pages that build trust and provide more information.
- **Primary Links**: `/contact`, `/about-us`.
- **Secondary Links**: Relevant, detailed blog posts (e.g., "A Guide to Understanding Your NDIS Plan").

## Step 4: Content Creation & Quality Validation

### Content Development Based on Research
Apply your **sanitized GSC data** and **Groq research insights** to write content that directly addresses the core user needs, separate from their location. The content should be helpful first, and promotional second.

### Markdown Quality Control
**CRITICAL**: Ensure clean, professional markdown.
-   **Remove all stray CSS/HTML**.
-   **Fix any broken markdown formatting**.
-   **Validate all internal links**.
-   **Ensure a clean, readable structure** with proper heading hierarchy (H1 -> H2 -> H3).

### Content Quality Validation
**MANDATORY: Use your sanitized GSC keywords to validate content accuracy and relevance.**

```bash
cd src/scripts
CURRENT_DATE=$(date +"%B %Y")
PRIMARY_KEYWORD="[your exact sanitized primary GSC keyword]"

# Validate that your content directly answers the core need
python3 groq_research.py "My page for '${PRIMARY_KEYWORD}' covers [list key points]. Based on user intent, what critical information am I missing that would stop someone from contacting us?"

# Cross-check with community pain points
python3 groq_research.py "Based on recent Reddit discussions about '${PRIMARY_KEYWORD}' in Australia, does my content address the main frustrations or concerns people have when seeking this service?"

# Final gap analysis
python3 groq_research.py "What unique or important information about '${PRIMARY_KEYWORD}' are my top competitors missing? What can I include to be the most helpful resource?"
```

## Step 5: Service-Specific SERP Optimization

### Local Pack & Map Optimization
While the on-page content is critical, for service pages, you must also consider off-page local SEO.
-   **Google Business Profile**: Ensure your Google Business Profile is fully optimized for each service area, with correct service listings, hours, and contact information.
-   **Local Citations**: Build consistent Name, Address, Phone Number (NAP) citations across relevant Australian directories.
-   **Reviews**: Actively encourage satisfied clients to leave reviews mentioning the service and location.

### Featured Snippet Targeting
Service pages can win snippets for:
-   **"What is..." questions** (answered in your definition section).
-   **"How to..." questions** (answered in your process section).
-   **Bulleted lists** (your benefits section).

## Final Quality Checklist
-   [ ] **GSC data consolidated** using a page filter.
-   [ ] **Keywords sanitized** by stripping out suburb names.
-   [ ] **Content is built around core, sanitized keywords**.
-   [ ] **Title and H1 are geo-targeted**.
-   [ ] **Content directly answers the user's primary problem**.
-   [ ] **Clear, compelling CTAs** are present.
-   [ ] **FAQ section addresses real user questions**.
-   [ ] **No markdown or formatting errors**.
-   [ ] **Internal linking is strategic and helpful**.

This service page optimization playbook provides a systematic, data-driven approach to increasing visibility and generating leads. By validating GSC data, focusing on user empathy and trust, and building a clear path to conversion, you can create service pages that rank well and convert effectively across all target locations. 