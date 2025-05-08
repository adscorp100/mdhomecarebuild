# MD Homecare Blog Post Generator

This set of scripts makes it easy to create new blog posts for the MD Homecare website.

## Setup

1. Make sure both scripts are executable:
   ```
   chmod +x create-blog-post.sh blog-post
   ```

2. For convenience, you may want to move the `blog-post` wrapper script to a directory in your PATH:
   ```
   # Optional
   sudo cp blog-post /usr/local/bin/
   ```

## Usage

### Using the main script directly

```
./create-blog-post.sh
```

The script will prompt you for:
- Post title (required)
- Description (required)
- Publication date (defaults to tomorrow)
- Author name (defaults to 'Camila')
- Tags (comma separated)
- Featured image path (defaults to '/assets/makingbed.webp')

### Using the wrapper script

The wrapper script allows you to run the blog post generator from any directory within your project:

```
./blog-post
```

It automatically finds the project root (where package.json is located) and runs the main script.

### Getting help

For usage instructions:

```
./create-blog-post.sh --help
```

or

```
./blog-post --help
```

## How It Works

The script:

1. Prompts for post details (title, description, etc.)
2. Generates a slug from the title
3. Creates a markdown file in `src/content/blog/` with the proper frontmatter
4. Adds template sections to help structure your post

## Blog Post Structure

Each blog post consists of:

1. **Frontmatter**: Contains metadata like title, description, publication date, author, tags, and featured image.
2. **Content**: Written in Markdown format, including headings, paragraphs, lists, and links.

### Example Frontmatter

```yaml
---
title: "Home Care Package Level 3: Complete Guide"
description: "Everything you need to know about Level 3 Home Care Packages"
pubDate: 2025-03-09
author: "Camila"
tags: ["home care packages", "aged care", "level 3"]
image: "/assets/makingbed.webp"
---
```

## Post Template

The generated post includes template sections:
- Introduction
- Main content sections
- Conclusion
- FAQ section

You can customize this template by editing the `create-blog-post.sh` file.

## Troubleshooting

- **Script not found**: Make sure the path to the script is correct and the script is executable.
- **Permission denied**: Run `chmod +x create-blog-post.sh blog-post` to make the scripts executable.
- **Date command error**: The script attempts to handle different date formats for various systems. If you encounter an error, manually enter the date when prompted. 