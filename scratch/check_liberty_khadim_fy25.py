import pandas as pd

# Load ratio analysis
df_ratio = pd.read_csv("extracted/ratio_analysis.csv")

# Let's inspect Liberty and Khadim in FY25
liberty_fy25_ratio = df_ratio[(df_ratio["Company"] == "Liberty Shoes") & (df_ratio["FinancialYear"] == "FY25")]
khadim_fy25_ratio = df_ratio[(df_ratio["Company"] == "Khadim India") & (df_ratio["FinancialYear"] == "FY25")]

print("=== LIBERTY SHOES FY25 RATIOS ===")
print(liberty_fy25_ratio)

print("\n=== KHADIM INDIA FY25 RATIOS ===")
print(khadim_fy25_ratio)

# Let's check the sales values from master financials
df_master = pd.read_csv("extracted/master_financials.csv")
liberty_sales = df_master[(df_master["Company"] == "Liberty Shoes") & (df_master["FinancialYear"] == "FY25") & (df_master["Statement"] == "pnl") & (df_master["Metric"].str.contains("revenue from operations|sales", case=False, na=False))]
khadim_sales = df_master[(df_master["Company"] == "Khadim India") & (df_master["FinancialYear"] == "FY25") & (df_master["Statement"] == "pnl") & (df_master["Metric"].str.contains("revenue from operations|sales", case=False, na=False))]

print("\n=== SALES VALUES ===")
print("Liberty Sales Row:")
print(liberty_sales[["Metric", "Value"]])
print("Khadim Sales Row:")
print(khadim_sales[["Metric", "Value"]])
