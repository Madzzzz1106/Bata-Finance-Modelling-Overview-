import fitz
import pandas as pd
import os
import json
import re

# Precise page mappings for all 15 files
PDF_MAPPINGS = {
    "Bata_FY21.pdf": {
        "type": "consolidated",
        "BS": [199],
        "P&L": [200],
        "CF": [202, 203],
        "RP": [234, 235, 236, 237],
        "CL": [231],
        "MDA": list(range(66, 75)),
        "Audit": list(range(189, 195))
    },
    "Bata_FY22.pdf": {
        "type": "consolidated",
        "BS": [181],
        "P&L": [182],
        "CF": [184, 185],
        "RP": [217, 218, 219, 220],
        "CL": [214],
        "MDA": list(range(59, 67)),
        "Audit": list(range(171, 181))
    },
    "Bata_FY23.pdf": {
        "type": "consolidated",
        "BS": [210],
        "P&L": [211],
        "CF": [213, 214],
        "RP": [248, 249, 250, 251, 252, 253],
        "CL": [247],
        "MDA": list(range(55, 63)),
        "Audit": list(range(197, 210))
    },
    "Bata_FY24.pdf": {
        "type": "consolidated",
        "BS": [232],
        "P&L": [233],
        "CF": [235, 236],
        "RP": [274, 275, 276, 277, 278, 279],
        "CL": [273],
        "MDA": list(range(56, 64)),
        "Audit": list(range(214, 232))
    },
    "Bata_FY25.pdf": {
        "type": "consolidated",
        "BS": [221],
        "P&L": [222],
        "CF": [224, 225],
        "RP": [263, 264, 265, 266, 267, 268],
        "CL": [262],
        "MDA": list(range(47, 55)),
        "Audit": list(range(210, 221))
    },
    "Relaxo_FY21.pdf": {
        "type": "standalone",
        "BS": [76],
        "P&L": [77],
        "CF": [78, 79],
        "RP": [116],
        "CL": [106],
        "MDA": list(range(14, 19)),
        "Audit": list(range(68, 76))
    },
    "Relaxo_FY22.pdf": {
        "type": "standalone",
        "BS": [80],
        "P&L": [81],
        "CF": [82, 83],
        "RP": [119],
        "CL": [110],
        "MDA": list(range(14, 19)),
        "Audit": list(range(72, 80))
    },
    "Relaxo_FY23.pdf": {
        "type": "standalone",
        "BS": [98],
        "P&L": [99],
        "CF": [100, 101],
        "RP": [138],
        "CL": [128],
        "MDA": list(range(14, 19)),
        "Audit": list(range(90, 98))
    },
    "Relaxo_FY24.pdf": {
        "type": "standalone",
        "BS": [112],
        "P&L": [113],
        "CF": [114, 115],
        "RP": [153],
        "CL": [143],
        "MDA": list(range(14, 20)),
        "Audit": list(range(104, 112))
    },
    "Relaxo_FY25.pdf": {
        "type": "standalone",
        "BS": [106],
        "P&L": [107],
        "CF": [108, 109],
        "RP": [149],
        "CL": [138],
        "MDA": list(range(13, 19)),
        "Audit": list(range(113, 121))
    },
    "Metro_FY21.pdf": {
        "type": "consolidated",
        "BS": [99],
        "P&L": [100],
        "CF": [101],
        "RP": [128, 129, 130, 131, 132],
        "CL": [122, 123],
        "MDA": [29, 30, 31],
        "Audit": list(range(93, 99))
    },
    "Metro_FY22.pdf": {
        "type": "consolidated",
        "BS": [204],
        "P&L": [205],
        "CF": [206],
        "RP": [250, 251, 261, 262],
        "CL": [241],
        "MDA": [41, 42, 43, 44, 45, 46],
        "Audit": list(range(197, 204))
    },
    "Metro_FY23.pdf": {
        "type": "consolidated",
        "BS": [226],
        "P&L": [227],
        "CF": [228],
        "RP": [274, 275, 286],
        "CL": [266],
        "MDA": [51, 52, 53, 54, 55],
        "Audit": list(range(219, 226))
    },
    "Metro_FY24.pdf": {
        "type": "consolidated",
        "BS": [109],
        "P&L": [109],
        "CF": [110],
        "RP": [130, 131, 136],
        "CL": [127],
        "MDA": [26, 27, 28, 29, 30],
        "Audit": list(range(101, 109))
    },
    "Metro_FY25.pdf": {
        "type": "consolidated",
        "BS": [117],
        "P&L": [117],
        "CF": [118],
        "RP": [141, 144, 147],
        "CL": [137],
        "MDA": [26, 27, 28],
        "Audit": list(range(109, 117))
    }
}

def clean_value(val):
    if not val:
        return ""
    val = val.strip()
    if val == "-" or val == "—":
        return "0"
    val = re.sub(r'[*#^º~]', '', val)
    val = val.replace(" ", "")
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

