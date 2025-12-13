// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: 'https://mdhomecare.com.au',
  output: 'static', // Explicitly set to static (default)
  compressHTML: true, // Minify HTML output
  integrations: [
    sitemap({
      changefreq: 'weekly',
      priority: 0.7,
      lastmod: new Date(),
      filter: (page) =>
        // Exclude any pages you don't want in the sitemap
        !page.includes('/private/'),
    }),
  ],
  vite: {
    plugins: [tailwindcss()],
  },
});
