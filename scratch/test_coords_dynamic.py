import fitz
import pandas as pd
import numpy as np

def extract_table_dynamic(pdf_path, page_num):
    doc = fitz.open(pdf_path)
    page = doc[page_num - 1]
    words = page.get_text("words")
    
    # 1. Detect headers to get column bounds
    # Search for words in the top section (y between 80 and 150)
    header_words = [w for w in words if 80 < w[1] < 135]
    
    # Let's find:
    # - "Notes" or "Note"
    # - "2025"
    # - "2024" (or other years like 2023, 2022, 2021)
    
    note_x = None
    y2025_x = None
    y2024_x = None
    
    for w in header_words:
        word_text = w[4].lower().strip().replace(".", "").replace(",", "")
        cx = (w[0] + w[2]) / 2
        if "note" in word_text:
            note_x = cx
        elif "2025" in word_text:
            y2025_x = cx
        elif "2024" in word_text:
            y2024_x = cx
            
    # Default fallbacks if not found
    if note_x is None:
        note_x = 280.0
    if y2025_x is None:
        y2025_x = 380.0
    if y2024_x is None:
        y2024_x = 480.0
        
    print(f"Page {page_num} Detected centers: Note={note_x:.1f}, 2025={y2025_x:.1f}, 2024={y2024_x:.1f}")
    
    # Let's define the thresholds as the mid-points between the column centers
    # Threshold 1: between Description and Note
    # Note is typically around note_x. Description is to its left.
    # Let's set the boundary at note_x - 30
    t1 = note_x - 30.0
    # Threshold 2: between Note and 2025
    t2 = (note_x + y2025_x) / 2.0
    # Threshold 3: between 2025 and 2024
    t3 = (y2025_x + y2024_x) / 2.0
    
    # 2. Extract and group table words
    table_words = [w for w in words if 130 < w[1] < 570] # limit to table content area
    
    # Group by y coordinate with tolerance
    table_words.sort(key=lambda w: w[1])
    lines = []
    current_line = []
    current_y = None
    y_tolerance = 4.0
    
    for w in table_words:
        x0, y0, x1, y1, word, _, _, _ = w
        if current_y is None:
            current_y = y0
            current_line.append(w)
        elif abs(y0 - current_y) <= y_tolerance:
            current_line.append(w)
        else:
            current_line.sort(key=lambda wl: wl[0])
            lines.append(current_line)
            current_line = [w]
            current_y = y0
            
    if current_line:
        current_line.sort(key=lambda wl: wl[0])
        lines.append(current_line)
        
    # Group words in each line into columns
    rows = []
    for line in lines:
        col0_words = []
        col1_words = []
        col2_words = []
        col3_words = []
        
        for w in line:
            x0, y0, x1, y1, word, _, _, _ = w
            cx = (x0 + x1) / 2.0
            
            if cx < t1:
                col0_words.append(word)
            elif cx < t2:
                col1_words.append(word)
            elif cx < t3:
                col2_words.append(word)
            else:
                col3_words.append(word)
                
        desc = " ".join(col0_words).strip()
        note = " ".join(col1_words).strip()
        val2025 = " ".join(col2_words).strip()
        val2024 = " ".join(col3_words).strip()
        
        if desc or note or val2025 or val2024:
            rows.append({
                "Particulars": desc,
                "Note": note,
                "2025": val2025,
                "2024": val2024
            })
            
    df = pd.DataFrame(rows)
    return df

if __name__ == "__main__":
    df221 = extract_table_dynamic("Bata_FY25.pdf", 221)
    print("\n--- Page 221 Balance Sheet ---")
    print(df221.to_string())
    
    df222 = extract_table_dynamic("Bata_FY25.pdf", 222)
    print("\n--- Page 222 Profit & Loss ---")
    print(df222.to_string())
