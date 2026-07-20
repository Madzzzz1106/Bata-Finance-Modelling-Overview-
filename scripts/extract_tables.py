import fitz
import pandas as pd
import os
import re
import json

def clean_value(val):
    if not val:
        return ""
    val = val.strip()
    if val == "-" or val == "—":
        return "0"
    # Remove footnotes/asterisks/hashes but keep parentheses for negative numbers
    val = re.sub(r'[*#^º~]', '', val)
    # Remove spaces
    val = val.replace(" ", "")
    # Check if numeric
    # Format typically: 1,234.56 or (1,234.56)
    is_neg = False
    if val.startswith("(") and val.endswith(")"):
        is_neg = True
        val = val[1:-1]
    
    val = val.replace(",", "")
    try:
        float(val)
        if is_neg:
            return f"-{val}"
        return val
    except ValueError:
        return val

def extract_table_dynamic(pdf_path, page_num, start_y=130, end_y=690):
    doc = fitz.open(pdf_path)
    page = doc[page_num - 1]
    words = page.get_text("words")
    
    # 1. Detect headers to get column bounds
    header_words = [w for w in words if 80 < w[1] < 135]
    
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
            
    # Default fallbacks
    if note_x is None:
        note_x = 280.0
    if y2025_x is None:
        y2025_x = 380.0
    if y2024_x is None:
        y2024_x = 480.0
        
    t1 = note_x - 30.0
    t2 = (note_x + y2025_x) / 2.0
    t3 = (y2025_x + y2024_x) / 2.0
    
    # 2. Extract and group table words
    table_words = [w for w in words if start_y < w[1] < end_y]
    
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
            # Clean values
            clean_2025 = clean_value(val2025)
            clean_2024 = clean_value(val2024)
            rows.append({
                "Particulars": desc,
                "Note": note,
                "2025": clean_2025,
                "2024": clean_2024
            })
            
    df = pd.DataFrame(rows)
    return df

def clean_statements_dataframe(df):
    cleaned_rows = []
    for idx, row in df.iterrows():
        part = row['Particulars'].strip()
        note = row['Note'].strip()
        val_2025 = row['2025'].strip()
        val_2024 = row['2024'].strip()
        
        # If a row has only text in Particulars and nothing else, it's a section header.
        # If it has values, we keep it.
        # We can clean up empty rows or random page numbers.
        if not part and not note and not val_2025 and not val_2024:
            continue
        cleaned_rows.append([part, note, val_2025, val_2024])
        
    return pd.DataFrame(cleaned_rows, columns=["Particulars", "Note", "2025", "2024"])

if __name__ == "__main__":
    pdf_path = "Bata_FY25.pdf"
    
    # Read page map to get the consolidated pages
    with open(os.path.join("extracted", "Bata_FY25_pagemap.json"), "r") as f:
        pagemap = json.load(f)
        
    # Consolidated pages are the second/later index in the page lists
    # Balance Sheet Consolidated page:
    bs_page = pagemap["Balance Sheet"][-1]
    # P&L Consolidated page:
    pnl_page = pagemap["Statement of Profit and Loss"][-1]
    # Cash Flow Consolidated pages (usually 2 pages, the last 2 pages in the list):
    cf_pages = pagemap["Cash Flow Statement"][-2:]
    
    print(f"Consolidated Balance Sheet Page: {bs_page}")
    print(f"Consolidated P&L Page: {pnl_page}")
    print(f"Consolidated Cash Flow Pages: {cf_pages}")
    
    # 1. Balance Sheet
    df_bs = extract_table_dynamic(pdf_path, bs_page, start_y=130, end_y=580)
    df_bs = clean_statements_dataframe(df_bs)
    df_bs.to_csv(os.path.join("extracted", "Bata_FY25_balance_sheet.csv"), index=False)
    
    # 2. P&L
    df_pnl = extract_table_dynamic(pdf_path, pnl_page, start_y=130, end_y=560)
    df_pnl = clean_statements_dataframe(df_pnl)
    df_pnl.to_csv(os.path.join("extracted", "Bata_FY25_pnl.csv"), index=False)
    
    # 3. Cash Flow
    # Extract each page and concatenate
    cf_list = []
    for p in cf_pages:
        df_p = extract_table_dynamic(pdf_path, p, start_y=130, end_y=690)
        cf_list.append(df_p)
    df_cf = pd.concat(cf_list, ignore_index=True)
    df_cf = clean_statements_dataframe(df_cf)
    df_cf.to_csv(os.path.join("extracted", "Bata_FY25_cashflow.csv"), index=False)
    
    print("Stage 3 completed: CSVs saved to extracted/")
