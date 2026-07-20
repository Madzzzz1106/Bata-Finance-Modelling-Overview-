import pandas as pd
df = pd.read_csv("extracted/master_financials.csv")
print("Relaxo Statements:", df[df["Company"] == "Relaxo"]["Statement"].unique())
print("Relaxo BS Row count:", len(df[(df["Company"] == "Relaxo") & (df["Statement"] == "Balance Sheet")]))
print("Relaxo PNL Row count:", len(df[(df["Company"] == "Relaxo") & (df["Statement"] == "Profit & Loss")]))
print("Relaxo Cash Flow Row count:", len(df[(df["Company"] == "Relaxo") & (df["Statement"] == "Cash Flow")]))
print("Some Relaxo Rows:")
print(df[df["Company"] == "Relaxo"][["Statement", "Metric"]].drop_duplicates().head(30))
