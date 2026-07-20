import glob
import pandas as pd
import re

csvs = glob.glob("extracted/*.csv")
found_count = 0

for f in sorted(csvs):
    if "master_financials" in f or "results" in f:
        continue
    df = pd.read_csv(f)
    for col in df.columns:
        if col == "Particulars" or col == "Note":
            continue
        for idx, val in enumerate(df[col]):
            val_str = str(val).strip()
            # If it has two decimal points or a pattern of two numbers merged
            if val_str.count('.') >= 2:
                print(f"File: {f}")
                print(f"  Row {idx+2}: {df.iloc[idx]['Particulars']} -> Col: {col} -> Val: {val_str}")
                found_count += 1

print(f"\nTotal merged values found: {found_count}")
