import pandas as pd

# Load ratio analysis data
df_ratio = pd.read_csv("extracted/ratio_analysis.csv")

# Let's inspect the values for Bata, Metro, Relaxo, Campus
target_companies = ["Bata", "Metro", "Relaxo", "Campus Activewear"]
print(df_ratio[df_ratio["Company"].isin(target_companies)])
