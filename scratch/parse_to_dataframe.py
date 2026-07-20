import fitz
import re
import pandas as pd

def parse_financial_page(pdf_path, page_num):
    doc = fitz.open(pdf_path)
    page = doc[page_num - 1]
    blocks = page.get_text("blocks")
    # Sort blocks by y0 (top to bottom), then x0 (left to right)
    blocks.sort(key=lambda b: (b[1], b[0]))
    
    all_lines = []
    for b in blocks:
        # Ignore footer/header blocks
        x0, y0, x1, y1, text, block_no, block_type = b
        if y0 < 80 or y0 > 690:
            continue
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        all_lines.extend(lines)
        
    print(f"--- Raw lines on page {page_num} ---")
    for i, line in enumerate(all_lines):
        print(f"{i}: {line}")
        
if __name__ == "__main__":
    parse_financial_page("Bata_FY25.pdf", 221)
    parse_financial_page("Bata_FY25.pdf", 222)
