import pandas as pd
df = pd.read_csv("extracted/master_financials.csv")
print(df.groupby(["Company", "Statement"])["FinancialYear"].unique())
