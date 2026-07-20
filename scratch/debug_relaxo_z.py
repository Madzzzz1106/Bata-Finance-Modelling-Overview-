import pandas as pd
import re

def parse_year_num(fy_str):
    match = re.search(r'\d+', str(fy_str))
    if match:
        return int(match.group(0))
    return None

df = pd.read_csv("extracted/master_financials.csv")
df["YearNum"] = df["FinancialYear"].apply(parse_year_num)

r_df = df[df["Company"] == "Relaxo"]
years = sorted(r_df["YearNum"].dropna().unique())

for yr in years:
    yr_df = r_df[r_df["YearNum"] == yr]
    
    # helper
    def get_val(metric_patterns):
        res = pd.DataFrame()
        for pat in metric_patterns:
            match_df = yr_df[yr_df["Metric"].str.contains(pat, case=False, na=False)]
            if not match_df.empty:
                res = match_df
                break
        if not res.empty:
            return float(res.iloc[0]["Value"])
        return None

    ta = get_val([r"Total assets\s*\(Current Assets\)", r"Total assets"])
    bve = get_val([r"Total equity"])
    if bve is None:
        sc = get_val([r"Equity share capital", r"Equity Share Capital"]) or 0.0
        oe = get_val([r"Other equity", r"Other Equity"]) or 0.0
        bve = sc + oe
        
    print(f"Year: FY{yr} -> TotalAssets: {ta}, BookValueOfEquity: {bve}, Difference (Total Liabilities): {ta - bve if (ta is not None and bve is not None) else None}")
