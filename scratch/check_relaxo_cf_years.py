import pandas as pd
df = pd.read_csv("extracted/master_financials.csv")

r_cf = df[(df["Company"] == "Relaxo") & (df["Statement"] == "cashflow")]
for yr in sorted(r_cf["FinancialYear"].unique()):
    yr_df = r_cf[r_cf["FinancialYear"] == yr]
    print(f"\n--- {yr} ---")
    cfo_rows = yr_df[yr_df["Metric"].str.contains("operating", case=False, na=False)]
    print(cfo_rows[["Metric", "Value"]])
