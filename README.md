# Astro Static Site

A modern static site built with [Astro](https://astro.build/), featuring blog capabilities, responsive design, and optimized performance.

## 🚀 Project Structure

```
/
├── public/
│   ├── styles/
│   │   └── global.css     # Global styles
│   └── favicon.svg        # Site favicon
├── src/
│   ├── components/        # Reusable UI components
│   ├── content/           # Content collections (blog posts)
│   │   ├── blog/          # Blog posts (Markdown files)
│   │   └── config.ts      # Collections configuration 
│   ├── layouts/           # Page layouts
│   │   └── BaseLayout.astro # Main site layout
│   ├── pages/             # Routes and pages
│   │   ├── index.astro    # Home page
│   │   ├── about.astro    # About page
│   │   ├── contact.astro  # Contact page
│   │   └── blog/          # Blog pages
│   │       ├── index.astro # Blog index
│   │       └── [slug].astro # Dynamic blog post page
│   └── styles/            # Component/page specific styles
└── package.json          # Project dependencies
```

## 🧞 Commands

All commands are run from the root of the project, from a terminal:

| Command                | Action                                          |
| :--------------------- | :---------------------------------------------- |
| `npm install`          | Installs dependencies                           |
| `npm run dev`          | Starts local dev server at `localhost:4321`     |
| `npm run build`        | Build your production site to `./dist/`         |
| `npm run preview`      | Preview your build locally, before deploying    |
| `npm run astro ...`    | Run CLI commands like `astro add`, `astro check`|

## 🎈 Features

- **Performance-first**: Built with Astro for optimal performance
- **SEO-friendly**: Includes meta tags and sitemap generation
- **Responsive Design**: Works on all devices
- **Blog System**: Markdown-based blog with collections
- **Modern CSS**: Uses CSS variables and modern layout techniques

## 🧰 Customization

### Site Configuration

Update the site configuration in `astro.config.mjs`:

```js
export default defineConfig({
  site: 'https://your-domain.com', // Replace with your actual domain
});
```

### Content Collections

The content collections are configured in `src/content/config.ts`. You can modify the schema or add new collections as needed.

### Styling

Global styles are in `public/styles/global.css`. Component-specific styles are included within each `.astro` file.

## 📝 Adding Blog Posts

To add a new blog post, create a new Markdown file in `src/content/blog/` with the following frontmatter:

```md
---
title: "Your Post Title"
description: "A brief description of your post"
pubDate: 2023-07-14
author: "Your Name"
tags: ["tag1", "tag2"]
---

Your content here...
```

## 📚 Learn More

- [Astro documentation](https://docs.astro.build)
- [Astro Content Collections](https://docs.astro.build/en/guides/content-collections/)
- [Markdown in Astro](https://docs.astro.build/en/guides/markdown-content/)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. 