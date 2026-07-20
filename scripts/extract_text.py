import fitz
import json
import os

def extract_section_text(pdf_path, pages, output_txt_path):
    if not pages:
        print(f"No pages mapped for {output_txt_path}. Skipping.")
        return
    
    doc = fitz.open(pdf_path)
    text_content = []
    
    for p in pages:
        page = doc[p - 1]
        text_content.append(f"--- Page {p} ---")
        text_content.append(page.get_text("text"))
        
    with open(output_txt_path, "w") as f:
        f.write("\n\n".join(text_content))
    print(f"Saved qualitative text to {output_txt_path}")

if __name__ == "__main__":
    pdf_path = "Bata_FY25.pdf"
    
    with open(os.path.join("extracted", "Bata_FY25_pagemap.json"), "r") as f:
        pagemap = json.load(f)
        
    # 1. MD&A
    mda_pages = pagemap["MD&A"]
    extract_section_text(pdf_path, mda_pages, os.path.join("extracted", "Bata_FY25_mda.txt"))
    
    # 2. Related Party
    rp_pages = pagemap["Notes to Accounts (Related Party)"]
    # Standalone is the first half (6 pages), Consolidated is the second half (6 pages)
    if len(rp_pages) >= 12:
        rp_standalone = rp_pages[:6]
        rp_consolidated = rp_pages[6:]
    elif len(rp_pages) >= 6:
        rp_standalone = rp_pages[:6]
        rp_consolidated = rp_pages[:6] # fallback
    else:
        rp_standalone = rp_pages
        rp_consolidated = rp_pages
        
    extract_section_text(pdf_path, rp_consolidated, os.path.join("extracted", "Bata_FY25_related_party.txt"))
    extract_section_text(pdf_path, rp_standalone, os.path.join("extracted", "Bata_FY25_related_party_standalone.txt"))
    
    # 3. Contingent Liabilities
    cl_pages = pagemap["Notes to Accounts (Contingent Liabilities)"]
    if len(cl_pages) >= 2:
        cl_standalone = [cl_pages[0]]
        cl_consolidated = [cl_pages[1]]
    else:
        cl_standalone = cl_pages
        cl_consolidated = cl_pages
        
    extract_section_text(pdf_path, cl_consolidated, os.path.join("extracted", "Bata_FY25_contingent_liabilities.txt"))
    extract_section_text(pdf_path, cl_standalone, os.path.join("extracted", "Bata_FY25_contingent_liabilities_standalone.txt"))
    
    # 4. Auditor's Report
    # Standalone Auditor's report: pages 133 to 150
    audit_standalone_pages = pagemap["Auditor's Report"]
    
    # Consolidated Auditor's report: pages 210 to 220
    audit_consolidated_pages = list(range(210, 221))
    
    extract_section_text(pdf_path, audit_consolidated_pages, os.path.join("extracted", "Bata_FY25_auditor_report.txt"))
    extract_section_text(pdf_path, audit_standalone_pages, os.path.join("extracted", "Bata_FY25_auditor_report_standalone.txt"))
    
    print("Stage 4 completed: qualitative texts saved to extracted/")
