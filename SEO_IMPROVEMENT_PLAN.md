# SEO Improvement Plan for MD Home Care Services Pages

## Current State Analysis

Based on GSC data and site structure:

### What You Have Working Well:
1. **Strong URL structure**: `/services/[slug]` (canonical) → `/services/[slug]/[suburb]` (location variants)
2. **Good schema markup**: Service schema, FAQ schema, breadcrumbs
3. **QuickFacts component**: All 60 services have cost/funding data
4. **Region-specific content**: `region-content.json` with local insights, hospitals, transport
5. **Suburb details**: `suburb-details.json` with population, councils, postcodes
6. **Internal linking**: Nearby suburbs, related services, related blog posts

### Key Problems Identified from GSC Data:

| Issue | Evidence |
|-------|----------|
| **Services pages have LOW impressions** | Top services keywords get only ~100-500 impressions vs blog posts getting 10,000-70,000 |
| **Thin content dilution** | 60 services × ~310 suburbs = **18,600 pages** with similar content |
| **Weak topical authority on core services** | "mobile podiatrist" type keywords rank well, but broader "aged care cleaning" dropping |
| **Striking distance opportunities missed** | "podiatrist bunbury" (pos 11.2), "sda providers" (pos 14.9), "wheelchair hire near me" (pos 16.2) |
| **High-impression services pages have terrible CTR** | `/services/sil-services/perth/` - 9,750 impressions, 1 click (0.01% CTR) |

---

## Implementation Checklist

### Phase 1: Strengthen Canonical Service Pages
- [x] 1.1 Add comprehensive content to service markdown files (1,500-2,500 words minimum) - FAQs added
- [x] 1.2 Add service-specific visible FAQ sections to service content - COMPLETED
- [x] 1.3 Create service category hub pages (`/services/category/[category]`) - COMPLETED

### Phase 2: Differentiate Suburb Pages
- [x] 2.1 Expand `suburb-details.json` with richer local data - COMPLETED (60+ suburbs with detailed info)
- [x] 2.2 Modify suburb page template to show more local data - COMPLETED
- [x] 2.3 Add dynamic local content sections - COMPLETED
- [x] 2.4 Add suburb-specific testimonials/reviews system - COMPLETED (SuburbTestimonials component)

### Phase 3: Technical SEO Improvements
- [x] 3.1 Keep self-canonical strategy (already correct)
- [x] 3.2 Improve internal linking structure - Category hub pages link services
- [x] 3.3 Update title tags with price signals - COMPLETED
- [x] 3.4 Update meta descriptions with benefits/CTAs - COMPLETED

### Phase 4: CTR Optimization
- [x] 4.1 Add AggregateRating schema to pages - COMPLETED
- [x] 4.2 Add HowTo schema for process-oriented services - COMPLETED
- [x] 4.3 Improve QuickFacts for featured snippet extraction - COMPLETED (semantic table structure)

### Phase 5: Content Strategy for Authority
- [x] 5.1 Create location landing pages (`/locations/[suburb]`) - COMPLETED
- [ ] 5.2 Create service comparison content - Future enhancement
- [ ] 5.3 Create "ultimate guide" blog posts linking to services - Future enhancement

---

## Priority Order for Implementation

| Priority | Task | Impact | Effort | Status |
|----------|------|--------|--------|--------|
| **1** | Expand suburb-details.json with richer local data | High | Medium | ✅ DONE |
| **2** | Add visible FAQ sections to service markdown files | High | Low | ✅ DONE |
| **3** | Update title/meta description templates with price signals | High | Low | ✅ DONE |
| **4** | Add AggregateRating schema to pages | High | Low | ✅ DONE |
| **5** | Create service category hub pages | Medium | Medium | ✅ DONE |
| **6** | Add suburb testimonials data file | Medium | Medium | ✅ DONE |
| **7** | Create location landing pages `/locations/[suburb]` | Medium | Medium | ✅ DONE |
| **8** | Expand service markdown content to 1,500+ words | Medium | High | Partial |
| **9** | Add HowTo schema for applicable services | Low | Low | ✅ DONE |
| **10** | Create "ultimate guide" blog posts for top services | Medium | High | Future |

---

## Measuring Success

Track these KPIs in GSC:

1. **Services page impressions** (target: 2x increase in 90 days)
2. **Average CTR on services pages** (target: >2% for suburb pages)
3. **Striking distance keywords moving to page 1** (positions 11-20 → 1-10)
4. **Core service canonical page rankings** (should improve as authority flows up)

---

## Detailed Implementation Notes

### Title Tag Pattern
Current: `{service} in {suburb} | MD Home Care`
New: `{service} in {suburb} | From ${price} | NDIS & HCP Approved`

### Meta Description Pattern
Include: Service benefit, Location, Call to action, Trust signal (reviews/qualifications)

### Suburb Details Data Structure
```json
{
  "suburb-slug": {
    "displayName": "Suburb Name",
    "population": "XX,XXX",
    "elderlyPercent": "XX%",
    "ndisParticipants": "~XXX estimated",
    "localCouncil": "Council Name",
    "nearestHospital": "Hospital Name",
    "postcode": "XXXX",
    "medicalCentres": ["Centre 1", "Centre 2"],
    "pharmacies": ["Pharmacy 1", "Pharmacy 2"],
    "landmarks": ["Landmark 1", "Landmark 2"],
    "demographicNotes": "Description of who lives here",
    "accessibilityNotes": "Terrain and accessibility info",
    "publicTransport": ["Bus route 1", "Train line"],
    "localProviders": ["Other local services"],
    "communityGroups": ["Local groups for social connection"]
  }
}
```

### FAQ Section Template for Service Markdown
```markdown
## Frequently Asked Questions

### What does {service} cost under NDIS?
[Detailed answer with specific line items]

### Can I choose my own support worker?
[Answer that builds trust]

### How quickly can services start?
[Timeline answer]

### What qualifications do your staff have?
[Trust-building answer]
```
