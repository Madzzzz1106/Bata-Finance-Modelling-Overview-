import fitz
import re

def get_adv_spend(pdf_path, year_label):
    doc = fitz.open(pdf_path)
    for p in range(len(doc)):
        text = doc[p].get_text("text")
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if "advertising and sales promotion" in line.lower() or "advertising & sales promotion" in line.lower():
                print(f"[{year_label}] Page {p+1}:")
                # Print the line and the next 15 lines to capture the numbers associated with it
                start = max(0, i - 2)
                end = min(len(lines), i + 8)
                for j in range(start, end):
                    print(f"  Line {j}: {lines[j].strip()}")
                print("-" * 40)

if __name__ == "__main__":
    pdfs = [
        ("Bata_FY25.pdf", "FY25"),
        ("Bata_FY24.pdf", "FY24"),
        ("Bata_FY23.pdf", "FY23"),
        ("Bata_FY22.pdf", "FY22"),
        ("Bata_FY21.pdf", "FY21")
    ]
    for pdf_name, year in pdfs:
        try:
            get_adv_spend("/Users/mridulagarwal/Desktop/BATA/" + pdf_name, year)
        except Exception as e:
            print(f"Error reading {pdf_name}: {e}")
