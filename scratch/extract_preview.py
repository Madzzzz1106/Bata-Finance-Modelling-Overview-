import pdfplumber
import pandas as pd

def extract_page_tables(pdf_path, page_num):
    print(f"--- Extracting Page {page_num} ---")
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num - 1]
        tables = page.extract_tables()
        for idx, table in enumerate(tables):
            print(f"Table {idx+1}:")
            df = pd.DataFrame(table)
            print(df.to_string())
            print("\n")

if __name__ == "__main__":
    extract_page_tables("Bata_FY25.pdf", 221)
    extract_page_tables("Bata_FY25.pdf", 222)
