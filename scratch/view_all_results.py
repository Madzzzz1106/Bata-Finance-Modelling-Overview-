import pandas as pd
df = pd.read_csv("extracted/forensic_screening_results.csv")
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 1000)
print(df)
