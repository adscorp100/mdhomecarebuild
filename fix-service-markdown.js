import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Get the directory name
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const servicesDir = path.join(__dirname, 'src/content/services');
const files = fs.readdirSync(servicesDir).filter(file => file.endsWith('.md'));

files.forEach(file => {
  if (file === 'domestic-assistance.md') {
    // Skip this one as we've already fixed it manually
    console.log(`Skipping ${file} (already fixed manually)`);
    return;
  }
  
  const filePath = path.join(servicesDir, file);
  let content = fs.readFileSync(filePath, 'utf8');
  
  // Replace merged headings and text
  // Find headings (## or ### followed by text) then find cases where there's no newline before the next word
  content = content.replace(/^(#{2,3}\s+[^{]*?{[^}]+})((?:Our|Who|When|This|The|These|Arranging|Getting|Contact)[A-Za-z])/gm, 
                            '$1\n\n$2');
  
  // Store the original content to check if changes were made
  const originalContent = content;
  
  // Process line by line for more complex patterns
  const lines = content.split('\n');
  const newLines = [];
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    // If the line is a heading
    if (line.startsWith('##') || line.startsWith('###')) {
      // Add the heading
      newLines.push(line);
      
      // Check if next line exists and isn't empty and isn't a heading
      if (i + 1 < lines.length && 
          lines[i + 1].trim() !== '' && 
          !lines[i + 1].startsWith('#')) {
        
        // Add an empty line after the heading
        newLines.push('');
      }
    } else {
      newLines.push(line);
    }
  }
  
  // Convert back to string
  const newContent = newLines.join('\n');
  
  // Only write if content has changed
  if (newContent !== originalContent) {
    fs.writeFileSync(filePath, newContent);
    console.log(`Fixed formatting in ${file}`);
  } else {
    console.log(`No changes needed in ${file}`);
  }
});

console.log(`Processed ${files.length} service files.`); 