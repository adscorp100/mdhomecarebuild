import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Get the directory name
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const servicesDir = path.join(__dirname, 'src/content/services');
const files = fs.readdirSync(servicesDir).filter(file => 
  file.endsWith('.md') && 
  file !== 'domestic-assistance.md' && 
  file !== 'transport-services.md'
);

files.forEach(file => {
  const filePath = path.join(servicesDir, file);
  let content = fs.readFileSync(filePath, 'utf8');
  
  // Step 1: Fix empty lines after headings followed by blank lines
  content = content.replace(/^(#{2,3}[^\n]*)\n\n+\n+/gm, '$1\n\n');
  
  // Step 2: Fix heading lines with heading text attached to content
  content = content.replace(/^(##[^\n]*?)([A-Za-z])/gm, '$1\n\n$2');
  content = content.replace(/^(###[^\n]*?)([A-Za-z])/gm, '$1\n\n$2');
  
  // Step 3: Fix link formatting at the end
  content = content.replace(/## \[\n\n([^\]]+)\]\(([^)]+)\)/gm, '## [$1]($2)');
  
  fs.writeFileSync(filePath, content);
  console.log(`Fixed formatting in ${file}`);
});

console.log(`Fixed ${files.length} service files.`); 