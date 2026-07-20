import pandas as pd

df = pd.read_csv("extracted/master_financials.csv")
r_cf = df[(df["Company"] == "Relaxo") & (df["Statement"] == "cashflow")]
print("=== Relaxo Cash Flow Metrics in Master ===")
for m in sorted(r_cf["Metric"].unique()):
    print("  ", m)
