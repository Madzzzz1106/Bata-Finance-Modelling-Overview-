import pandas as pd

df = pd.read_csv("extracted/forensic_screening_results.csv")
print("All FY25 Forensic results:")
print(df[df["FinancialYear"] == "FY25"][["Company", "Altman_Z_Score", "Z_Score_Zone"]])

print("\nFull table for all companies:")
print(df[["Company", "FinancialYear", "Altman_Z_Score", "Z_Score_Zone"]].to_string())
