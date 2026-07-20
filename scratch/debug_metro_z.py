import pandas as pd
import re

df = pd.read_csv("extracted/master_financials.csv")
def parse_year_num(fy_str):
    match = re.search(r'\d+', str(fy_str))
    if match:
        return int(match.group(0))
    return None
df["YearNum"] = df["FinancialYear"].apply(parse_year_num)

m_df = df[df["Company"] == "Metro"]
years = sorted(m_df["YearNum"].dropna().unique())

pivoted_rows = []
for yr in years:
    yr_str = f"FY{str(yr)[-2:]}"
    yr_df = m_df[m_df["YearNum"] == yr]
    
    def get_val(statement, metric_patterns):
        stmt_df = yr_df[yr_df["Statement"].str.contains(statement, case=False, na=False)]
        res = pd.DataFrame()
        for pat in metric_patterns:
            match_df = stmt_df[stmt_df["Metric"].str.contains(pat, case=False, na=False)]
            if not match_df.empty:
                res = match_df
                break
        if not res.empty:
            return float(res.iloc[0]["Value"])
        return None

    # Total Assets
    ta = get_val("balance_sheet", [r"Total assets\s*\(Current Assets\)", r"Total assets\s*\(1\+2\)\s*\(Current Assets\)", r"Total assets", r"Total assets\s*\(1\+2\)"])
    
    # Book Value of Equity
    bve = get_val("balance_sheet", [r"^Total equity$", r"^Total Equity$"])
    if bve is None:
        sc = get_val("balance_sheet", [r"^Equity share capital$", r"^Equity Share Capital$"]) or 0.0
        oe = get_val("balance_sheet", [r"^Other equity$", r"^Other Equity$"]) or 0.0
        bve = sc + oe

    retained = get_val("balance_sheet", [r"^Other equity$", r"^Other Equity$"])
    sales = get_val("pnl", ["Sales", "Revenue from operations", "Revenue from Operations"])
    pbt = get_val("pnl", ["Profit before tax", "Profit Before Tax"])
    interest = get_val("pnl", ["Interest", "Finance Costs", "Finance costs", "Finance Cost"])
    ebit = (pbt + interest) if (pbt is not None and interest is not None) else None
    
    print(f"FY{yr} -> TA: {ta}, BVE: {bve}, Retained: {retained}, Sales: {sales}, EBIT: {ebit}")
