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

def get_original_unit_and_factor(company, year):
    # Determine unit based on company and year
    comp_lower = company.lower()
    
    if comp_lower == "bata":
        return "INR Million", 0.1  # Divide by 10 to get Crores
    elif comp_lower == "relaxo":
        return "INR Crore", 1.0   # Already in Crores
    elif comp_lower == "metro":
        # Metro FY21, FY22, FY23 are in Lakhs
        # Metro FY24, FY25 are in Crores
        if year in [2020, 2021, 2022, 2023]:
            return "INR Lakhs", 0.01  # Divide by 100 to get Crores
        else:
            return "INR Crore", 1.0
    else:
        # Excel screener files are in INR Crores
        return "INR Crore", 1.0

def clean_num(s):
    s = s.strip()
    if not s:
        return None
    is_neg = False
    if '(' in s or ')' in s or '-' in s:
        is_neg = True
    s = s.replace(')', '').replace('(', '').replace('-', '').replace(',', '')
    try:
        val = float(s)
        return -val if is_neg else val
    except ValueError:
        return None

def split_merged(s):
    s = str(s).strip()
    matches = re.findall(r'[(-]?\d[\d,]*\.\d{2}[)]?', s)
    if len(matches) >= 2:
        part1 = matches[-2]
        part2 = matches[-1]
        v1 = clean_num(part1)
        v2 = clean_num(part2)
        return v1, v2
    return None

