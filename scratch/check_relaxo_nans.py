import pandas as pd
import numpy as np
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

pivoted_rows = []
for yr in years:
    yr_str = f"FY{str(yr)[-2:]}"
    yr_df = r_df[r_df["YearNum"] == yr]
    
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

    ta = get_val("balance_sheet", [r"Total assets\s*\(Current Assets\)", r"Total assets"])
    ca = get_sum("balance_sheet", r"\(Current Assets\)")
    cl = get_sum("balance_sheet", r"\(Current Liabilities\)")
    
    sc = get_val("balance_sheet", [r"^Equity share capital$", r"^Equity Share Capital$"]) or 0.0
    oe = get_val("balance_sheet", [r"^Other equity$", r"^Other Equity$"]) or 0.0
    bve = sc + oe
    
    retained = get_val("balance_sheet", [r"^Other equity$", r"^Other Equity$"])
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
print("=== pivoted data ===")
print(df_p.to_string())