def extract_table_dynamic(pdf_path, page_num, start_y=120, end_y=690, x_min=0, x_max=1500, company_name=""):
    doc = fitz.open(pdf_path)
    page = doc[page_num - 1]
    words = page.get_text("words")
    
    # Filter words to active coordinates
    words = [w for w in words if x_min <= w[0] <= x_max]
    
    # 1. Detect headers to get column bounds
    header_words = [w for w in words if 80 < w[1] < 140]
    
    note_x = None
    y_curr_x = None
    y_prev_x = None
    
    year_words = ["2025", "2024", "2023", "2022", "2021", "2020"]
    
    for w in header_words:
        word_text = w[4].lower().strip().replace(".", "").replace(",", "")
        cx = (w[0] + w[2]) / 2.0
        if "note" in word_text:
            note_x = cx
        elif any(yr in word_text for yr in year_words) and cx > x_min + 350.0:
            if y_curr_x is None:
                y_curr_x = cx
            else:
                y_prev_x = cx
                
    if y_curr_x is not None and y_prev_x is not None and y_curr_x > y_prev_x:
        y_curr_x, y_prev_x = y_prev_x, y_curr_x
        
    # Company-specific column coordinate fallbacks
    comp_lower = company_name.lower()
    if comp_lower == "metro":
        # Metro portrait pages have headers shifted right
        fallback_note = x_min + 390.0 if x_min == 0 else x_min + 360.0
        fallback_curr = x_min + 460.0 if x_min == 0 else x_min + 440.0
        fallback_prev = x_min + 530.0 if x_min == 0 else x_min + 520.0
    else:
        fallback_note = x_min + 280.0
        fallback_curr = x_min + 380.0
        fallback_prev = x_min + 480.0
        
    if note_x is None:
        note_x = fallback_note
    if y_curr_x is None:
        y_curr_x = fallback_curr
    if y_prev_x is None:
        y_prev_x = fallback_prev
        
    # Thresholds
    t1 = note_x - 30.0
    t2 = (note_x + y_curr_x) / 2.0
    t3 = (y_curr_x + y_prev_x) / 2.0
    
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
        val_curr = " ".join(col2_words).strip()
        val_prev = " ".join(col3_words).strip()
        
        if desc or note or val_curr or val_prev:
            rows.append({
                "Particulars": desc,
                "Note": note,
                "CurrentYear": clean_value(val_curr),
                "PreviousYear": clean_value(val_prev)
            })
            
    df = pd.DataFrame(rows)
    return df

def clean_and_save_csv(df, output_path):
    df = df[df["Particulars"].str.strip() != ""]
    df.to_csv(output_path, index=False)
    return len(df)

def extract_qualitative_text(pdf_path, pages, output_txt_path):
    if not pages:
        return
    doc = fitz.open(pdf_path)
    text_content = []
    for p in pages:
        if p <= len(doc):
            page = doc[p - 1]
            text_content.append(f"--- Page {p} ---")
            text_content.append(page.get_text("text"))
    with open(output_txt_path, "w") as f:
        f.write("\n\n".join(text_content))

def process_all_files():
    summary_report = []
    
    for filename, mappings in PDF_MAPPINGS.items():
        if not os.path.exists(filename):
            print(f"Warning: {filename} not found in root. Skipping.")
            continue
            
        print(f"\nProcessing {filename}...")
        base_name = filename.replace(".pdf", "")
        
        bs_path = os.path.join("extracted", f"{base_name}_balance_sheet.csv")
        pnl_path = os.path.join("extracted", f"{base_name}_pnl.csv")
        cf_path = os.path.join("extracted", f"{base_name}_cashflow.csv")
        
        # 1. Balance Sheet & P&L
        bs_page = mappings["BS"][0]
        
        # Check if BS and P&L are on the same page (Metro FY24, FY25 side-by-side landscape format)
        if len(mappings["P&L"]) > 0 and bs_page == mappings["P&L"][0]:
            print(f"  BS and P&L are on the same page ({bs_page}) for {filename}. Splitting vertically at center.")
            # Metro FY24 and FY25 page width is 1143.8. Split at x=572.
            df_bs = extract_table_dynamic(filename, bs_page, start_y=80, end_y=680, x_min=0, x_max=572, company_name="Metro")
            df_pnl = extract_table_dynamic(filename, bs_page, start_y=80, end_y=680, x_min=572, x_max=1200, company_name="Metro")
        else:
            df_bs = extract_table_dynamic(filename, bs_page, start_y=120, end_y=680, company_name=base_name.split("_")[0])
            pnl_page = mappings["P&L"][0]
            df_pnl = extract_table_dynamic(filename, pnl_page, start_y=120, end_y=680, company_name=base_name.split("_")[0])
            
        # 2. Cash Flow
        cf_dfs = []
        for p in mappings["CF"]:
            cf_dfs.append(extract_table_dynamic(filename, p, start_y=120, end_y=690, company_name=base_name.split("_")[0]))
        if cf_dfs:
            df_cf = pd.concat(cf_dfs, ignore_index=True)
        else:
            df_cf = pd.DataFrame(columns=["Particulars", "Note", "CurrentYear", "PreviousYear"])
            
        # Clean and save CSVs
        bs_rows = clean_and_save_csv(df_bs, bs_path)
        pnl_rows = clean_and_save_csv(df_pnl, pnl_path)
        cf_rows = clean_and_save_csv(df_cf, cf_path)
        
        # 3. Qualitative text extraction
        extract_qualitative_text(filename, mappings["MDA"], os.path.join("extracted", f"{base_name}_mda.txt"))
        extract_qualitative_text(filename, mappings["RP"], os.path.join("extracted", f"{base_name}_related_party.txt"))
        extract_qualitative_text(filename, mappings["CL"], os.path.join("extracted", f"{base_name}_contingent_liabilities.txt"))
        extract_qualitative_text(filename, mappings["Audit"], os.path.join("extracted", f"{base_name}_auditor_report.txt"))
        
        # Record row counts for reporting
        summary_report.append({
            "File": filename,
            "Type": mappings["type"],
            "BS_Rows": bs_rows,
            "PNL_Rows": pnl_rows,
            "CF_Rows": cf_rows
        })
        
        if bs_rows < 5 or pnl_rows < 5:
            print(f"WARNING: Low row count warning for {filename}! BS={bs_rows}, PNL={pnl_rows}")
            
    print("\nSummary Report:")
    print(pd.DataFrame(summary_report).to_string(index=False))

if __name__ == "__main__":
    process_all_files()
