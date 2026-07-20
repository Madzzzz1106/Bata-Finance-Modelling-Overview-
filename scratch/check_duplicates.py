import pandas as pd

# Load master
df = pd.read_csv("extracted/master_financials.csv")

# Let's count how many times "Investments" or "Lease Liabilities" appear for a single company-year-statement
dup_check = df[(df["Company"] == "Relaxo") & (df["FinancialYear"] == "FY25") & (df["Statement"] == "balance_sheet")]
print("=== Relaxo FY25 BS Rows in Master ===")
print(dup_check[["Metric", "Value"]])
