# MDHOMECARE Content Optimization Rules
# Based on GSC analysis showing 2.3% CTR success patterns

## Content Creation & SEO Guidelines

### Title Optimization Formula
When creating or editing content titles, ALWAYS:
1. **Lead with specific benefit/number** (e.g., "$40,529 Annual Funding", "$30-42/Hour")
2. **Include current year (2025)** for freshness signals
3. **Add cost/savings information** when relevant
4. **Use action-oriented language** (Get, Save, Complete Guide)
5. **Keep under 60 characters** for full SERP display

**Successful Pattern Examples:**
- "Level 3 Home Care Package: $40,529 Annual Funding Guide 2025"
- "NDIS Support Worker Rates $30-42/Hour + Latest Price Updates"
- "Best NDIS Courses 2025: Certificate III-IV Training $2,000-$5,000"

### Meta Description Template
"[Specific benefit/amount] with [service]. Complete guide to [process], [costs], and [outcome]. [Additional value proposition]."

**Examples:**
- "Get $40,529 annual funding with Level 3 Home Care Package. Complete guide to eligibility requirements, exact costs, services included, and step-by-step application process for 2025."

### Content Structure Standard
Every article MUST include:

1. **Quick Facts Box (top 100 words):**
```markdown
**Quick Facts - [Service] 2025:**
- **Cost/Funding**: [Specific amounts]
- **Eligibility**: [Age/requirements] 
- **Duration/Timeframe**: [How long]
- **Next Steps**: [Clear action items]
- **⚠️ Updates**: [Any program changes]
```

2. **Front-loaded value proposition** (after Quick Facts)
3. **Scannable content** with bullet points and numbered lists
4. **FAQ section** targeting "People Also Ask" queries
5. **Clear next steps/CTA**

### High-Converting Content Elements

**ALWAYS Include When Relevant:**
- Specific dollar amounts and rates
- Current year indicators (2025)
- Program change alerts (Support at Home transition)
- Comparison tables
- Step-by-step processes
- Eligibility checklists

**Content Topics to Prioritize:**
- Pay rates and salary information
- Funding amounts and costs
- Training costs and free options
- Eligibility requirements
- Application processes
- Program changes and updates

### Internal Linking Strategy
- Link pay rate articles to service descriptions
- Connect eligibility guides to application processes  
- Cross-reference home care and NDIS content
- Create topic clusters around:
  - Home Care Package levels (1-4)
  - NDIS service categories
  - Support worker training/jobs
  - Provider comparisons

### Featured Snippet Optimization
Structure answers for common questions:

```markdown
## [Question]?

**Quick Answer:** [Direct answer in 2-3 sentences]
- Key point 1
- Key point 2
- Key point 3

[Detailed explanation follows]
```

### Local SEO Integration
When possible, add location-specific information:
- "[Service] providers in Sydney/Melbourne/Brisbane"
- "Support worker rates [city] vs [city]"
- Regional availability and variations

## Technical Requirements

### Development Guidelines
- **Asset Imports**: Always use `/assets` path when importing assets instead of relative paths (e.g., `/assets/image.webp` instead of `../assets/image.webp`)

### Blog Post Schema Requirements
All blog posts must follow this exact frontmatter schema:

```yaml
---
title: "Specific Title with Benefits/Numbers and Year"
description: "Meta description following template with specific benefits and process"
pubDate: YYYY-MM-DD
author: "Camila"
tags: ["primary keyword", "secondary keywords", "category tags"]
image: "/assets/relevant-image.webp"
---
```

### Image Guidelines
- **Always use `/assets/` path** for image paths in frontmatter
- **Choose relevant images** from the available assets in `/public/assets/`
- **Use descriptive alt text** with target keywords when possible
- **Compress images** under 1MB for page speed
- **Available images include**: disabled carer.webp, respite care.webp, ndis-services-intellectual-disability-2-woman-smiling-hugging.webp, nurse.webp, etc.

### Schema Markup Priority
Implement schema for:
- FAQ sections (FAQ schema)
- How-to processes (HowTo schema)
- Provider reviews (Review schema)
- Cost information (Offer schema)

### Page Speed Requirements
- Target Core Web Vitals scores
- Implement table of contents for long articles
- Add "jump to section" navigation

## Writing Guidelines

### Tone & Style
- Professional but accessible
- Use specific numbers and data points
- Include disclaimers for rate/policy information
- Cite official sources (NDIS, My Aged Care, etc.)

### Keyword Integration
Focus on:
- Cost-related keywords ([service] cost, rates, fees)
- Process keywords (how to, guide, application)
- Comparison keywords (vs, difference, compare)
- Local keywords (city names + services)

### Content Freshness
- Monthly: Update all rate/cost information
- Quarterly: Refresh year indicators
- Annually: Comprehensive content audit

## Success Metrics to Monitor

### Primary KPIs
- CTR improvement (target: 1-2% increase)
- Click volume growth (target: 25-50% in 90 days)
- Featured snippet captures
- Long-tail keyword rankings

### Content Performance Indicators
- Time on page improvement
- Bounce rate reduction
- Conversion rate to contact forms
- Internal link click-through

## Content Calendar Integration

### Monthly Reviews
- Update rate information across all content
- Check for program changes (Support at Home transition)
- Analyze GSC data for new opportunities

### Quarterly Optimization
- Title tag A/B testing for top articles
- Meta description refresh
- Internal linking audit and improvement

### Annual Strategy
- Comprehensive content audit
- ROI analysis of optimization efforts
- Strategic planning for next year's focus

## Quality Control Checklist

Before publishing any content, verify:
- [ ] Title includes specific benefit/number
- [ ] Meta description follows template
- [ ] Quick Facts box present and accurate
- [ ] Current rates/costs verified from official sources
- [ ] FAQ section included
- [ ] Internal links to related content added
- [ ] Images optimized and using /assets path
- [ ] Schema markup implemented where relevant

## Competitive Differentiation

**What Makes Our Content Win:**
- More specific cost/rate information
- Current year indicators (2025)
- Program change updates
- Clear, actionable next steps
- Comprehensive eligibility guides
- Local provider information

**Avoid These Common Mistakes:**
- Generic titles without specific benefits
- Vague meta descriptions
- Burying key information below fold
- Outdated rate information
- Missing program change alerts
- Poor internal linking structure

This framework ensures all content follows proven patterns for maximum search visibility and user engagement, based on successful articles achieving 2.3% CTR performance. 