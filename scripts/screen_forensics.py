import pandas as pd
import numpy as np
import os
import re

def parse_year_num(fy_str):
    match = re.search(r'\d+', str(fy_str))
    if match:
        return int(match.group(0))
    return None

def compute_forensics():
    # Load master financials
    df = pd.read_csv("extracted/master_financials.csv")
    
    # Standardize years to integer for sorting
    df["YearNum"] = df["FinancialYear"].apply(parse_year_num)
    
    companies = df["Company"].unique()
    
    pivoted_rows = []
    
    for comp in companies:
        comp_df = df[df["Company"] == comp]
        years = sorted(comp_df["YearNum"].dropna().unique())
        
        for yr in years:
            yr_str = f"FY{str(yr)[-2:]}"
            yr_df = comp_df[comp_df["YearNum"] == yr]
            
            # Helper to get value
            def get_val(statement, metric_patterns, exact=False):
                stmt_df = yr_df[yr_df["Statement"].str.contains(statement, case=False, na=False)]
                if exact:
                    res = stmt_df[stmt_df["Metric"].isin(metric_patterns)]
                else:
                    # check pattern
                    res = pd.DataFrame()
                    for pat in metric_patterns:
                        match_df = stmt_df[stmt_df["Metric"].str.contains(pat, case=False, na=False)]
                        if not match_df.empty:
                            res = match_df
                            break
                if not res.empty:
                    return float(res.iloc[0]["Value"])
                return None

            # Get values that are sum of items matching a pattern
            def get_sum(statement, pattern):
                stmt_df = yr_df[yr_df["Statement"].str.contains(statement, case=False, na=False)]
                matches = stmt_df[stmt_df["Metric"].str.contains(pattern, case=False, na=False)]
                if not matches.empty:
                    # Filter out non-numeric values
                    vals = pd.to_numeric(matches["Value"], errors="coerce")
                    return float(vals.sum())
                return 0.0

            # Extraction logic per company
            is_excel = comp in ["Campus Activewear", "Khadim India", "Liberty Shoes"]
            
            # 1. Total Assets
            if is_excel:
                # Excel sheets have "Total" under balance_sheet
                ta = get_val("balance_sheet", ["Total"], exact=True)
            else:
                # PDF sheets have "Total Assets (Current Assets)" or "Total assets" or similar
                ta = get_val("balance_sheet", [r"Total assets\s*\(Current Assets\)", r"Total assets\s*\(1\+2\)\s*\(Current Assets\)", r"Total assets"])
                
            # 2. Current Assets
            if is_excel:
                # Sum of: Inventory, Receivables, Cash & Bank, Investments (if any)
                inv = get_val("balance_sheet", ["Inventory"], exact=True) or 0.0
                rec = get_val("balance_sheet", ["Receivables"], exact=True) or 0.0
                cash = get_val("balance_sheet", ["Cash & Bank"], exact=True) or 0.0
                investments = get_val("balance_sheet", ["Investments"], exact=True) or 0.0
                ca = inv + rec + cash + investments
            else:
                if comp == "Relaxo":
                    # Relaxo has no "Total current assets" row, so we sum the elements ending in (Current Assets)
                    ca = get_sum("balance_sheet", r"\(Current Assets\)")
                else:
                    ca = get_val("balance_sheet", [r"Total current assets"])
                    
            # 3. Current Liabilities
            if is_excel:
                cl = get_val("balance_sheet", ["Other Liabilities"], exact=True)
            else:
                if comp == "Relaxo":
                    cl = get_sum("balance_sheet", r"\(Current Liabilities\)")
                else:
                    cl = get_val("balance_sheet", [r"Total current liabilities"])
                    
            # 4. Book Value of Equity
            if is_excel:
                sc = get_val("balance_sheet", ["Equity Share Capital"], exact=True) or 0.0
                reserves = get_val("balance_sheet", ["Reserves"], exact=True) or 0.0
                bve = sc + reserves
            else:
                bve = get_val("balance_sheet", [r"Total equity$"])
                if bve is None:
                    # Calculate as Share Capital + Other Equity
                    sc = get_val("balance_sheet", [r"Equity share capital", r"Equity Share Capital"]) or 0.0
                    oe = get_val("balance_sheet", [r"Other equity", r"Other Equity"]) or 0.0
                    bve = sc + oe
                    
            # 5. Retained Earnings
            if is_excel:
                retained = get_val("balance_sheet", ["Reserves"], exact=True)
            else:
                retained = get_val("balance_sheet", [r"Other equity", r"Other Equity"])


                
            # 6. Sales
            sales = get_val("pnl", ["Sales", "Revenue from operations", "Revenue from Operations"])
            
            # 7. COGS
            if is_excel:
                raw_mat = get_val("pnl", ["Raw Material Cost"], exact=True) or 0.0
                change_inv = get_val("pnl", ["Change in Inventory"], exact=True) or 0.0
                cogs = raw_mat - change_inv
            else:
                # Sum of: raw materials consumed, purchases of stock-in-trade, changes in inventories
                rm = get_val("pnl", [r"Cost of.*material.*consumed", r"Cost of raw materials"]) or 0.0
                pur = get_val("pnl", [r"Purchases of stock-in-trade", r"Purchases of Stock-in-Trade"]) or 0.0
                chg = get_val("pnl", [r"Changes in inventor", r"Change.*in.*inventor"]) or 0.0
                cogs = rm + pur + chg
                if cogs == 0.0:
                    cogs = None
                    
            # 8. EBIT (PBT + Interest/Finance costs)
            pbt = get_val("pnl", ["Profit before tax", "Profit Before Tax"])
            interest = get_val("pnl", ["Interest", "Finance Costs", "Finance costs", "Finance Cost"])
            ebit = (pbt + interest) if (pbt is not None and interest is not None) else None
            
            # 9. Net Profit
            np_val = get_val("pnl", ["Net profit", "Net Profit", "Profit for the year", "Profit/loss for the period"])
            
            # 10. Receivables
            if is_excel:
                receivables = get_val("balance_sheet", ["Receivables"], exact=True)
            else:
                # Find current receivables
                receivables = get_val("balance_sheet", [r"Trade receivables\s*\(Current Assets\)", r"Trade Receivables\s*\(Current Assets\)", r"Trade receivables"])
                
            # 11. Depreciation
            depr = get_val("pnl", ["Depreciation", "Depreciation and Amortisation Expense", "Depreciation and amortisation expense"])
            
            # 12. SGA
            if is_excel:
                sga = get_val("pnl", ["Selling and admin"], exact=True)
            else:
                sga = get_val("pnl", ["Other expenses", "Other Expenses"])
                
            # 13. Total Debt
            if is_excel:
                debt = get_val("balance_sheet", ["Borrowings"], exact=True)
            else:
                # Sum of all lease liabilities and borrowings
                debt = get_sum("balance_sheet", r"Lease Liabilities|Borrowings")
                
            # 14. CFO
            cfo = get_val("cashflow", [r"Cash.*Operating.*Activity", r"Net cash.*operating"])

            
            # 15. Net PP&E
            if is_excel:
                ppe = get_val("balance_sheet", ["Net Block"], exact=True)
            else:
                ppe = get_val("balance_sheet", [r"Property, Plant and Equipment\s*\(Non-Current Assets\)", r"Property, plant and equipment\s*\(Non-Current Assets\)", r"Property, plant and equipment"])

            # Calculate derived variables
            # Total Liabilities = Total Assets - Book Value of Equity
            tl = (ta - bve) if (ta is not None and bve is not None) else None
            
            pivoted_rows.append({
                "Company": comp,
                "YearNum": yr,
                "FinancialYear": yr_str,
                "TotalAssets": ta,
                "CurrentAssets": ca,
                "CurrentLiabilities": cl,
                "TotalLiabilities": tl,
                "BookValueOfEquity": bve,
                "RetainedEarnings": retained,
                "Sales": sales,
                "COGS": cogs,
                "EBIT": ebit,
                "NetProfit": np_val,
                "Receivables": receivables,
                "Depreciation": depr,
                "SGA": sga,
                "TotalDebt": debt,
                "CFO": cfo,
                "NetPPE": ppe,
                "liquidity_ratio_confidence": "approximate" if is_excel else "high",
                "cogs_confidence": "approximate" if is_excel else "high"
            })
            
    df_pivot = pd.DataFrame(pivoted_rows)
    df_pivot.sort_values(by=["Company", "YearNum"], inplace=True)
    
    # Calculate Forensic Metrics
    results = []
    for comp in companies:
        comp_df = df_pivot[df_pivot["Company"] == comp].copy()
        
        # Shifted values for index calculations
        comp_df["Prev_Sales"] = comp_df["Sales"].shift(1)
        comp_df["Prev_Receivables"] = comp_df["Receivables"].shift(1)
        comp_df["Prev_COGS"] = comp_df["COGS"].shift(1)
        comp_df["Prev_CurrentAssets"] = comp_df["CurrentAssets"].shift(1)
        comp_df["Prev_NetPPE"] = comp_df["NetPPE"].shift(1)
        comp_df["Prev_TotalAssets"] = comp_df["TotalAssets"].shift(1)
        comp_df["Prev_Depreciation"] = comp_df["Depreciation"].shift(1)
        comp_df["Prev_SGA"] = comp_df["SGA"].shift(1)
        comp_df["Prev_TotalDebt"] = comp_df["TotalDebt"].shift(1)
        
        # Calculate Altman Z'-Score variables
        # Working Capital / Total Assets
        comp_df["X1"] = (comp_df["CurrentAssets"] - comp_df["CurrentLiabilities"]) / comp_df["TotalAssets"]
        # Retained Earnings / Total Assets
        comp_df["X2"] = comp_df["RetainedEarnings"] / comp_df["TotalAssets"]
        # EBIT / Total Assets
        comp_df["X3"] = comp_df["EBIT"] / comp_df["TotalAssets"]
        # Book Value of Equity / Total Liabilities
        comp_df["X4"] = comp_df["BookValueOfEquity"] / comp_df["TotalLiabilities"]
        # Sales / Total Assets
        comp_df["X5"] = comp_df["Sales"] / comp_df["TotalAssets"]
        
        # Altman Z'-Score
        comp_df["Altman_Z_Score"] = 0.717 * comp_df["X1"] + 0.847 * comp_df["X2"] + 3.107 * comp_df["X3"] + 0.420 * comp_df["X4"] + 0.998 * comp_df["X5"]
        
        def z_zone(z):
            if pd.isna(z):
                return "N/A"
            if z > 2.9:
                return "Safe"
            elif z >= 1.23:
                return "Grey"
            else:
                return "Distress"
                
        comp_df["Z_Score_Zone"] = comp_df["Altman_Z_Score"].apply(z_zone)
        
        # Calculate Beneish M-Score variables
        # 1. DSRI
        comp_df["DSRI"] = (comp_df["Receivables"] / comp_df["Sales"]) / (comp_df["Prev_Receivables"] / comp_df["Prev_Sales"])
        
        # 2. GMI
        prev_gm = (comp_df["Prev_Sales"] - comp_df["Prev_COGS"]) / comp_df["Prev_Sales"]
        curr_gm = (comp_df["Sales"] - comp_df["COGS"]) / comp_df["Sales"]
        comp_df["GMI"] = prev_gm / curr_gm
        
        # 3. AQI
        curr_aq = 1.0 - (comp_df["CurrentAssets"] + comp_df["NetPPE"]) / comp_df["TotalAssets"]
        prev_aq = 1.0 - (comp_df["Prev_CurrentAssets"] + comp_df["Prev_NetPPE"]) / comp_df["Prev_TotalAssets"]
        comp_df["AQI"] = curr_aq / prev_aq
        
        # 4. SGI
        comp_df["SGI"] = comp_df["Sales"] / comp_df["Prev_Sales"]
        
        # 5. DEPI
        # Depreciation Rate = Depreciation / (Net PP&E + Depreciation)
        curr_dep_rate = comp_df["Depreciation"] / (comp_df["NetPPE"] + comp_df["Depreciation"])
        prev_dep_rate = comp_df["Prev_Depreciation"] / (comp_df["Prev_NetPPE"] + comp_df["Prev_Depreciation"])
        comp_df["DEPI"] = prev_dep_rate / curr_dep_rate
        
        # 6. SGAI
        comp_df["SGAI"] = (comp_df["SGA"] / comp_df["Sales"]) / (comp_df["Prev_SGA"] / comp_df["Prev_Sales"])
        
        # 7. LVGI
        comp_df["LVGI"] = (comp_df["TotalDebt"] / comp_df["TotalAssets"]) / (comp_df["Prev_TotalDebt"] / comp_df["Prev_TotalAssets"])
        
        # 8. TATA (using NetProfit)
        comp_df["TATA"] = (comp_df["NetProfit"] - comp_df["CFO"]) / comp_df["TotalAssets"]
        
        # Beneish M-Score
        comp_df["Beneish_M_Score"] = (
            -4.84 + 
            0.920 * comp_df["DSRI"] + 
            0.528 * comp_df["GMI"] + 
            0.404 * comp_df["AQI"] + 
            0.892 * comp_df["SGI"] + 
            0.115 * comp_df["DEPI"] - 
            0.172 * comp_df["SGAI"] + 
            4.037 * comp_df["TATA"] + 
            0.0327 * comp_df["LVGI"]
        )
        
        comp_df["Beneish_Red_Flag"] = comp_df["Beneish_M_Score"].apply(lambda m: "Yes" if m > -1.78 else ("No" if pd.notna(m) else "N/A"))
        
        # Key Ratios
        comp_df["Current_Ratio"] = comp_df["CurrentAssets"] / comp_df["CurrentLiabilities"]
        comp_df["Asset_Turnover"] = comp_df["Sales"] / comp_df["TotalAssets"]
        comp_df["Debt_To_Equity"] = comp_df["TotalDebt"] / comp_df["BookValueOfEquity"]
        
        results.append(comp_df)
        
    df_results = pd.concat(results, ignore_index=True)
    
    # Save the output results CSV
    out_cols = [
        "Company", "FinancialYear", 
        "Altman_Z_Score", "Z_Score_Zone", 
        "Beneish_M_Score", "Beneish_Red_Flag",
        "Current_Ratio", "Asset_Turnover", "Debt_To_Equity",
        "liquidity_ratio_confidence", "cogs_confidence"
    ]
    df_results[out_cols].to_csv("extracted/forensic_screening_results.csv", index=False)
    print(f"Saved results to extracted/forensic_screening_results.csv. Total rows: {len(df_results)}")
    
    # Print preview
    print("\n=== Forensic Screening Results Preview ===")
    print(df_results[out_cols].dropna(subset=["Altman_Z_Score"]).head(20).to_string(index=False))

if __name__ == "__main__":
    compute_forensics()
