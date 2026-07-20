import pandas as pd

df_forensic = pd.read_csv("extracted/forensic_screening_results.csv")
bata_forensic = df_forensic[df_forensic["Company"] == "Bata"]
print("--- Forensic ---")
print(bata_forensic[["FinancialYear", "Z_Score", "Current_Ratio", "Asset_Turnover", "M_Score"]])

df_master = pd.read_csv("extracted/master_financials.csv")
bata_master = df_master[df_master["Company"] == "Bata"]
cfo = bata_master[bata_master["Metric"].str.contains("Cash flow from operating", case=False, na=False)]
print("\n--- CFO ---")
print(cfo[["FinancialYear", "Value"]])
