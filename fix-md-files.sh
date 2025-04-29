#!/bin/bash

# Script to fix markdown files with empty headings
# It finds lines with just ## or ### and properly formats them with the title

for file in src/content/services/*.md; do
  echo "Processing $file..."
  
  # Create a temporary file
  temp_file=$(mktemp)
  
  # Use awk to process the file
  awk '
  # If line is just ## or ### followed by nothing
  /^##\s*$/ || /^###\s*$/ {
    heading = $0;  # Store the heading marker
    getline;       # Move to the next line
    # Print the heading followed by the title (removing the title from the next line)
    if ($0 ~ /^[^-*]/) {  # If the next line is text (not a list item)
      title = $0;
      sub(/[A-Za-z].*/, "", title);  # Remove everything after the first word
      content = $0;
      sub(/^[^A-Za-z]*/, "", content);  # Remove non-alphabetic characters from start
      print heading " " content;
      print "";  # Add an empty line after the heading
    } else {
      # If the next line is a list item or something else
      print heading;
      print "";  # Add an empty line after the heading
      print $0;  # Print the original next line
    }
    next;
  }
  
  # Print all other lines normally
  { print }
  ' "$file" > "$temp_file"
  
  # Replace original file with the fixed version
  mv "$temp_file" "$file"
done

echo "All markdown files processed." 