import pandas as pd
import numpy as np

# Load pivot data or calculate directly
# We can check what values were loaded in the screen_forensics code.
# Let's write a quick script that runs screen_forensics' variables and calculates public Z-score vs private Z'-score.
# We will inspect X1, X2, X3, X4, X5 for all companies in FY25.

df = pd.read_csv("extracted/forensic_screening_results.csv")
print("Private Z'-Score in forensic_screening_results.csv:")
print(df[df["FinancialYear"] == "FY25"][["Company", "Altman_Z_Score"]])

# Let's look at what data is in the master financials for Metro and others in FY25
df_master = pd.read_csv("extracted/master_financials.csv")
# Let's inspect the metrics for Metro in FY25
metro_fy25 = df_master[(df_master["Company"].str.lower() == "metro") & (df_master["FinancialYear"] == "FY25")]
print("\nMetro FY25 Metrics:")
print(metro_fy25[["Metric", "Value"]].to_string())
