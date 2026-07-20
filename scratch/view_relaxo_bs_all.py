import pandas as pd
df = pd.read_csv("extracted/master_financials.csv")
r_bs = df[(df["Company"] == "Relaxo") & (df["Statement"] == "balance_sheet") & (df["FinancialYear"] == "FY25")]
for idx, row in r_bs.iterrows():
    print(f"{row['Metric']}: {row['Value']}")
