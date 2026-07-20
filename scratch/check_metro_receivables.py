import pandas as pd
df = pd.read_csv("extracted/Metro_FY24_balance_sheet.csv")
print("=== Metro FY24 BS Trade Receivables Rows ===")
print(df[df["Particulars"].str.contains("receivables", case=False, na=False)])
