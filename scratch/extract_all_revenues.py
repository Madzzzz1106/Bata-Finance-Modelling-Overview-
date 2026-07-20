import pandas as pd

df = pd.read_csv("extracted/master_financials.csv")
pnl = df[(df["Statement"] == "pnl") & (df["Metric"].str.contains("revenue from operations|sales|revenue from Operations", case=False, na=False))]

print("=== ALL COMPANIES FY25 SALES ===")
fy25_sales = pnl[pnl["FinancialYear"] == "FY25"]
print(fy25_sales[["Company", "Value"]])
