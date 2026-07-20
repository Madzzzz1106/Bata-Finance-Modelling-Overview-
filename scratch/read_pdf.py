import fitz  # PyMuPDF
import sys

def read_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    print(f"Total pages: {len(doc)}")
    for i, page in enumerate(doc):
        print(f"\n--- PAGE {i+1} ---")
        text = page.get_text()
        print(text)

if __name__ == "__main__":
    pdf_path = "BataCompleteOverview.pdf"
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    read_pdf(pdf_path)
