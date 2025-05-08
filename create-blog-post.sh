#!/bin/bash

# create-blog-post.sh - Quick blog post generator for MD Homecare Astro site
# Author: Claude Assistant

# Text styling
BOLD='\033[1m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Check for help flag
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  echo -e "${BOLD}${GREEN}MD Homecare Blog Post Generator - Help${NC}"
  echo -e "This script creates a new blog post markdown file in the src/content/blog directory."
  echo -e "\nUsage:"
  echo -e "  ./create-blog-post.sh [options]"
  echo -e "\nOptions:"
  echo -e "  -h, --help    Display this help message"
  echo -e "\nThe script will prompt you for:"
  echo -e "  - Post title (required)"
  echo -e "  - Description (required)"
  echo -e "  - Publication date (defaults to tomorrow)"
  echo -e "  - Author name (defaults to 'Camila')"
  echo -e "  - Tags (comma separated)"
  echo -e "  - Featured image path (defaults to '/assets/makingbed.webp')"
  echo -e "\nThe script automatically generates a slug from the title."
  echo -e "Example: 'How to Apply for NDIS Funding' becomes 'how-to-apply-for-ndis-funding'"
  exit 0
fi

# Display banner
echo -e "${BOLD}${GREEN}MD Homecare Blog Post Generator${NC}"
echo -e "Create a new blog post in seconds\n"

# Get post details with interactive prompts
read -p "$(echo -e "${BOLD}Enter post title:${NC} ")" title
read -p "$(echo -e "${BOLD}Enter short description:${NC} ")" description

# Set default date to tomorrow (common for scheduling posts)
# This is a cross-platform compatible way to get tomorrow's date
if [[ "$OSTYPE" == "darwin"* ]]; then
  # macOS
  tomorrow=$(date -v+1d +%Y-%m-%d)
else
  # Linux and others
  tomorrow=$(date -d "tomorrow" +%Y-%m-%d 2>/dev/null || date -j -v+1d +%Y-%m-%d 2>/dev/null || date +%Y-%m-%d)
fi
read -p "$(echo -e "${BOLD}Enter publication date (YYYY-MM-DD) [default: $tomorrow]:${NC} ")" pubDate
pubDate=${pubDate:-$tomorrow}

# Default author prompt
read -p "$(echo -e "${BOLD}Enter author name [default: Camila]:${NC} ")" author
author=${author:-"Camila"}

# Tags with examples
echo -e "${BOLD}Enter tags (comma separated):${NC}"
echo -e "${BLUE}Examples: aged care, home care packages, ndis, disability support${NC}"
read tags

# Default image
read -p "$(echo -e "${BOLD}Enter image path [default: /assets/makingbed.webp]:${NC} ")" image
image=${image:-"/assets/makingbed.webp"}

# Create slug from title
slug=$(echo "$title" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//' | sed 's/-$//')

# Format tags for the frontmatter
formatted_tags=""
IFS=',' read -ra TAG_ARRAY <<< "$tags"
for i in "${TAG_ARRAY[@]}"; do
  # Trim whitespace and add to formatted string
  tag=$(echo "$i" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
  formatted_tags+="\"$tag\", "
done
# Remove trailing comma and space
formatted_tags=${formatted_tags%, }

# Create the blog post file
blog_dir="src/content/blog"
mkdir -p "$blog_dir"
file_path="$blog_dir/$slug.md"

# Check if file already exists
if [ -f "$file_path" ]; then
  echo -e "${BOLD}${YELLOW}Warning: A post with this slug already exists.${NC}"
  read -p "Do you want to overwrite it? (y/n): " overwrite
  if [ "$overwrite" != "y" ]; then
    echo "Operation cancelled."
    exit 1
  fi
fi

# Create the blog post with front matter and template content
cat > "$file_path" << EOL
---
title: "$title"
description: "$description"
pubDate: $pubDate
author: "$author"
tags: [$formatted_tags]
image: "$image"
---

## Introduction
Start with an engaging introduction to the topic. Explain why this information is valuable to readers and what they'll learn.

## Main Section 1
Add your first key point or section here. Include relevant information, statistics, or examples to support your points.

## Main Section 2
Continue with additional information in a logical flow. Break complex topics into digestible sections.

## Main Section 3
Provide more detailed information, practical advice, or step-by-step instructions if applicable.

## Conclusion
Summarize the key takeaways and encourage readers to take action or explore related resources.

## Frequently Asked Questions

### What is [Topic]?
Answer the first common question about your topic.

### How does [Topic] work?
Answer another common question with clear, concise information.

### Who is eligible for [Topic]?
Provide eligibility criteria or requirements if applicable.
EOL

echo -e "\n${GREEN}✓ Blog post created successfully!${NC}"
echo -e "File: ${BLUE}$file_path${NC}"
echo -e "\nYou can now edit this file to add your content."
echo -e "Run 'npm run dev' to preview your blog post locally." 