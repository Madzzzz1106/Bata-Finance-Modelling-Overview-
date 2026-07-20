import fitz

def get_other_operating_expenses(pdf_path, year_label):
    doc = fitz.open(pdf_path)
    for p in range(len(doc)):
        text = doc[p].get_text("text")
        lines = text.split('\n')
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(term in line_lower for term in ["sales commission", "royalty", "franchise commission"]):
                print(f"[{year_label}] Page {p+1} ({line.strip()}):")
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
            get_other_operating_expenses("/Users/mridulagarwal/Desktop/BATA/" + pdf_name, year)
        except Exception as e:
            print(f"Error reading {pdf_name}: {e}")
