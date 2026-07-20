import fitz
import pandas as pd

def extract_table_by_coords(pdf_path, page_num):
    doc = fitz.open(pdf_path)
    page = doc[page_num - 1]
    words = page.get_text("words")  # list of (x0, y0, x1, y1, "word", block_no, line_no, word_no)
    
    # Filter words to the main table area (y-coordinate between 80 and 690)
    words = [w for w in words if w[1] > 80 and w[3] < 690]
    
    # Group words into lines based on y-coordinate
    # We will sort words by y0 first
    words.sort(key=lambda w: w[1])
    
    lines = []
    current_line = []
    current_y = None
    y_tolerance = 3  # pixels
    
    for w in words:
        x0, y0, x1, y1, word, block_no, line_no, word_no = w
        if current_y is None:
            current_y = y0
            current_line.append(w)
        elif abs(y0 - current_y) <= y_tolerance:
            current_line.append(w)
        else:
            # Sort current line by x0 (left to right)
            current_line.sort(key=lambda wl: wl[0])
            lines.append(current_line)
            current_line = [w]
            current_y = y0
            
    if current_line:
        current_line.sort(key=lambda wl: wl[0])
        lines.append(current_line)
        
    # Now for each line, group words into columns based on x-coordinates
    # Let's see what the typical column boundaries are.
    # Col 0 (Metric): x < 260
    # Col 1 (Note): 260 <= x < 310
    # Col 2 (2025): 310 <= x < 420
    # Col 3 (2024): 420 <= x < 550
    
    rows = []
    for line in lines:
        col0_words = []
        col1_words = []
        col2_words = []
        col3_words = []
        
        for w in line:
            x0, y0, x1, y1, word, _, _, _ = w
            # Use mid-point of the word to assign to column
            cx = (x0 + x1) / 2
            if cx < 260:
                col0_words.append(word)
            elif cx < 310:
                col1_words.append(word)
            elif cx < 420:
                col2_words.append(word)
            else:
                col3_words.append(word)
                
        desc = " ".join(col0_words).strip()
        note = " ".join(col1_words).strip()
        val2025 = " ".join(col2_words).strip()
        val2024 = " ".join(col3_words).strip()
        
        # Only add if it's not a completely empty line
        if desc or note or val2025 or val2024:
            rows.append({
                "y": line[0][1],
                "Particulars": desc,
                "Note": note,
                "2025": val2025,
                "2024": val2024
            })
            
    df = pd.DataFrame(rows)
    return df

if __name__ == "__main__":
    df221 = extract_table_by_coords("Bata_FY25.pdf", 221)
    print("--- Page 221 (Balance Sheet) ---")
    print(df221.to_string())
    
    df222 = extract_table_by_coords("Bata_FY25.pdf", 222)
    print("\n--- Page 222 (Profit & Loss) ---")
    print(df222.to_string())
