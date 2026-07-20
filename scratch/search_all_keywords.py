import fitz

def search_pdf_details(pdf_path):
    print(f"\n===== SEARCHING {pdf_path} =====")
    doc = fitz.open(pdf_path)
    for p in range(len(doc)):
        text = doc[p].get_text("text").lower()
        # Clean text
        clean = " ".join(text.split())
        
        # Check for Cash Flow
        if "cash flow" in clean or "cash flows" in clean:
            if "operating activities" in clean and any(term in clean for term in ["standalone", "consolidated"]):
                print(f"Page {p+1}: contains 'Cash Flow' + 'operating activities' ({'standalone' if 'standalone' in clean else ''} {'consolidated' if 'consolidated' in clean else ''})")
                
        # Check for Balance Sheet
        if "balance sheet" in clean and "assets" in clean and "equity" in clean:
            print(f"Page {p+1}: contains 'Balance Sheet' ({'standalone' if 'standalone' in clean else ''} {'consolidated' if 'consolidated' in clean else ''})")
            
        # Check for P&L
        if any(term in clean for term in ["profit and loss", "profit & loss"]):
            if "revenue" in clean and "operations" in clean:
                print(f"Page {p+1}: contains 'Profit & Loss' ({'standalone' if 'standalone' in clean else ''} {'consolidated' if 'consolidated' in clean else ''})")

if __name__ == "__main__":
    search_pdf_details("Bata_FY21.pdf")
    search_pdf_details("Bata_FY22.pdf")
    search_pdf_details("Metro_FY21.pdf")
