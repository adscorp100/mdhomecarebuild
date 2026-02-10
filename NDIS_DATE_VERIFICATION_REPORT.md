# NDIS Pricing Dates Verification Report
**Date of Analysis:** February 11, 2026
**Analyst:** Subagent deep-verify-pricing
**Source Files Analyzed:** 5 blog posts

## CRITICAL ERRORS FOUND: 11 DATE DISCREPANCIES

---

## FILE 1: ndis-support-worker-pay-rates.md

### ERROR BLOCK 1: National Public Holidays 2026 Section (Lines 282-289)
**Issue:** ALL dates in the 2026 section incorrectly show year as 2025 instead of 2026

| Line | Current Text | Error | Correct Text | Source |
|------|-------------|-------|--------------|---------|
| 282 | `\| New Year's Day \| 1 January 2025 \| Thursday \|` | Year should be 2026 | `\| New Year's Day \| 1 January 2026 \| Thursday \|` | Fair Work Ombudsman 2026 |
| 283 | `\| Australia Day \| 26 January 2025 \| Monday \|` | Year should be 2026 | `\| Australia Day \| 26 January 2026 \| Monday \|` | Fair Work Ombudsman 2026 |
| 284 | `\| Good Friday \| 3 April 2025 \| Friday \|` | Year should be 2026 | `\| Good Friday \| 3 April 2026 \| Friday \|` | Fair Work Ombudsman 2026 |
| 285 | `\| Easter Saturday \| 4 April 2025 \| Saturday \|` | Year should be 2026 | `\| Easter Saturday \| 4 April 2026 \| Saturday \|` | Fair Work Ombudsman 2026 |
| 286 | `\| Easter Monday \| 6 April 2025 \| Monday \|` | Year should be 2026 | `\| Easter Monday \| 6 April 2026 \| Monday \|` | Fair Work Ombudsman 2026 |
| 287 | `\| Anzac Day \| 27 April 2025 \| Monday (observed) \|` | Year should be 2026 | `\| Anzac Day \| 27 April 2026 \| Monday (observed) \|` | ACT Gov 2026 Calendar |
| 288 | `\| Christmas Day \| 25 December 2025 \| Friday \|` | Year should be 2026 | `\| Christmas Day \| 25 December 2026 \| Friday \|` | Standard calendar |
| 289 | `\| Boxing Day \| 28 December 2025 \| Monday (observed) \|` | Year should be 2026 | `\| Boxing Day \| 28 December 2026 \| Monday (observed) \|` | Standard calendar |

**Verification Sources:**
- https://www.fairwork.gov.au/employment-conditions/public-holidays/2026-public-holidays
- https://publicholidays.com.au/easter/ (confirms Easter 2026: Good Friday April 3, Easter Sunday April 5)
- https://www.act.gov.au/__data/assets/pdf_file/0004/2155495/ACT-Public-Holidays-2026.pdf (Anzac Day Monday 27 April 2026 observed)

### NOTE: Anzac Day 2026 Date Logic Issue
**Line 287 context:** The actual Anzac Day 2026 is **Saturday, April 25, 2026**. The observed public holiday is **Monday, April 27, 2026** (in most jurisdictions).

**Table should clarify:**
- Option 1: `| Anzac Day | 25 April 2026 | Saturday |` (actual day)
- Option 2: Keep as is but fix year: `| Anzac Day | 27 April 2026 | Monday (observed) |`

Current practice in the document shows observed holidays, so Option 2 is consistent.

### ERROR BLOCK 2: Queen's Birthday Section (Lines 293-297)
**Issue:** Column headers are confusing and dates show 2025 instead of 2026

| Line | Current Text | Error | Issue |
|------|-------------|-------|-------|
| 293 | `\| State \| 2026 Date \| 2026 Date \|` | Duplicate column header | Should be `\| State \| 2025 Date \| 2026 Date \|` |
| 295 | `\| ACT, NSW, NT, SA, TAS, VIC \| 9 June 2025 \| 8 June 2025 \|` | Second column should be 2026 | `\| ACT, NSW, NT, SA, TAS, VIC \| 9 June 2025 \| 8 June 2026 \|` |
| 296 | `\| Queensland \| 6 October 2025 \| 5 October 2025 \|` | Second column should be 2026 | `\| Queensland \| 6 October 2025 \| 5 October 2026 \|` |
| 297 | `\| Western Australia \| 23 September 2025 \| 28 September 2025 \|` | Second column should be 2026 | `\| Western Australia \| 23 September 2025 \| 28 September 2026 \|` |

---

## FILE 2: ndis-invoice-template-guide.md

### ERROR: Claim Window Effective Date (Lines 17 & 474)
**Issue:** Effective date stated as 2026 but should be 2025

