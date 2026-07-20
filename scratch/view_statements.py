import pandas as pd
df = pd.read_csv("extracted/master_financials.csv")
for comp in df["Company"].unique():
    print(f"Company: {comp}")
    print("  Statements:", df[df["Company"] == comp]["Statement"].unique())
