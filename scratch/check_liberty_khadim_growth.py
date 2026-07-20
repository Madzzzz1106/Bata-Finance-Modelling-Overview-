import pandas as pd

df = pd.read_csv("extracted/master_financials.csv")
target = ["Liberty Shoes", "Khadim India"]
sales_df = df[(df["Company"].isin(target)) & (df["Statement"] == "pnl") & (df["Metric"].str.contains("sales|revenue from operations", case=False, na=False))]

pivoted = sales_df.pivot_table(index="Company", columns="FinancialYear", values="Value", aggfunc="first")
pivoted["YoY_Growth_FY25"] = ((pivoted["FY25"] - pivoted["FY24"]) / pivoted["FY24"] * 100).round(2)

print("=== SALES COMPARISON ===")
print(pivoted)
