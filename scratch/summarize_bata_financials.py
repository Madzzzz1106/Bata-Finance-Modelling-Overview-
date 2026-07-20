import pandas as pd
import glob
import os

results = []

for year in ["FY21", "FY22", "FY23", "FY24", "FY25"]:
    pnl_path = f"extracted/Bata_{year}_pnl.csv"
    bs_path = f"extracted/Bata_{year}_balance_sheet.csv"
    
    if not os.path.exists(pnl_path) or not os.path.exists(bs_path):
        print(f"Missing {year}")
        continue
        
    pnl = pd.read_csv(pnl_path)
    bs = pd.read_csv(bs_path)
    
    # We need to find the values. In P&L, they are usually under 'CurrentYear' or similar.
    # Let's inspect the columns
    pnl_cols = pnl.columns
    bs_cols = bs.columns
    
    # Clean string helper
    def clean_str(s):
        return str(s).strip().lower().replace(" ", "").replace(",", "").replace("-", "")
        
    # Get P&L value
    def get_pnl_val(keywords):
        for idx, row in pnl.iterrows():
            part = clean_str(row.iloc[0])
            for kw in keywords:
                if clean_str(kw) in part:
                    # Return current year value
                    try:
                        return float(row['CurrentYear'])
                    except:
                        try:
                            return float(row.iloc[2])
                        except:
                            return None
        return None

    # Get Balance Sheet value
    def get_bs_val(keywords):
        for idx, row in bs.iterrows():
            part = clean_str(row.iloc[0])
            for kw in keywords:
                if clean_str(kw) in part:
                    try:
                        return float(row['CurrentYear'])
                    except:
                        try:
                            return float(row.iloc[2])
                        except:
                            return None
        return None

    # Let's find specific numbers
    # Revenue: "Revenue from operations" or "Revenue from Operations"
    revenue = get_pnl_val(["Revenuefromoperations", "RevenuefromOperations"])
    
    # Net Profit: "Profit for the year" or "Profit/loss for the period" or "Net profit"
    net_profit = get_pnl_val(["Profitfortheyear", "Netprofit", "Profitaftertaxfortheyear"])
    
    # Cash: "Cash and cash equivalents"
    cash_eq = get_bs_val(["Cashandcashequivalents"]) or 0.0
    # Bank balances: "Bank balances other than" or "Other bank balances"
    bank_bal = get_bs_val(["Bankbalancesotherthan", "Otherbankbalances"]) or 0.0
    total_cash_bank = cash_eq + bank_bal
    
    # Borrowings: Look for Long-term borrowings, Short-term borrowings
    lt_borrowings = get_bs_val(["Longtermborrowings", "Borrowings(Non-Current)"]) or 0.0
    st_borrowings = get_bs_val(["Shorttermborrowings", "Borrowings(Current)"]) or 0.0
    total_debt = lt_borrowings + st_borrowings
    
    # Inventories
    inventories = get_bs_val(["Inventories", "Inventory"])
    
    # Total Assets
    total_assets = get_bs_val(["Totalassets"])
    
    # Let's print raw values
    print(f"\n{year}:")
    print(f"  Revenue: {revenue}")
    print(f"  Net Profit: {net_profit}")
    print(f"  Cash & Eq: {cash_eq} | Bank Bal: {bank_bal} | Total Cash & Bank: {total_cash_bank}")
    print(f"  LT Borrowings: {lt_borrowings} | ST Borrowings: {st_borrowings} | Total Debt: {total_debt}")
    print(f"  Inventories: {inventories}")
    print(f"  Total Assets: {total_assets}")
    
    results.append({
        "Year": year,
        "Revenue": revenue,
        "NetProfit": net_profit,
        "TotalCashBank": total_cash_bank,
        "TotalDebt": total_debt,
        "Inventories": inventories,
        "TotalAssets": total_assets
    })

df_res = pd.DataFrame(results)
print("\n=== SUMMARY TABLE ===")
print(df_res)
