import pandas as pd
import glob
import os

files = glob.glob("extracted/*.csv")
for f in files:
    df = pd.read_csv(f)
    print(f"{os.path.basename(f)}: {len(df)} rows")
