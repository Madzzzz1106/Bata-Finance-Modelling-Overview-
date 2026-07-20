import pandas as pd

df = pd.read_csv("extracted/master_financials.csv")

# Spot check Bata FY25 Total Assets
bata_assets = df[(df["Company"] == "Bata") & (df["FinancialYear"] == "FY25") & (df["Metric"].str.lower().str.contains("total assets"))]
print("--- Bata FY25 Total Assets in Master ---")
print(bata_assets.to_string())

# Spot check Metro FY21 Total Assets (Lakhs conversion check)
metro_assets_fy21 = df[(df["Company"] == "Metro") & (df["FinancialYear"] == "FY21") & (df["Metric"].str.lower().str.contains("total assets"))]
print("\n--- Metro FY21 Total Assets in Master ---")
print(metro_assets_fy21.to_string())

# Check data_status for Campus FY26
campus_fy26 = df[(df["Company"] == "Campus Activewear") & (df["FinancialYear"] == "FY26")].head(3)
print("\n--- Campus FY26 sample rows ---")
print(campus_fy26.to_string())
