import pandas as pd

df = pd.read_csv("extracted/master_financials.csv")
pnl = df[(df["Statement"] == "pnl") & (df["Metric"].str.contains("revenue from operations|sales|revenue from Operations", case=False, na=False))]

print("=== BATA HISTORICAL SALES ===")
bata_sales = pnl[pnl["Company"] == "Bata"].sort_values("FinancialYear")
print(bata_sales[["FinancialYear", "Value"]])

print("\n=== METRO HISTORICAL SALES ===")
metro_sales = pnl[pnl["Company"] == "Metro"].sort_values("FinancialYear")
print(metro_sales[["FinancialYear", "Value"]])
