import pandas as pd
import re

df = pd.read_csv("extracted/master_financials.csv")

companies = df["Company"].unique()
metrics_by_company = {}
for comp in companies:
    metrics_by_company[comp] = sorted(list(df[df["Company"] == comp]["Metric"].unique()))

def find_metrics(comp, pattern):
    rx = re.compile(pattern, re.IGNORECASE)
    matches = [m for m in metrics_by_company[comp] if rx.search(m)]
    return matches

for comp in companies:
    print(f"\n=== Mappings for {comp} ===")
    print("Total Assets:", find_metrics(comp, r"total\s+assets|^total$"))
    print("Current Assets:", find_metrics(comp, r"current\s+asset|total\s+current\s+assets"))
    print("Current Liabilities:", find_metrics(comp, r"current\s+liabilit|^other\s+liabilities$"))
    print("Total Liabilities:", find_metrics(comp, r"total\s+liabilit|^total$"))
    print("Equity/Reserves:", find_metrics(comp, r"equity|reserve"))
    print("Sales:", find_metrics(comp, r"sales|revenue\s+from\s+operations"))
    print("Receivables:", find_metrics(comp, r"receivables|debtors"))
    print("Depreciation:", find_metrics(comp, r"depreciation"))
    print("CFO:", find_metrics(comp, r"operating\s+activ"))
    print("Interest/Finance:", find_metrics(comp, r"interest|finance\s+cost"))
