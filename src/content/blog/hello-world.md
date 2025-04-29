---
title: "Hello, World! Welcome to Our Blog"
description: "This is our first blog post in our new Astro site."
pubDate: 2023-07-14
author: "Jane Doe"
tags: ["astro", "web development", "static site"]
---

# Hello, World!

Welcome to our first blog post on our brand new Astro-powered website. In this post, we'll explore what makes Astro so special for building modern static websites.

## Why Astro?

Astro is a modern framework for building static websites that offers several advantages:

1. **Performance-first**: Astro ships zero JavaScript to the client by default, resulting in incredibly fast page loads.
2. **Component Islands**: Use UI components from React, Vue, Svelte, and more, but only hydrate them when necessary.
3. **Content-focused**: Perfect for content-heavy websites like blogs, documentation, and marketing sites.
4. **Flexible**: Build sites your way with support for Markdown, MDX, and any front-end framework.

## Getting Started

To create a new Astro project, run one of the following commands:

```bash
# Using npm
npm create astro@latest

# Using Yarn
yarn create astro

# Using pnpm
pnpm create astro@latest
```

## Code Example

Here's a simple Astro component:

```astro
---
// Your component script goes here
const title = "Hello, Astro!";
---

<div>
  <h1>{title}</h1>
  <p>This is an Astro component.</p>
</div>

<style>
  h1 {
    color: purple;
  }
</style>
```

## What's Next?

In future blog posts, we'll dive deeper into Astro's features and show you how to build amazing websites with this powerful tool. Stay tuned for tutorials, tips, and best practices!

Thanks for reading, and welcome to our blog! 