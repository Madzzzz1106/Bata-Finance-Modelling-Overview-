import pandas as pd
df = pd.read_csv("extracted/master_financials.csv")
cfo_df = df[(df["Company"] == "Metro") & (df["Metric"].str.contains("Net cash generated from", case=False, na=False))]
print(cfo_df[["FinancialYear", "Metric", "Value", "data_status", "unit_original"]])
