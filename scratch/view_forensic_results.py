import pandas as pd

df = pd.read_csv("extracted/forensic_screening_results.csv")
print("Columns:", df.columns)
print(df[df["Company"] == "Bata"][["FinancialYear", "Current_Ratio", "Asset_Turnover"]])
print("\nPeer Averages:")
print(df.groupby("FinancialYear")[["Current_Ratio", "Asset_Turnover"]].mean())
