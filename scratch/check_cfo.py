import pandas as pd

df = pd.read_csv("extracted/master_financials.csv")
bata_cf = df[(df["Company"].str.lower() == "bata") & (df["Statement"].str.contains("cashflow", case=False))].copy()

print("Bata cashflow metrics:")
print(bata_cf["Metric"].unique())

cfo_metrics = bata_cf[bata_cf["Metric"].str.contains("operating|operating activities", case=False)]
print("\nCFO metrics for Bata across years:")
print(cfo_metrics[["FinancialYear", "Metric", "Value"]])
