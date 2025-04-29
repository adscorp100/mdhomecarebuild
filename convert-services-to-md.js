#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Get the directory name and filename using ES module approach
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const SOURCE_DIR = path.join(__dirname, 'src/data/services');
const TARGET_DIR = path.join(__dirname, 'src/content/services');

// Ensure target directory exists
if (!fs.existsSync(TARGET_DIR)) {
  fs.mkdirSync(TARGET_DIR, { recursive: true });
}

// Get all JSON files in the source directory
const jsonFiles = fs.readdirSync(SOURCE_DIR)
  .filter(file => file.endsWith('.json') && file !== 'services.json');

console.log(`Found ${jsonFiles.length} services to convert`);

// Process each JSON file
jsonFiles.forEach(jsonFile => {
  const filePath = path.join(SOURCE_DIR, jsonFile);
  
  try {
    // Read and parse the JSON file
    const fileContent = fs.readFileSync(filePath, 'utf8');
    const service = JSON.parse(fileContent);
    
    // Format the date correctly for Astro (YYYY-MM-DD)
    let pubDate = service.date;
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
      title: service.title,
      description: service.description || "No description provided",
      pubDate: pubDate,
      category: service.category || "Services",
      image: service.image || undefined,
      keywords: service.keywords || []
    };
    
    // Convert HTML content to Markdown if it exists
    let content = service.content || "";
    
    if (content) {
      // Remove HTML tags to create a basic Markdown version
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
    }
    
    // Create the Markdown content
    const markdown = `---
title: ${JSON.stringify(frontmatter.title)}
description: ${JSON.stringify(frontmatter.description)}
pubDate: ${frontmatter.pubDate}
category: ${JSON.stringify(frontmatter.category)}
${frontmatter.image ? `image: ${JSON.stringify(frontmatter.image)}` : ''}
${frontmatter.keywords && frontmatter.keywords.length > 0 ? `keywords: [${frontmatter.keywords.map(kw => JSON.stringify(kw)).join(', ')}]` : ''}
---

${content}
`;
    
    // Create the output file path
    const slug = service.slug || jsonFile.replace('.json', '');
    const outputPath = path.join(TARGET_DIR, `${slug}.md`);
    
    // Write the Markdown file
    fs.writeFileSync(outputPath, markdown);
    
    console.log(`Converted: ${jsonFile} -> ${slug}.md`);
  } catch (error) {
    console.error(`Error processing ${jsonFile}:`, error.message);
  }
});

console.log('Conversion complete!');

// Now update the content collection config to include the services collection
const contentConfigPath = path.join(__dirname, 'src/content/config.ts');
let contentConfig = '';

try {
  contentConfig = fs.readFileSync(contentConfigPath, 'utf8');
  
  // Check if services collection already exists
  if (!contentConfig.includes("'services':")) {
    // Add services collection to the config
    contentConfig = contentConfig.replace(
      'export const collections = {', 
      `const services = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.date(),
    category: z.string(),
    image: z.string().optional(),
    keywords: z.array(z.string()).default([]),
  }),
});

export const collections = {`
    );
    
    // Add services to collections
    contentConfig = contentConfig.replace(
      "'blog': blog,", 
      "'blog': blog,\n  'services': services,"
    );
    
    // Write updated config
    fs.writeFileSync(contentConfigPath, contentConfig);
    console.log('Updated content config to include services collection');
  } else {
    console.log('Services collection already exists in config');
  }
} catch (error) {
  console.error('Error updating content config:', error.message);
} 