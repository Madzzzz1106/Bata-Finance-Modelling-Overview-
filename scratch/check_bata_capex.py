import pandas as pd

df = pd.read_csv("extracted/master_financials.csv")
bata = df[df["Company"] == "Bata"]

# Capex is in cashflow, usually under "Purchase of property" or similar.
capex_rows = bata[(bata["Statement"] == "cashflow") & (bata["Metric"].str.contains("purchase of property|capital expenditure|acquisition of property", case=False, na=False))]

print("=== Capex Rows ===")
print(capex_rows[["FinancialYear", "Metric", "Value"]])
