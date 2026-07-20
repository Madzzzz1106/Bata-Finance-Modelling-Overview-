import fitz
import json
import os
import re

def refine_mapping(pdf_path):
    doc = fitz.open(pdf_path)
    num_pages = len(doc)
    
    sections = {
        "Balance Sheet": [],
        "Statement of Profit and Loss": [],
        "Cash Flow Statement": [],
        "Notes to Accounts (Related Party)": [],
        "Notes to Accounts (Contingent Liabilities)": [],
        "MD&A": [],
        "Auditor's Report": []
    }
    
    # Let's search each page and extract text to locate key markers
    for p in range(num_pages):
        page_num = p + 1
        text = doc[p].get_text("text")
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        full_text_clean = " ".join(lines)
        full_text_lower = full_text_clean.lower()
        
        # 1. Auditor's Report (Standalone starts around 133, Consolidated around 210)
        # Standalone starts on page 133, goes up to 150 (page 151 starts Balance Sheet)
        if "to the members of bata india limited" in full_text_lower and "report on the audit of the standalone financial" in full_text_lower:
            sections["Auditor's Report"] = list(range(page_num, page_num + 18))  # 133 to 150 inclusive
            
        # 2. Balance Sheet
        # Standalone is page 151, Consolidated is page 221
        if "balance sheet" in full_text_lower and "as at 31 march 2025" in full_text_lower:
            if "non-current assets" in full_text_lower and "property, plant and equipment" in full_text_lower:
                sections["Balance Sheet"].append(page_num)
                
        # 3. Statement of Profit and Loss
        # Standalone is page 152, Consolidated is page 222
        if any(term in full_text_lower for term in ["statement of profit and loss", "profit and loss statement"]) and "revenue from operations" in full_text_lower:
            if "for the year ended" in full_text_lower and "31 march 2025" in full_text_lower:
                sections["Statement of Profit and Loss"].append(page_num)
                
        # 4. Cash Flow Statement
        # Standalone is pages 154-155, Consolidated is pages 224-225
        if any(term in full_text_lower for term in ["cash flow statement", "statement of cash flows"]) and "cash flows from operating activities" in full_text_lower:
            sections["Cash Flow Statement"].append(page_num)
            # Cash Flow is usually 2 pages
            if page_num + 1 <= num_pages:
                sections["Cash Flow Statement"].append(page_num + 1)
                
        # 5. MD&A
        # Pages 47 to 54
        if "management discussion and analysis" in full_text_lower and "industry structure and developments" in full_text_lower:
            sections["MD&A"] = list(range(page_num, page_num + 8)) # 47 to 54
            
        # 6. Related Party Note
        # Standalone is pages 195-200
        if "related party disclosures" in full_text_lower and "names of related parties" in full_text_lower:
            sections["Notes to Accounts (Related Party)"].extend(list(range(page_num, page_num + 6)))
            
        # 7. Contingent Liabilities Note
        # Standalone is page 193
        if "contingent liabilities and commitments" in full_text_lower and "excise, customs and service tax" in full_text_lower:
            sections["Notes to Accounts (Contingent Liabilities)"].append(page_num)

    # De-duplicate lists and ensure correct data types
    for k in sections:
        sections[k] = sorted(list(set(sections[k])))
        
    return sections

if __name__ == "__main__":
    pdf_file = "Bata_FY25.pdf"
    mapping = refine_mapping(pdf_file)
    print("Refined Mapping Results for Bata_FY25.pdf:")
    for section, pages in mapping.items():
        print(f"{section}: {pages}")
        
    output_path = os.path.join("extracted", "Bata_FY25_pagemap.json")
    with open(output_path, "w") as f:
        json.dump(mapping, f, indent=4)
    print(f"Saved refined mapping to {output_path}")
