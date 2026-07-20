import pandas as pd
# Let's load the results of screen_forensics.py
# Since screen_forensics.py concatenates the results, we can just print the row for Metro in FY24
df = pd.read_csv("extracted/forensic_screening_results.csv")
print(df[df["Company"] == "Metro"])
