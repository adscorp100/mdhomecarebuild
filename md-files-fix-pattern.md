# Markdown File Issues and Fix Pattern

## Common Issues Found

1. **Empty Headings**: Many files have headings (## or ###) with no text after them, followed by combined heading text and paragraph.
   - Example: `## ` followed by `Service Name in {suburb}Our service details...`

2. **No Space After Heading**: Heading text and paragraph text are combined without proper spacing.
   - Example: `## Service NameThis is the description` (missing space after "Name")

3. **Split Content**: In some cases, section titles are on the heading line but content starts without proper spacing.

4. **Broken Formatting**: Some files have broken formatting, especially at the end of files.

## Fix Pattern

For each file, apply these fixes:

1. For empty headings (## or ### with no text):
   - Take the first part of the next line as the heading text
   - Add a blank line after the heading
   - The rest of the text becomes a separate paragraph

2. For headings with combined text:
   - Add a space between the heading text and paragraph text
   - Add a blank line after the heading

3. For all markdown files:
   - Ensure consistent spacing before and after all headings
   - Check for any broken formatting at the end of files

## Files Already Fixed

1. src/content/services/aged-care-home-modifications-maintenance.md
2. src/content/services/community-access-support.md
3. src/content/services/respite-care.md
4. src/content/services/therapy-services.md
5. src/content/services/disability-services.md
6. src/content/services/clinical-care.md

## Files Still Needing Fixes

Review and fix remaining files in src/content/services/ directory:
- transport-services.md
- domestic-assistance.md
- personal-care.md
- sil-services.md
- specialist-disability-accommodation.md
- disability-home-support-services.md
- support-workers.md
- ndis-behaviour-support-practitioner-training.md
- ndis-specialist-support-coordination.md

## Manual Process for Each File

1. Read the file to identify issues
2. Edit file to fix headings and spacing
3. Ensure text flows naturally from headings to paragraphs
4. Fix any additional formatting issues

This pattern ensures consistent, well-formatted markdown files across all service pages. 