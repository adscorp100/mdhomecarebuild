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
    '/blog/where-buy-sell-second-hand-disability-equipment-australia': '/blog/guide-buying-selling-donating-second-hand-disability-equipment-australia-2025',
    '/blog/where-buy-sell-second-hand-disability-equipment-australia/': '/blog/guide-buying-selling-donating-second-hand-disability-equipment-australia-2025/',
    // NDIS Independent Support Worker page consolidation - redirect duplicate blog posts to main guide
    '/blog/becoming-an-independent-ndis-support-worker-your-ultimate-2025-guide': '/blog/guide-to-becoming-an-independent-support-worker',
    '/blog/becoming-an-independent-ndis-support-worker-your-ultimate-2025-guide/': '/blog/guide-to-becoming-an-independent-support-worker/',
    '/blog/how-to-work-as-independent-ndis-support-worker': '/blog/guide-to-becoming-an-independent-support-worker',
    '/blog/how-to-work-as-independent-ndis-support-worker/': '/blog/guide-to-becoming-an-independent-support-worker/',
    // STA page consolidation - redirect duplicate STA blog posts to main comprehensive guide
    '/blog/understanding-sta-meaning-in-ndis': '/blog/ndis-respite-sta-accommodation-guide-2025',
    '/blog/understanding-sta-meaning-in-ndis/': '/blog/ndis-respite-sta-accommodation-guide-2025/',
    '/blog/ndis-respite-sta-short-term-accommodation-guide-2025': '/blog/ndis-respite-sta-accommodation-guide-2025',
    '/blog/ndis-respite-sta-short-term-accommodation-guide-2025/': '/blog/ndis-respite-sta-accommodation-guide-2025/',
    '/blog/ndis-respite-sta-pricing-guide-2024-25': '/blog/ndis-respite-sta-accommodation-guide-2025',
    '/blog/ndis-respite-sta-pricing-guide-2024-25/': '/blog/ndis-respite-sta-accommodation-guide-2025/',
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
