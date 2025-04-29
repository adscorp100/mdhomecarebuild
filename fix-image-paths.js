import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Get the directory name
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Base URL to prepend to image paths
const BASE_URL = '/mdhomecarebuild';

// Function to process a markdown file
function processMarkdownFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const hasImagePath = content.includes('image: "/');
    
    if (!hasImagePath) {
      return false; // No image path to fix
    }
    
    // Regular expression to find image paths in frontmatter
    // This looks for image: "/path/to/image.ext" format
    const imagePathRegex = /image: "\/([^"]+)"/g;
    
    // Replace with the proper base URL
    const updatedContent = content.replace(imagePathRegex, `image: "${BASE_URL}/$1"`);
    
    if (content !== updatedContent) {
      fs.writeFileSync(filePath, updatedContent);
      return true; // File was updated
    }
    
    return false; // No changes needed
  } catch (error) {
    console.error(`Error processing ${filePath}:`, error);
    return false;
  }
}

// Process all markdown files in a directory
function processDirectory(dirPath) {
  const files = fs.readdirSync(dirPath);
  let updatedCount = 0;
  
  files.forEach(file => {
    if (file.endsWith('.md')) {
      const filePath = path.join(dirPath, file);
      const updated = processMarkdownFile(filePath);
      if (updated) {
        console.log(`Updated image path in: ${filePath}`);
        updatedCount++;
      }
    }
  });
  
  return updatedCount;
}

// Process both blog and services markdown files
const servicesDir = path.join(__dirname, 'src/content/services');
const blogDir = path.join(__dirname, 'src/content/blog');

console.log('Processing service files...');
const servicesUpdated = processDirectory(servicesDir);

console.log('Processing blog files...');
const blogUpdated = processDirectory(blogDir);

console.log(`Complete! Updated ${servicesUpdated} service files and ${blogUpdated} blog files.`); 