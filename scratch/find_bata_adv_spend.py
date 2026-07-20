import fitz
import re

def search_marketing_expenses(pdf_path, year_label):
    print(f"\n==================== SEARCHING {pdf_path} ({year_label}) ====================")
    doc = fitz.open(pdf_path)
    
    # We will search for pages containing "other expenses" or "advertising" or "promotion"
    for page_num in range(len(doc)):
        text = doc[page_num].get_text("text")
        text_lower = text.lower()
        
        # Check if the page is likely the "Other expenses" note page
        # Usually it has "other expenses" and items like "rent", "rates and taxes", "insurance", "advertising" or "marketing" or "publicity"
        if ("other expenses" in text_lower or "note 25" in text_lower or "note 26" in text_lower) and \
           any(term in text_lower for term in ["advertising", "publicity", "promotion", "advertisement", "business promotion"]):
            print(f"--- Found potential page: {page_num + 1} ---")
            lines = text.split('\n')
            for line in lines:
                line_clean = line.strip()
                # If the line contains words like advertising, promotion, marketing, publicity, or other expenses
                if any(term in line_clean.lower() for term in ["advertis", "publicity", "promotion", "marketing", "rent", "insurance", "brokerage", "commission"]):
                    print("  ", line_clean)
            
            # Print a snippet around where these keywords appear
            print("\nPage text snippet:")
            # print first 1000 characters
            print(text[:2000])
            print("--------------------------------------------------")

if __name__ == "__main__":
    import sys
    pdfs = [
        ("Bata_FY25.pdf", "FY25"),
        ("Bata_FY24.pdf", "FY24"),
        ("Bata_FY23.pdf", "FY23"),
        ("Bata_FY22.pdf", "FY22"),
        ("Bata_FY21.pdf", "FY21")
    ]
    for pdf_name, year in pdfs:
        try:
            search_marketing_expenses("/Users/mridulagarwal/Desktop/BATA/" + pdf_name, year)
        except Exception as e:
            print(f"Error reading {pdf_name}: {e}")
