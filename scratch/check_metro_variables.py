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

    def get_sum(statement, pattern):
        stmt_df = yr_df[yr_df["Statement"].str.contains(statement, case=False, na=False)]
        matches = stmt_df[stmt_df["Metric"].str.contains(pattern, case=False, na=False)]
        if not matches.empty:
            vals = pd.to_numeric(matches["Value"], errors="coerce")
            return float(vals.sum())
        return 0.0

    ta = get_val("balance_sheet", [r"Total assets\s*\(Current Assets\)", r"Total assets\s*\(1\+2\)\s*\(Current Assets\)", r"Total assets", r"Total assets\s*\(1\+2\)"])
    ca = get_sum("balance_sheet", r"\(Current Assets\)")
    cl = get_sum("balance_sheet", r"\(Current Liabilities\)")
    
    sc = get_val("balance_sheet", [r"Equity share capital", r"Equity Share Capital"]) or 0.0
    oe = get_val("balance_sheet", [r"Other equity", r"Other Equity"]) or 0.0
    bve = sc + oe
    
    retained = get_val("balance_sheet", [r"Other equity", r"Other Equity"])
    sales = get_val("pnl", ["Sales", "Revenue from operations", "Revenue from Operations"])
    
    rm = get_val("pnl", [r"Cost of.*material.*consumed", r"Cost of raw materials"]) or 0.0
    pur = get_val("pnl", [r"Purchases of stock-in-trade", r"Purchases of Stock-in-Trade"]) or 0.0
    chg = get_val("pnl", [r"Changes in inventor", r"Change.*in.*inventor"]) or 0.0
    cogs = rm + pur + chg
    
    pbt = get_val("pnl", ["Profit before tax", "Profit Before Tax"])
    interest = get_val("pnl", ["Interest", "Finance Costs", "Finance costs", "Finance Cost"])
    ebit = (pbt + interest) if (pbt is not None and interest is not None) else None
    
    np_val = get_val("pnl", ["Net profit", "Net Profit", "Profit for the year", "Profit/loss for the period"])
    receivables = get_val("balance_sheet", [r"Trade receivables\s*\(Current Assets\)", r"Trade Receivables\s*\(Current Assets\)", r"Trade receivables"])
    depr = get_val("pnl", ["Depreciation", "Depreciation and Amortisation Expense", "Depreciation and amortisation expense"])
    sga = get_val("pnl", ["Other expenses", "Other Expenses"])
    debt = get_sum("balance_sheet", r"Lease Liabilities|Borrowings")
    cfo = get_val("cashflow", ["Cash from Operating Activity", "Net Cash Generated from Operating Activities", "Net cash flow from operating activities", "Net cash generated from operating activities", "Net Cash Generated from / (used in) Operating Activities"])
    ppe = get_val("balance_sheet", [r"Property, Plant and Equipment\s*\(Non-Current Assets\)", r"Property, plant and equipment\s*\(Non-Current Assets\)", r"Property, plant and equipment"])

    pivoted_rows.append({
        "FinancialYear": yr_str,
        "TotalAssets": ta, "CurrentAssets": ca, "CurrentLiabilities": cl,
        "BookValueOfEquity": bve, "RetainedEarnings": retained, "Sales": sales,
        "COGS": cogs, "EBIT": ebit, "NetProfit": np_val, "Receivables": receivables,
        "Depreciation": depr, "SGA": sga, "TotalDebt": debt, "CFO": cfo, "NetPPE": ppe
    })

df_p = pd.DataFrame(pivoted_rows)

# Shifted values for index calculations
df_p["Prev_Sales"] = df_p["Sales"].shift(1)
df_p["Prev_Receivables"] = df_p["Receivables"].shift(1)
df_p["Prev_COGS"] = df_p["COGS"].shift(1)
df_p["Prev_CurrentAssets"] = df_p["CurrentAssets"].shift(1)
df_p["Prev_NetPPE"] = df_p["NetPPE"].shift(1)
df_p["Prev_TotalAssets"] = df_p["TotalAssets"].shift(1)
df_p["Prev_Depreciation"] = df_p["Depreciation"].shift(1)
df_p["Prev_SGA"] = df_p["SGA"].shift(1)
df_p["Prev_TotalDebt"] = df_p["TotalDebt"].shift(1)

# Indexes
df_p["DSRI"] = (df_p["Receivables"] / df_p["Sales"]) / (df_p["Prev_Receivables"] / df_p["Prev_Sales"])
prev_gm = (df_p["Prev_Sales"] - df_p["Prev_COGS"]) / df_p["Prev_Sales"]
curr_gm = (df_p["Sales"] - df_p["COGS"]) / df_p["Sales"]
df_p["GMI"] = prev_gm / curr_gm
curr_aq = 1.0 - (df_p["CurrentAssets"] + df_p["NetPPE"]) / df_p["TotalAssets"]
prev_aq = 1.0 - (df_p["Prev_CurrentAssets"] + df_p["Prev_NetPPE"]) / df_p["Prev_TotalAssets"]
df_p["AQI"] = curr_aq / prev_aq
df_p["SGI"] = df_p["Sales"] / df_p["Prev_Sales"]
curr_dep_rate = df_p["Depreciation"] / (df_p["NetPPE"] + df_p["Depreciation"])
prev_dep_rate = df_p["Prev_Depreciation"] / (df_p["Prev_NetPPE"] + df_p["Prev_Depreciation"])
df_p["DEPI"] = prev_dep_rate / curr_dep_rate
df_p["SGAI"] = (df_p["SGA"] / df_p["Sales"]) / (df_p["Prev_SGA"] / df_p["Prev_Sales"])
df_p["LVGI"] = (df_p["TotalDebt"] / df_p["TotalAssets"]) / (df_p["Prev_TotalDebt"] / df_p["Prev_TotalAssets"])
df_p["TATA"] = (df_p["NetProfit"] - df_p["CFO"]) / df_p["TotalAssets"]

df_p["M_Score"] = (
    -4.84 + 
    0.920 * df_p["DSRI"] + 
    0.528 * df_p["GMI"] + 
    0.404 * df_p["AQI"] + 
    0.892 * df_p["SGI"] + 
    0.115 * df_p["DEPI"] - 
    0.172 * df_p["SGAI"] + 
    4.037 * df_p["TATA"] + 
    0.0327 * df_p["LVGI"]
)

pd.set_option('display.max_columns', 25)
print(df_p[["FinancialYear", "M_Score", "DSRI", "GMI", "AQI", "SGI", "DEPI", "SGAI", "TATA", "LVGI", "Receivables", "Sales", "COGS", "TotalAssets", "NetProfit", "CFO"]])
