import fitz
import glob

def search_metro_pdf(pdf_path):
    print(f"\n===== SEARCHING {pdf_path} =====")
    doc = fitz.open(pdf_path)
    for p in range(len(doc)):
        text = doc[p].get_text("text").lower()
        clean = " ".join(text.split())
        
        # Cash Flow
        if "operating activities" in clean and ("cash flow" in clean or "cash flows" in clean or "cashﬂow" in clean or "cash ﬂow" in clean):
            print(f"  Page {p+1}: Cash Flow ({'standalone' if 'standalone' in clean else ''} {'consolidated' if 'consolidated' in clean else ''})")
            
        # Related Party
        if "related party disclosures" in clean or "related party transactions" in clean or "names of related parties" in clean or ("related party" in clean and "disclosure" in clean and "key management" in clean):
            print(f"  Page {p+1}: Related Party ({'standalone' if 'standalone' in clean else ''} {'consolidated' if 'consolidated' in clean else ''})")
            
        # Contingent Liabilities
        if "contingent liabilities" in clean and any(m in clean for m in ["commitments", "contingent liabilities and commitments", "claims against"]):
            print(f"  Page {p+1}: Contingent Liabilities ({'standalone' if 'standalone' in clean else ''} {'consolidated' if 'consolidated' in clean else ''})")
            
        # MD&A
        if "management discussion" in clean or ("discussion" in clean and "outlook" in clean and "industry structure" in clean):
            print(f"  Page {p+1}: MD&A ({'standalone' if 'standalone' in clean else ''} {'consolidated' if 'consolidated' in clean else ''})")

if __name__ == "__main__":
    for f in sorted(glob.glob("Metro_*.pdf")):
        search_metro_pdf(f)
