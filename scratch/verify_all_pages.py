import fitz
import glob
import json
import os

def find_exact_pages(pdf_path):
    doc = fitz.open(pdf_path)
    num_pages = len(doc)
    
    bs_pages = []
    pnl_pages = []
    cf_pages = []
    
    for p in range(num_pages):
        text = doc[p].get_text("text").lower()
        clean = " ".join(text.split())
        
        # Balance Sheet
        if "balance sheet" in clean and any(term in clean for term in ["as at 31 march", "as at march 31", "as at 31st march"]):
            if any(term in clean for term in ["assets", "equity and liabilities", "particulars", "non-current assets"]):
                bs_pages.append(p + 1)
                
        # Profit and Loss
        if any(term in clean for term in ["statement of profit and loss", "profit and loss statement", "profit & loss statement", "statement of profit & loss"]) and any(term in clean for term in ["revenue from operations", "income", "expenses", "revenue"]):
            pnl_pages.append(p + 1)
            
        # Cash Flow
        if any(term in clean for term in ["cash flow statement", "statement of cash flows", "statement of cash flow", "cash flows statement"]) and any(term in clean for term in ["operating activities", "operating activity"]):
            cf_pages.append(p + 1)
            
    # Filter/clean false positives
    # Usually:
    # Bata has Standalone and Consolidated, so we want both.
    # Relaxo has Standalone only, so we want Standalone.
    # Metro has Standalone and Consolidated, so we want both.
    
    return {
        "BS": bs_pages,
        "P&L": pnl_pages,
        "CF": cf_pages
    }

if __name__ == "__main__":
    files = sorted(glob.glob("*.pdf"))
    all_mappings = {}
    for f in files:
        mapping = find_exact_pages(f)
        all_mappings[f] = mapping
        print(f"'{f}': {mapping},")
