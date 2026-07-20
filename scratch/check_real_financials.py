import pandas as pd

df = pd.read_csv("extracted/master_financials.csv")
bata = df[df["Company"].str.lower() == "bata"].copy()
print("Unique statements for Bata:")
print(bata["Statement"].unique())

print("\nPNL metrics for Bata:")
pnl = bata[bata["Statement"].str.contains("pnl|profit_and_loss|profit|income", case=False)]
print(pnl["Metric"].unique())

# Let's filter for Revenue and Net Profit metrics
revenue_metrics = pnl[pnl["Metric"].str.contains("revenue|operations|turnover", case=False)]
print("\nRevenue metrics:")
print(revenue_metrics[["FinancialYear", "Metric", "Value"]])

pat_metrics = pnl[pnl["Metric"].str.contains("profit for the year|net profit|pat|profit after tax", case=False)]
print("\nNet Profit (PAT) metrics:")
print(pat_metrics[["FinancialYear", "Metric", "Value"]])
