// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://mdhomecare.com.au',
  output: 'static', // Explicitly set to static (default)
  compressHTML: true, // Minify HTML output
  integrations: [
    sitemap(),
  ],
});
