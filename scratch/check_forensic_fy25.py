import pandas as pd

df = pd.read_csv("extracted/forensic_screening_results.csv")
target_companies = ["Bata", "Metro", "Relaxo", "Campus Activewear", "Liberty Shoes", "Khadim India"]
fy25_data = df[(df["Company"].isin(target_companies)) & (df["FinancialYear"] == "FY25")]

print("=== FORENSIC SCREENING FY25 RESULTS ===")
print(fy25_data[["Company", "Altman_Z_Score", "Z_Score_Zone", "Debt_To_Equity"]])
