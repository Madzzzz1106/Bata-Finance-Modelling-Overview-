import pandas as pd
import re

def parse_year_num(fy_str):
    match = re.search(r'\d+', str(fy_str))
    if match:
        return int(match.group(0))
    return None

df = pd.read_csv("extracted/master_financials.csv")
df["YearNum"] = df["FinancialYear"].apply(parse_year_num)

bata_df = df[df["Company"] == "Bata"]
years = sorted(bata_df["YearNum"].dropna().unique())

for yr in years:
    yr_str = f"FY{str(yr)[-2:]}"
    yr_df = bata_df[bata_df["YearNum"] == yr]
    
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

    cfo = get_val("cashflow", [r"Cash.*Operating.*Activity", r"Net cash.*operating", r"Net cash inflow from operating activities"])
    print(f"{yr_str}: CFO = {cfo}")

