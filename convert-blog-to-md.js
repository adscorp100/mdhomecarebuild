#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';

// Get the directory name and filename using ES module approach
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const SOURCE_DIR = path.join(__dirname, 'src/data/blog');
const TARGET_DIR = path.join(__dirname, 'src/content/blog');

// Ensure target directory exists
if (!fs.existsSync(TARGET_DIR)) {
  fs.mkdirSync(TARGET_DIR, { recursive: true });
}

// Get all JSON files in the source directory
const jsonFiles = fs.readdirSync(SOURCE_DIR)
  .filter(file => file.endsWith('.json') && file !== 'posts.json');

console.log(`Found ${jsonFiles.length} blog posts to convert`);

// Process each JSON file
jsonFiles.forEach(jsonFile => {
  const filePath = path.join(SOURCE_DIR, jsonFile);
  
  try {
    // Read and parse the JSON file
    const fileContent = fs.readFileSync(filePath, 'utf8');
    const blogPost = JSON.parse(fileContent);
    
    // Format the date correctly for Astro (YYYY-MM-DD)
    let pubDate = blogPost.date;
    if (!pubDate) {
      // If date is missing, use current date
      const now = new Date();
      pubDate = now.toISOString().split('T')[0];
    } else {
      // Ensure date is in YYYY-MM-DD format
      pubDate = new Date(pubDate).toISOString().split('T')[0];
    }
    
    // Create the frontmatter
    const frontmatter = {
      title: blogPost.title,
      description: blogPost.description || "No description provided",
      pubDate: pubDate,
      author: "MD Home Care", // Default author
      tags: [], // Default empty tags array
      image: blogPost.image || undefined
    };
    
    // Convert HTML content to Markdown
    let content = blogPost.content;
    
    // Remove HTML tags to create a basic Markdown version
    // In a real-world scenario, you might want to use a proper HTML-to-Markdown converter
    content = content
      .replace(/<h1[^>]*>(.*?)<\/h1>/gi, '# $1')
      .replace(/<h2[^>]*>(.*?)<\/h2>/gi, '## $1')
      .replace(/<h3[^>]*>(.*?)<\/h3>/gi, '### $1')
      .replace(/<h4[^>]*>(.*?)<\/h4>/gi, '#### $1')
      .replace(/<h5[^>]*>(.*?)<\/h5>/gi, '##### $1')
      .replace(/<h6[^>]*>(.*?)<\/h6>/gi, '###### $1')
      .replace(/<p[^>]*>(.*?)<\/p>/gi, '$1\n\n')
      .replace(/<strong[^>]*>(.*?)<\/strong>/gi, '**$1**')
      .replace(/<em[^>]*>(.*?)<\/em>/gi, '*$1*')
      .replace(/<ul[^>]*>(.*?)<\/ul>/gis, '$1\n')
      .replace(/<ol[^>]*>(.*?)<\/ol>/gis, '$1\n')
      .replace(/<li[^>]*>(.*?)<\/li>/gi, '- $1\n')
      .replace(/<a[^>]*href="([^"]*)"[^>]*>(.*?)<\/a>/gi, '[$2]($1)')
      .replace(/<div[^>]*>(.*?)<\/div>/gis, '$1\n')
      .replace(/<br\s*\/?>/gi, '\n')
      .replace(/<[^>]*>/g, '') // Remove any remaining HTML tags
      .replace(/&nbsp;/g, ' ')
      .replace(/&amp;/g, '&')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .replace(/&quot;/g, '"')
      .replace(/&#39;/g, "'")
      .replace(/\n\s*\n\s*\n/g, '\n\n') // Remove excessive newlines
      .trim();
    
    // Create the Markdown content
    const markdown = `---
title: ${JSON.stringify(frontmatter.title)}
description: ${JSON.stringify(frontmatter.description)}
pubDate: ${frontmatter.pubDate}
author: ${JSON.stringify(frontmatter.author)}
tags: [${frontmatter.tags.map(tag => JSON.stringify(tag)).join(', ')}]
${frontmatter.image ? `image: ${JSON.stringify(frontmatter.image)}` : ''}
---

${content}
`;
    
    // Create the output file path
    const slug = blogPost.slug || jsonFile.replace('.json', '');
    const outputPath = path.join(TARGET_DIR, `${slug}.md`);
    
    // Write the Markdown file
    fs.writeFileSync(outputPath, markdown);
    
    console.log(`Converted: ${jsonFile} -> ${slug}.md`);
  } catch (error) {
    console.error(`Error processing ${jsonFile}:`, error.message);
  }
});

console.log('Conversion complete!'); 