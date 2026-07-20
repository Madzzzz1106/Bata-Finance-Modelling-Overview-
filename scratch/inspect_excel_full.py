import pandas as pd

excel_path = "Campus Activewe.xlsx"
for sheet in ["Profit & Loss", "Balance Sheet", "Cash Flow"]:
    print(f"\n--- Sheet: {sheet} ---")
    df = pd.read_excel(excel_path, sheet_name=sheet, header=None)
    for idx, row in df.head(10).iterrows():
        print(f"Row {idx}: {list(row)}")