| Line | Current Text | Correct Text | Source |
|------|-------------|--------------|---------|
| 17 | `Claim window extended to 2 years from service date (effective October 3, 2026)` | `Claim window extended to 2 years from service date (effective October 3, 2025)` | Multiple NDIS provider sources |
| 474 | `As of October 3, 2026, you have **2 years** from the service delivery date to submit claims.` | `As of October 3, 2025, you have **2 years** from the service delivery date to submit claims.` | Multiple NDIS provider sources |

**Verification Sources:**
- https://prcsa.com.au/ndis-claims-must-be-submitted-within-two-years-new-rule-explained/ (states "3 October 2024: commenced with grace period, 2 October 2025: grace period ended")
- https://helpathandsupport.com.au/ndis-claims-time-limits/ (states "from 3 October 2025")
- https://www.leapin.com.au/ndis/ndis-changes/ (states "From 3 October 2025")

**Critical Note:** The document is dated "Last updated: December 17, 2025" (line 23), which is **after** October 3, 2025, yet incorrectly states the effective date as October 3, 2026 (future tense). This is logically inconsistent.

---

## FILE 3: ndis-price-guide.md

### UNVERIFIED DATE: Funding Periods Effective Date (Line 135)
**Issue:** Cannot verify this specific date from official sources

| Line | Current Text | Verification Status |
|------|-------------|-------------------|
| 135 | `**New "funding periods"** introduced in NDIS plans (effective May 19, 2026)` | ❌ NO OFFICIAL SOURCE FOUND |

**Search Results:** Web search for "NDIS funding periods May 19 2026" OR "19 May 2026" returned ZERO results.

**Recommendation:** 
- If this date is from an official NDIA announcement, cite the source URL
- If speculative, remove or change to "announced for mid-2026"
- If the actual date is different, correct it

---

## VERIFIED CORRECT DATES

### ✅ Financial Year Logic - ALL CORRECT
- Financial year 2025-26 = July 1, 2025 to June 30, 2026 ✓
- All references to "effective July 1, 2025" for 2025-26 pricing ✓

### ✅ NDIS Pricing Arrangements v1.1 - CORRECT
- Stated as "effective 24 November 2025" throughout documents ✓
- **Source:** https://www.ndis.gov.au/providers/pricing-arrangements (official NDIA page confirms this date)

### ✅ SCHADS Award Pay Rise - CORRECT
- Stated as "3.5% increase from 1 July 2025" ✓
- Consistent with Fair Work Commission annual wage review timing ✓

### ✅ Price Increase Percentage - CORRECT
- Stated as "3.95% increase" for NDIS price limits ✓
- Consistent across all documents ✓

### ✅ National Public Holidays 2025 - ALL CORRECT (Lines 268-276 in ndis-support-worker-pay-rates.md)
- New Year's Day: 1 January 2025 (Wednesday) ✓
- Australia Day: 27 January 2025 (Monday observed) ✓
- Good Friday: 18 April 2025 (Friday) ✓
- Easter Saturday: 19 April 2025 (Saturday) ✓
- Easter Monday: 21 April 2025 (Monday) ✓
- Anzac Day: 25 April 2025 (Friday) ✓
- Christmas Day: 25 December 2025 (Thursday) ✓
- Boxing Day: 26 December 2025 (Friday) ✓

---

## SUMMARY OF ERRORS

| File | Error Type | Count | Severity |
|------|-----------|-------|----------|
| ndis-support-worker-pay-rates.md | 2026 holidays shown as 2025 | 8 errors | CRITICAL |
| ndis-support-worker-pay-rates.md | Queen's Birthday column confusion | 3 errors | HIGH |
| ndis-invoice-template-guide.md | Claim window date wrong year | 2 errors | CRITICAL |
| ndis-price-guide.md | Unverified funding periods date | 1 unverified | HIGH |

**TOTAL ERRORS:** 11 date discrepancies + 1 unverified date

---

## CONCLUSION

❌ **NOT ALL DATES ARE 100% ACCURATE**

**Required Actions:**
1. **CRITICAL:** Fix all 8 instances of 2026 holidays incorrectly showing year 2025 in ndis-support-worker-pay-rates.md (lines 282-289)
2. **CRITICAL:** Correct claim window effective date from "October 3, 2026" to "October 3, 2025" in ndis-invoice-template-guide.md (lines 17 & 474)
3. **HIGH:** Fix Queen's Birthday table header and dates in ndis-support-worker-pay-rates.md (lines 293-297)
4. **HIGH:** Verify or remove "effective May 19, 2026" funding periods claim in ndis-price-guide.md (line 135)

**Verification Sources Used:**
- NDIS official website (ndis.gov.au)
- Fair Work Ombudsman 2026 public holidays calendar
- ACT Government 2026 public holidays PDF
- Multiple NDIS provider compliance sources (PRCSA, Help at Hand, Leapin)
- Australian public holiday calendars (publicholidays.com.au)
