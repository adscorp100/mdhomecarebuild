import json
import pandas as pd
import sys
import io

# Load the list of Australian suburbs
with open('data/australian-suburbs.json', 'r') as f:
    suburbs_data = json.load(f)
    suburbs = set(key.lower() for key in suburbs_data.keys())

def sanitize_query(query):
    """Removes suburb names from a search query."""
    words = query.lower().split()
    # Remove words that are suburbs and common geo-qualifiers
    sanitized_words = [word for word in words if word not in suburbs and word not in ['near', 'me', 'in']]
    # Also remove postcodes and other numeric-heavy words that are likely geo related
    sanitized_words = [word for word in sanitized_words if not any(char.isdigit() for char in word)]
    return ' '.join(sanitized_words)

def process_gsc_data(input_data):
    # Find the start of the keyword list
    lines = input_data.strip().split('\n')
    start_index = -1
    for i, line in enumerate(lines):
        if 'Keyword' in line and 'Clicks' in line and 'Impressions' in line:
            start_index = i + 2  # 2 lines for header and separator
            break

    if start_index == -1:
        print("Could not find keyword data in the input.")
        return

    keyword_lines = lines[start_index:]
    
    # It seems the data is fixed-width, which makes parsing tricky.
    # Let's try to parse it based on common separators or by splitting.
    # A robust way is to treat multiple spaces as a delimiter.
    
    data = []
    for line in keyword_lines:
        # Split based on more than 2 spaces, but handle the keyword part carefully
        parts = line.split()
        if len(parts) < 4:
            continue
        
        # Reconstruct the keyword which might contain spaces
        # The last 3 columns are Clicks, Impressions, CTR%, Position
        # But CTR and Position can be tricky. Let's rely on Clicks and Impressions.
        # Let's find the first numeric value from the right, which should be impressions or position
        
        clicks_idx, impr_idx = -1, -1
        
        # Let's assume the last 4 columns are Clicks, Impressions, CTR, Position
        try:
            position = float(parts[-1])
            ctr = parts[-2]
            impressions = int(parts[-3])
            clicks = int(parts[-4])
            keyword = ' '.join(parts[:-4])
            
            data.append([keyword, clicks, impressions])
        except (ValueError, IndexError):
            # The line format is not as expected, skip it
            continue

    if not data:
        print("No keyword data could be parsed.")
        return

    gsc_df = pd.DataFrame(data, columns=['query', 'clicks', 'impressions'])

    # Apply the sanitization function to the query column
    gsc_df['sanitized_query'] = gsc_df['query'].apply(sanitize_query)

    # Aggregate metrics for sanitized queries
    aggregated_df = gsc_df.groupby('sanitized_query').agg({
        'clicks': 'sum',
        'impressions': 'sum',
    }).reset_index().sort_values(by='impressions', ascending=False)

    # Filter out empty or very short queries that are likely just noise
    aggregated_df = aggregated_df[aggregated_df['sanitized_query'].str.strip().str.len() > 3]

    print("Aggregated and Sanitized Keywords:")
    print(aggregated_df.head(20).to_string(index=False))


if __name__ == "__main__":
    # Read from stdin
    input_data = sys.stdin.read()
    process_gsc_data(input_data) 