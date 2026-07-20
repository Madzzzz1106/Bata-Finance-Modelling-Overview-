import pdfplumber
import pandas as pd

with pdfplumber.open("Bata_FY25.pdf") as pdf:
    page = pdf.pages[220] # page 221
    # Try different table settings
    settings = {
        "vertical_strategy": "text",
        "horizontal_strategy": "text",
    }
    tables = page.extract_tables(settings)
    print("Found tables:", len(tables))
    for idx, t in enumerate(tables):
        print(f"Table {idx+1}:")
        df = pd.DataFrame(t)
        print(df.to_string())
