import pandas as pd

df = pd.read_csv("extracted/master_financials.csv")
print("Columns:", df.columns)
print("Companies:", df["Company"].unique())

for comp in df["Company"].unique():
    comp_df = df[df["Company"] == comp]
    print(f"\n=== Metrics for {comp} ({len(comp_df)} rows) ===")
    print(comp_df["Metric"].unique()[:40])