def build_master_csv():
    all_data = []
    
    # 1. Process PDF-extracted CSVs
    pdf_csvs = glob.glob(os.path.join("extracted", "*_FY[2-9][0-9]_*.csv"))
    print(f"Found {len(pdf_csvs)} PDF CSV files to consolidate.")
    
    for f in pdf_csvs:
        basename = os.path.basename(f)
        parts = basename.replace(".csv", "").split("_")
        company = parts[0]
        statement_name = "_".join(parts[2:])
        
        curr_year = parse_year_from_filename(basename)
        if not curr_year:
            print(f"Warning: Could not parse year from {basename}. Skipping.")
            continue
        prev_year = curr_year - 1
        
        df = pd.read_csv(f)
        statement_type = "standalone" if company.lower() == "relaxo" else "consolidated"
        
        current_section = "Unknown"
        for idx, row in df.iterrows():
            metric = row["Particulars"]
            if pd.isna(metric) or str(metric).strip() == "":
                continue
            metric = str(metric).strip()
            
            val_curr = row.get("CurrentYear")
            val_prev = row.get("PreviousYear")
            val_note = row.get("Note")
            
            # Check for merged values in Note column (e.g. Metro cash flow shifting)
            if not pd.isna(val_note) and str(val_note).strip() != "":
                res_note = split_merged(val_note)
                if res_note:
                    def is_float(x):
                        try:
                            float(str(x).replace('(', '').replace(')', '').replace(',', '').strip())
                            return True
                        except ValueError:
                            return False
                    curr_ok = not pd.isna(val_curr) and str(val_curr).strip() != "" and is_float(val_curr)
                    prev_ok = not pd.isna(val_prev) and str(val_prev).strip() != "" and is_float(val_prev)
                    if not curr_ok or not prev_ok:
                        val_curr, val_prev = res_note
                        
            # Otherwise check for merged values in PreviousYear or CurrentYear
            if (pd.isna(val_curr) or str(val_curr).strip() == "") and not pd.isna(val_prev):
                res = split_merged(val_prev)
                if res:
                    val_curr, val_prev = res
            elif (pd.isna(val_prev) or str(val_prev).strip() == "") and not pd.isna(val_curr):
                res = split_merged(val_curr)
                if res:
                    val_curr, val_prev = res


            
            # Check if it is a section header (empty values)
            is_empty_val = (pd.isna(val_curr) or str(val_curr).strip() == "") and (pd.isna(val_prev) or str(val_prev).strip() == "")
            if is_empty_val and "balance_sheet" in statement_name:
                metric_lower = metric.lower()
                if "non-current assets" in metric_lower or "non current assets" in metric_lower:
                    current_section = "Non-Current Assets"
                elif "current assets" in metric_lower:
                    current_section = "Current Assets"
                elif "non-current liabilities" in metric_lower or "non current liabilities" in metric_lower:
                    current_section = "Non-Current Liabilities"
                elif "current liabilities" in metric_lower:
                    current_section = "Current Liabilities"
                elif "equity" in metric_lower and "liabilities" not in metric_lower:
                    current_section = "Equity"
                continue # Skip writing header rows as metrics
            
            # Append active section to balance sheet metrics to prevent collision/deduplication drops
            if "balance_sheet" in statement_name and current_section in ["Non-Current Assets", "Current Assets", "Non-Current Liabilities", "Current Liabilities"]:
                metric = f"{metric} ({current_section})"
                
            # Current Year
            if not pd.isna(val_curr) and str(val_curr).strip() != "":
                try:
                    num_val = float(val_curr)
                    orig_unit, factor = get_original_unit_and_factor(company, curr_year)
                    converted_val = round(num_val * factor, 4)
                except ValueError:
                    orig_unit = "Text"
                    converted_val = val_curr
                    
                all_data.append({
                    "Company": company,
                    "FinancialYear": f"FY{str(curr_year)[2:]}",
                    "Statement": statement_name,
                    "Metric": metric,
                    "Value": converted_val,
                    "statement_type": statement_type,
                    "unit": "INR Crore",
                    "unit_original": orig_unit,
                    "data_status": "actual"
                })
                
            # Previous Year
            if not pd.isna(val_prev) and str(val_prev).strip() != "":
                try:
                    num_val = float(val_prev)
                    orig_unit, factor = get_original_unit_and_factor(company, curr_year)
                    converted_val = round(num_val * factor, 4)
                except ValueError:
                    orig_unit = "Text"
                    converted_val = val_prev

                    
                all_data.append({
                    "Company": company,
                    "FinancialYear": f"FY{str(prev_year)[2:]}",
                    "Statement": statement_name,
                    "Metric": metric,
                    "Value": converted_val,
                    "statement_type": statement_type,
                    "unit": "INR Crore",
                    "unit_original": orig_unit,
                    "data_status": "actual"
                })


    # 2. Process Excel-extracted CSVs
    excel_csvs = glob.glob(os.path.join("extracted", "*_*.csv"))
    excel_csvs = [f for f in excel_csvs if "_FY" not in f and "master_financials" not in f and "results" not in f]

    print(f"Found {len(excel_csvs)} Excel CSV files to consolidate.")
    
    for f in excel_csvs:
        basename = os.path.basename(f)
        parts = basename.replace(".csv", "").split("_")
        company = parts[0]
        statement_name = "_".join(parts[1:])
        
        df = pd.read_csv(f)
        statement_type = "consolidated"
        
        for idx, row in df.iterrows():
            metric = row["Particulars"]
            if pd.isna(metric) or str(metric).strip() == "":
                continue
                
            for col in df.columns:
                if col == "Particulars":
                    continue
                val = row[col]
                if not pd.isna(val) and str(val).strip() != "":
                    short_yr = str(col)[-2:]
                    yr_int = int(col)
                    
                    try:
                        num_val = float(val)
                        orig_unit, factor = get_original_unit_and_factor(company, yr_int)
                        converted_val = round(num_val * factor, 4)
                    except ValueError:
                        orig_unit = "Text"
                        converted_val = val
                        
                    data_status = "actual - recently reported" if yr_int == 2026 else "actual"
                    
                    all_data.append({
                        "Company": company,
                        "FinancialYear": f"FY{short_yr}",
                        "Statement": statement_name,
                        "Metric": metric,
                        "Value": converted_val,
                        "statement_type": statement_type,
                        "unit": "INR Crore",
                        "unit_original": orig_unit,
                        "data_status": data_status
                    })
                    
    master_df = pd.DataFrame(all_data)
    master_df.drop_duplicates(subset=["Company", "FinancialYear", "Statement", "Metric", "statement_type"], keep="first", inplace=True)
    
    master_path = os.path.join("extracted", "master_financials.csv")
    master_df.to_csv(master_path, index=False)
    
    print(f"\nMaster consolidation complete! Saved to {master_path}")
    print(f"Total master rows: {len(master_df)}")
    
    # Print row counts per company to verify coverage
    print("\nRow counts per Company:")
    print(master_df["Company"].value_counts())
    
if __name__ == "__main__":
    build_master_csv()
