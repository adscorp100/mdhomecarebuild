// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';
import icon from 'astro-icon';

// https://astro.build/config
export default defineConfig({
  site: 'https://mdhomecare.com.au',
  output: 'static', // Explicitly set to static (default)
  compressHTML: true, // Minify HTML output
  redirects: {
    // FCA page consolidation - redirect duplicate blog posts to main FCA guide
    '/blog/functional-capacity-assessment-what-it-is-and-why-it-matters': '/blog/functional-capacity-assessment-report-example-what-a-good-one-looks-like',
    '/blog/functional-capacity-assessment-what-it-is-and-why-it-matters/': '/blog/functional-capacity-assessment-report-example-what-a-good-one-looks-like/',
    '/blog/functional-capacity-assessment-guide-ndis-2025': '/blog/functional-capacity-assessment-report-example-what-a-good-one-looks-like',
    '/blog/functional-capacity-assessment-guide-ndis-2025/': '/blog/functional-capacity-assessment-report-example-what-a-good-one-looks-like/',
    '/blog/functional-capacity-assessment-ultimate-guide-2025': '/blog/functional-capacity-assessment-report-example-what-a-good-one-looks-like',
    '/blog/functional-capacity-assessment-ultimate-guide-2025/': '/blog/functional-capacity-assessment-report-example-what-a-good-one-looks-like/',
    '/blog/functional-capacity-assessments-in-the-ndis': '/blog/functional-capacity-assessment-report-example-what-a-good-one-looks-like',
    '/blog/functional-capacity-assessments-in-the-ndis/': '/blog/functional-capacity-assessment-report-example-what-a-good-one-looks-like/',
    // Second-hand disability equipment page consolidation
    '/blog/where-buy-sell-second-hand-disability-equipment-australia': '/blog/guide-buying-selling-donating-second-hand-disability-equipment-australia',
    '/blog/where-buy-sell-second-hand-disability-equipment-australia/': '/blog/guide-buying-selling-donating-second-hand-disability-equipment-australia/',
    '/blog/guide-buying-selling-donating-second-hand-disability-equipment-australia-2025': '/blog/guide-buying-selling-donating-second-hand-disability-equipment-australia',
    '/blog/guide-buying-selling-donating-second-hand-disability-equipment-australia-2025/': '/blog/guide-buying-selling-donating-second-hand-disability-equipment-australia/',
    // NDIS Independent Support Worker page consolidation - redirect duplicate blog posts to main guide
    '/blog/becoming-an-independent-ndis-support-worker-your-ultimate-2025-guide': '/blog/guide-to-becoming-an-independent-support-worker',
    '/blog/becoming-an-independent-ndis-support-worker-your-ultimate-2025-guide/': '/blog/guide-to-becoming-an-independent-support-worker/',
    '/blog/how-to-work-as-independent-ndis-support-worker': '/blog/guide-to-becoming-an-independent-support-worker',
    '/blog/how-to-work-as-independent-ndis-support-worker/': '/blog/guide-to-becoming-an-independent-support-worker/',
    // STA page consolidation - redirect duplicate STA blog posts to main comprehensive guide
    '/blog/understanding-sta-meaning-in-ndis': '/blog/ndis-respite-sta-accommodation-guide',
    '/blog/understanding-sta-meaning-in-ndis/': '/blog/ndis-respite-sta-accommodation-guide/',
    '/blog/ndis-respite-sta-short-term-accommodation-guide-2025': '/blog/ndis-respite-sta-accommodation-guide',
    '/blog/ndis-respite-sta-short-term-accommodation-guide-2025/': '/blog/ndis-respite-sta-accommodation-guide/',
    '/blog/ndis-respite-sta-pricing-guide-2024-25': '/blog/ndis-respite-sta-accommodation-guide',
    '/blog/ndis-respite-sta-pricing-guide-2024-25/': '/blog/ndis-respite-sta-accommodation-guide/',
    '/blog/ndis-respite-sta-accommodation-guide-2025': '/blog/ndis-respite-sta-accommodation-guide',
    '/blog/ndis-respite-sta-accommodation-guide-2025/': '/blog/ndis-respite-sta-accommodation-guide/',
    // Finding NDIS Clients page consolidation
    '/blog/how-to-find-get-ndis-clients-support-worker': '/blog/how-to-find-ndis-clients-participants-guide',
    '/blog/how-to-find-get-ndis-clients-support-worker/': '/blog/how-to-find-ndis-clients-participants-guide/',
    // NDIS Support Worker Pay Rates page consolidation - redirect duplicates to main comprehensive guide
    '/blog/ndis-support-worker-hourly-rate-2025': '/blog/ndis-support-worker-hourly-rate',
    '/blog/ndis-support-worker-hourly-rate-2025/': '/blog/ndis-support-worker-hourly-rate/',
    '/blog/ndis-pay-rates-for-support-workers-2025': '/blog/ndis-pay-rates-for-support-workers',
    '/blog/ndis-pay-rates-for-support-workers-2025/': '/blog/ndis-pay-rates-for-support-workers/',
    // Disability Support Pension page consolidation - redirect to comprehensive rates guide
    '/blog/disability-support-pension-australia': '/blog/how-much-disability-pension-per-fortnight',
    '/blog/disability-support-pension-australia/': '/blog/how-much-disability-pension-per-fortnight/',
    '/blog/how-much-disability-pension-per-fortnight-2025': '/blog/how-much-disability-pension-per-fortnight',
    '/blog/how-much-disability-pension-per-fortnight-2025/': '/blog/how-much-disability-pension-per-fortnight/',

    // Year-specific redirects (2025 → year-agnostic URLs)
    '/blog/autism-school-holiday-programs-melbourne-2025': '/blog/autism-school-holiday-programs-melbourne',
    '/blog/autism-school-holiday-programs-melbourne-2025/': '/blog/autism-school-holiday-programs-melbourne/',
    '/blog/complete-guide-ndis-worker-screening-check-2025': '/blog/complete-guide-ndis-worker-screening-check',
    '/blog/complete-guide-ndis-worker-screening-check-2025/': '/blog/complete-guide-ndis-worker-screening-check/',
    '/blog/disability-support-worker-australia-2025': '/blog/disability-support-worker-australia',
    '/blog/disability-support-worker-australia-2025/': '/blog/disability-support-worker-australia/',
    '/blog/hireup-support-worker-rates-guide-2025': '/blog/hireup-support-worker-rates-guide',
    '/blog/hireup-support-worker-rates-guide-2025/': '/blog/hireup-support-worker-rates-guide/',
    '/blog/how-to-become-ndis-provider-australia-2025': '/blog/how-to-become-ndis-provider-australia',
    '/blog/how-to-become-ndis-provider-australia-2025/': '/blog/how-to-become-ndis-provider-australia/',
    '/blog/how-to-become-psychosocial-recovery-coach-ndis-2025': '/blog/how-to-become-psychosocial-recovery-coach-ndis',
    '/blog/how-to-become-psychosocial-recovery-coach-ndis-2025/': '/blog/how-to-become-psychosocial-recovery-coach-ndis/',
    '/blog/how-to-get-support-worker-insurance-in-australia-a-2025-guide': '/blog/how-to-get-support-worker-insurance-in-australia',
    '/blog/how-to-get-support-worker-insurance-in-australia-a-2025-guide/': '/blog/how-to-get-support-worker-insurance-in-australia/',
    '/blog/how-to-start-a-successful-ndis-business-in-australia-the-ultimate-2025-guide': '/blog/how-to-start-a-successful-ndis-business-in-australia',
    '/blog/how-to-start-a-successful-ndis-business-in-australia-the-ultimate-2025-guide/': '/blog/how-to-start-a-successful-ndis-business-in-australia/',
    '/blog/is-being-a-support-worker-worth-it-in-2025-pay-lifestyle-and-challenges': '/blog/is-being-a-support-worker-worth-it-pay-lifestyle-and-challenges',
    '/blog/is-being-a-support-worker-worth-it-in-2025-pay-lifestyle-and-challenges/': '/blog/is-being-a-support-worker-worth-it-pay-lifestyle-and-challenges/',
    '/blog/mable-support-workers-ndis-2025': '/blog/mable-support-workers-ndis',
    '/blog/mable-support-workers-ndis-2025/': '/blog/mable-support-workers-ndis/',
    '/blog/mable-support-workers-ndis-complete-guide-2025': '/blog/mable-support-workers-ndis-complete-guide',
    '/blog/mable-support-workers-ndis-complete-guide-2025/': '/blog/mable-support-workers-ndis-complete-guide/',
    '/blog/myplace-portal-ndis-complete-guide-2025': '/blog/myplace-portal-ndis-complete-guide',
    '/blog/myplace-portal-ndis-complete-guide-2025/': '/blog/myplace-portal-ndis-complete-guide/',
    '/blog/ndis-capacity-building-supports-complete-guide-2025': '/blog/ndis-capacity-building-supports-complete-guide',
    '/blog/ndis-capacity-building-supports-complete-guide-2025/': '/blog/ndis-capacity-building-supports-complete-guide/',
    '/blog/ndis-eligibility-requirements-complete-guide-2025': '/blog/ndis-eligibility-requirements-complete-guide',
    '/blog/ndis-eligibility-requirements-complete-guide-2025/': '/blog/ndis-eligibility-requirements-complete-guide/',
    '/blog/ndis-goals-examples-smart-planning-guide-2025': '/blog/ndis-goals-examples-smart-planning-guide',
    '/blog/ndis-goals-examples-smart-planning-guide-2025/': '/blog/ndis-goals-examples-smart-planning-guide/',
    '/blog/ndis-improved-daily-living-cb-daily-activity-guide-2025': '/blog/ndis-improved-daily-living-cb-daily-activity-guide',
    '/blog/ndis-improved-daily-living-cb-daily-activity-guide-2025/': '/blog/ndis-improved-daily-living-cb-daily-activity-guide/',
    '/blog/ndis-invoice-template-guide-2025': '/blog/ndis-invoice-template-guide',
    '/blog/ndis-invoice-template-guide-2025/': '/blog/ndis-invoice-template-guide/',
    '/blog/ndis-news-latest-updates-australia-2025': '/blog/ndis-news-latest-updates-australia',
    '/blog/ndis-news-latest-updates-australia-2025/': '/blog/ndis-news-latest-updates-australia/',
    '/blog/ndis-pace-system-participant-guide-2025': '/blog/ndis-pace-system-participant-guide',
    '/blog/ndis-pace-system-participant-guide-2025/': '/blog/ndis-pace-system-participant-guide/',
    '/blog/ndis-plan-manager-complete-guide-2025': '/blog/ndis-plan-manager-complete-guide',
    '/blog/ndis-plan-manager-complete-guide-2025/': '/blog/ndis-plan-manager-complete-guide/',
    '/blog/ndis-provider-application-process-guide-2025': '/blog/ndis-provider-application-process-guide',
    '/blog/ndis-provider-application-process-guide-2025/': '/blog/ndis-provider-application-process-guide/',
    '/blog/ndis-provider-cost-guide-2025': '/blog/ndis-provider-cost-guide',
    '/blog/ndis-provider-cost-guide-2025/': '/blog/ndis-provider-cost-guide/',
    '/blog/ndis-support-categories-consumables-guide-2025': '/blog/ndis-support-categories-consumables-guide',
    '/blog/ndis-support-categories-consumables-guide-2025/': '/blog/ndis-support-categories-consumables-guide/',
    '/blog/ndis-therapy-assistant-guide-role-qualifications-funding-2025': '/blog/ndis-therapy-assistant-guide-role-qualifications-funding',
    '/blog/ndis-therapy-assistant-guide-role-qualifications-funding-2025/': '/blog/ndis-therapy-assistant-guide-role-qualifications-funding/',
    '/blog/ndis-worker-screening-check-complete-guide-2025': '/blog/ndis-worker-screening-check-complete-guide',
    '/blog/ndis-worker-screening-check-complete-guide-2025/': '/blog/ndis-worker-screening-check-complete-guide/',
    '/blog/sda-calculator-specialist-disability-accommodation-2025': '/blog/sda-calculator-specialist-disability-accommodation',
    '/blog/sda-calculator-specialist-disability-accommodation-2025/': '/blog/sda-calculator-specialist-disability-accommodation/',
    '/blog/sil-sles-ndis-funding-guide-2025': '/blog/sil-sles-ndis-funding-guide',
    '/blog/sil-sles-ndis-funding-guide-2025/': '/blog/sil-sles-ndis-funding-guide/',
    '/blog/support-at-home-prices-2025': '/blog/support-at-home-prices',
    '/blog/support-at-home-prices-2025/': '/blog/support-at-home-prices/',
    '/blog/support-at-home-program-2025-complete-guide': '/blog/support-at-home-program-complete-guide',
    '/blog/support-at-home-program-2025-complete-guide/': '/blog/support-at-home-program-complete-guide/',
    '/blog/top-20-ndis-providers-melbourne-2025': '/blog/top-20-ndis-providers-melbourne',
    '/blog/top-20-ndis-providers-melbourne-2025/': '/blog/top-20-ndis-providers-melbourne/',
  },
  integrations: [
    icon(),
    sitemap({
      changefreq: 'weekly',
      priority: 0.7,
      lastmod: new Date(),
      filter: (page) =>
        // Exclude any pages you don't want in the sitemap
        !page.includes('/private/'),
      serialize(item) {
        // Main service pages: highest priority (canonical pages)
        if (item.url.match(/\/services\/[^\/]+\/?$/)) {
          item.priority = 0.9;
          item.changefreq = 'weekly';
        }
        // Suburb-specific service pages: medium-high priority (long-tail keywords)
        else if (item.url.match(/\/services\/[^\/]+\/[^\/]+\/?$/)) {
          item.priority = 0.7;
          item.changefreq = 'monthly';
        }
        // Tools pages: high priority (interactive content)
        else if (item.url.includes('/tools/')) {
          item.priority = 0.9;
          item.changefreq = 'monthly';
        }
        // Blog posts: high priority (content marketing)
        else if (item.url.includes('/blog/')) {
          item.priority = 0.8;
          item.changefreq = 'weekly';
        }
        // Jobs pages
        else if (item.url.includes('/jobs/')) {
          item.priority = 0.6;
          item.changefreq = 'weekly';
        }
        // Homepage
        else if (item.url === 'https://mdhomecare.com.au/' || item.url === 'https://mdhomecare.com.au') {
          item.priority = 1.0;
          item.changefreq = 'daily';
        }
        // Services index
        else if (item.url === 'https://mdhomecare.com.au/services/' || item.url === 'https://mdhomecare.com.au/services') {
          item.priority = 0.9;
          item.changefreq = 'weekly';
        }
        return item;
      },
    }),
  ],
  vite: {
    plugins: [tailwindcss()],
  },
});
