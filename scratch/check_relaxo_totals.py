import glob
import pandas as pd

files = glob.glob("extracted/Relaxo_*_balance_sheet.csv")
for f in sorted(files):
    df = pd.read_csv(f)
    print(f"File: {f}")
    print("  Contains 'Total current assets':", df["Particulars"].str.contains("Total current assets", case=False, na=False).any())
    print("  Contains 'Total current liabilities':", df["Particulars"].str.contains("Total current liabilities", case=False, na=False).any())
