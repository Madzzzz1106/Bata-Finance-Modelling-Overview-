import pandas as pd

df = pd.read_csv("extracted/master_financials.csv")
bata_fy25 = df[(df["Company"] == "Bata") & (df["FinancialYear"] == "FY25")]

print("=== BATA FY25 MASTER FINANCIALS ===")
for idx, row in bata_fy25.iterrows():
    print(f"Statement: {row['Statement']} | Metric: {row['Metric']} | Value: {row['Value']}")
