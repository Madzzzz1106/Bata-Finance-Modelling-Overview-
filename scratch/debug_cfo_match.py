import pandas as pd
df = pd.read_csv("extracted/master_financials.csv")

m_cf = df[(df["Company"] == "Metro") & (df["Statement"] == "cashflow")]
print("=== Metro Cash Flow Metrics ===")
for m in m_cf["Metric"].unique():
    print("  ", m)

print("\n--- Testing patterns ---")
patterns = [
    "Cash from Operating Activity", 
    "Net Cash Generated from Operating Activities", 
    "Net cash flow from operating activities", 
    "Net cash generated from operating activities", 
    "Net Cash Generated from / (used in) Operating Activities"
]

for pat in patterns:
    matches = m_cf[m_cf["Metric"].str.contains(pat, case=False, na=False)]
    print(f"Pattern: {pat} -> Matches: {len(matches)}")
    if not matches.empty:
        print(matches[["Metric", "Value"]])
