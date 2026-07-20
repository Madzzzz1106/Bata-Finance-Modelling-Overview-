import os
import glob
import pandas as pd
import re

def parse_year_from_filename(filename):
    match = re.search(r'_FY(\d{2})_', filename)
    if match:
        short_year = int(match.group(1))
        return 2000 + short_year
    return None

def test_pnl_bs():
    pdf_csvs = glob.glob(os.path.join("extracted", "*_FY[2-9][0-9]_balance_sheet.csv"))
    for f in sorted(pdf_csvs):
        basename = os.path.basename(f)
        company = basename.split("_")[0]
        df = pd.read_csv(f)
        print(f"\n--- {basename} ---")
        
        current_section = "Unknown"
        for idx, row in df.iterrows():
            metric = str(row["Particulars"]).strip()
            if not metric or pd.isna(row["Particulars"]):
                continue
            val_curr = row.get("CurrentYear")
            val_prev = row.get("PreviousYear")
            
            is_empty_val = (pd.isna(val_curr) or str(val_curr).strip() == "") and (pd.isna(val_prev) or str(val_prev).strip() == "")
            if is_empty_val:
                metric_lower = metric.lower()
                if "non-current assets" in metric_lower or "non current assets" in metric_lower:
                    current_section = "Non-Current Assets"
                elif "current assets" in metric_lower:
                    current_section = "Current Assets"
                elif "non-current liabilities" in metric_lower or "non current liabilities" in metric_lower:
                    current_section = "Non-Current Liabilities"
                elif "current liabilities" in metric_lower:
                    current_section = "Current Liabilities"
                elif "equity" in metric_lower and not "liabilities" in metric_lower:
                    current_section = "Equity"
                print(f"  [Header] -> {metric} (Active Section: {current_section})")
            else:
                if current_section in ["Non-Current Assets", "Current Assets", "Non-Current Liabilities", "Current Liabilities"]:
                    print(f"    {metric} ({current_section}) = {val_curr}")
                else:
                    print(f"    {metric} = {val_curr}")

if __name__ == "__main__":
    test_pnl_bs()
