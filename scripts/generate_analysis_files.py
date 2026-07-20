import pandas as pd
import numpy as np
import re
import os

def parse_year_num(fy_str):
    match = re.search(r'\d+', str(fy_str))
    if match:
        return int(match.group(0))
    return None

def main():
    df = pd.read_csv("extracted/master_financials.csv")
    df["YearNum"] = df["FinancialYear"].apply(parse_year_num)
    
    companies = df["Company"].unique()
    pivoted_rows = []
    
    for comp in companies:
        comp_df = df[df["Company"] == comp]
        years = sorted(comp_df["YearNum"].dropna().unique())
        
        for yr in years:
            yr_str = f"FY{str(yr)[-2:]}"
            yr_df = comp_df[comp_df["YearNum"] == yr]
            
            def get_val(statement, metric_patterns, exact=False):
                stmt_df = yr_df[yr_df["Statement"].str.contains(statement, case=False, na=False)]
                if exact:
                    res = stmt_df[stmt_df["Metric"].isin(metric_patterns)]
                else:
                    res = pd.DataFrame()
                    for pat in metric_patterns:
                        match_df = stmt_df[stmt_df["Metric"].str.contains(pat, case=False, na=False)]
                        if not match_df.empty:
                            res = match_df
                            break
                if not res.empty:
                    return float(res.iloc[0]["Value"])
                return None

            is_excel = comp in ["Campus Activewear", "Khadim India", "Liberty Shoes"]
            
            # Sales
            sales = get_val("pnl", ["Sales", "Revenue from operations", "Revenue from Operations"])
            
            # COGS
            if is_excel:
                raw_mat = get_val("pnl", ["Raw Material Cost"], exact=True) or 0.0
                change_inv = get_val("pnl", ["Change in Inventory"], exact=True) or 0.0
                cogs = raw_mat - change_inv
            else:
                rm = get_val("pnl", [r"Cost of.*material.*consumed", r"Cost of raw materials"]) or 0.0
                pur = get_val("pnl", [r"Purchases of stock-in-trade", r"Purchases of Stock-in-Trade", r"Purchase of stock-in-trade"]) or 0.0
                chg = get_val("pnl", [r"Changes in inventor", r"Change.*in.*inventor"]) or 0.0
                cogs = rm + pur + chg
            if cogs == 0.0:
                cogs = None

            # Receivables
            receivables = get_val("balance_sheet", [r"Trade receivables\s*\(Current Assets\)", r"Trade Receivables\s*\(Current Assets\)", r"Trade receivables", r"Receivables"])
            
            # Inventory
            if is_excel:
                inventory = get_val("balance_sheet", ["Inventory"], exact=True)
            else:
                inventory = get_val("balance_sheet", [r"Inventories\s*\(Current Assets\)", r"Inventories", r"Inventory"])
                
            # Net Profit
            np_val = get_val("pnl", ["Net profit", "Net Profit", "Profit for the year", "Profit/loss for the period", r"Profit/\s*\(Loss\)\s*for\s*the\s*year", r"Profit after tax for the year"])
            
            # EBIT / EBITDA Components
            pbt = get_val("pnl", ["Profit before tax", "Profit Before Tax", r"Profit/\s*\(Loss\)\s*before\s*tax"])
            interest = get_val("pnl", ["Interest", "Finance Costs", "Finance costs", "Finance Cost"])
            ebit = (pbt + interest) if (pbt is not None and interest is not None) else None
            depr = get_val("pnl", ["Depreciation", "Depreciation and Amortisation Expense", "Depreciation and amortisation expense"])
            ebitda = (ebit + depr) if (ebit is not None and depr is not None) else None
            
            pivoted_rows.append({
                "Company": comp,
                "FinancialYear": yr_str,
                "YearNum": yr,
                "Sales": sales,
                "COGS": cogs,
                "Receivables": receivables,
                "Inventory": inventory,
                "EBITDA": ebitda,
                "NetProfit": np_val
            })
            
    df_pivot = pd.DataFrame(pivoted_rows)
    df_pivot.sort_values(by=["Company", "YearNum"], inplace=True)
    
    # Calculate Ratios
    df_pivot["Receivable_Days"] = (df_pivot["Receivables"] / df_pivot["Sales"]) * 365
    df_pivot["Inventory_Days"] = (df_pivot["Inventory"] / df_pivot["COGS"]) * 365
    df_pivot["Gross_Margin_Pct"] = ((df_pivot["Sales"] - df_pivot["COGS"]) / df_pivot["Sales"]) * 100
    df_pivot["EBITDA_Margin_Pct"] = (df_pivot["EBITDA"] / df_pivot["Sales"]) * 100
    df_pivot["Net_Margin_Pct"] = (df_pivot["NetProfit"] / df_pivot["Sales"]) * 100
    
    # Round values for readability
    ratio_cols = ["Receivable_Days", "Inventory_Days", "Gross_Margin_Pct", "EBITDA_Margin_Pct", "Net_Margin_Pct"]
    for col in ratio_cols:
        df_pivot[col] = df_pivot[col].round(2)
        
    # Output ratio_analysis.csv
    out_ratio_cols = ["Company", "FinancialYear"] + ratio_cols
    df_pivot[out_ratio_cols].to_csv("extracted/ratio_analysis.csv", index=False)
    print("Saved extracted/ratio_analysis.csv")
    
    # Load forensic results for peer benchmark averages
    df_forensic = pd.read_csv("extracted/forensic_screening_results.csv")
    peer_avg = df_forensic.groupby("FinancialYear")[["Current_Ratio", "Asset_Turnover"]].mean().reset_index()
    peer_avg.rename(columns={
        "Current_Ratio": "Peer_Average_Current_Ratio",
        "Asset_Turnover": "Peer_Average_Asset_Turnover"
    }, inplace=True)
    
    # Sort peer averages chronologically
    peer_avg["YearNum"] = peer_avg["FinancialYear"].apply(parse_year_num)
    peer_avg.sort_values(by="YearNum", inplace=True)
    peer_avg.drop(columns=["YearNum"], inplace=True)
    
    # Round values
    peer_avg["Peer_Average_Current_Ratio"] = peer_avg["Peer_Average_Current_Ratio"].round(2)
    peer_avg["Peer_Average_Asset_Turnover"] = peer_avg["Peer_Average_Asset_Turnover"].round(2)
    
    # Output peer_benchmark.csv
    peer_avg.to_csv("extracted/peer_benchmark.csv", index=False)
    print("Saved extracted/peer_benchmark.csv")

if __name__ == "__main__":
    main()
