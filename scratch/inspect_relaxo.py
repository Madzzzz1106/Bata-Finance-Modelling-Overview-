import pandas as pd

df = pd.read_csv("extracted/master_financials.csv")
r_df = df[df["Company"] == "Relaxo"]
m_df = df[df["Company"] == "Metro"]

print("=== Relaxo Assets / Liabilities / Total Metrics ===")
for m in sorted(r_df["Metric"].unique()):
    if any(k in m.lower() for k in ["total", "asset", "liabilit", "equity"]):
        print("  ", m)

print("\n=== Metro Assets / Liabilities / Total Metrics ===")
for m in sorted(m_df["Metric"].unique()):
    if any(k in m.lower() for k in ["total", "asset", "liabilit", "equity"]):
        print("  ", m)
