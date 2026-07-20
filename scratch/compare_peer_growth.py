import pandas as pd

df = pd.read_csv("extracted/master_financials.csv")

# We want to extract sales/revenue for Bata, Metro, Relaxo, Campus
target_companies = ["Bata", "Metro", "Relaxo", "Campus Activewear"]
pnl_data = df[(df["Company"].isin(target_companies)) & (df["Statement"] == "pnl") & (df["Metric"].str.contains("sales|revenue", case=False, na=False))]

# Let's inspect the sales figures for each company across years
pivoted = df[df["Statement"] == "pnl"].pivot_table(index="Company", columns="FinancialYear", values="Value", aggfunc="first")

# Let's find specific revenue/sales metric names
sales_metrics = {}
for comp in target_companies:
    comp_df = df[(df["Company"] == comp) & (df["Statement"] == "pnl")]
    # print(comp, comp_df["Metric"].unique())

# Let's write a simple extraction based on the generate_analysis_files logic
rows = []
for comp in target_companies:
    comp_df = df[df["Company"] == comp]
    for yr in ["FY23", "FY24", "FY25"]:
        yr_df = comp_df[comp_df["FinancialYear"] == yr]
        sales = None
        # Try to match sales
        sales_row = yr_df[yr_df["Metric"].str.contains("Revenue from operations|Revenue from Operations|Sales", case=False, na=False)]
        if not sales_row.empty:
            sales = float(sales_row.iloc[0]["Value"])
        rows.append({"Company": comp, "Year": yr, "Sales": sales})

df_sales = pd.DataFrame(rows)
df_sales_pivot = df_sales.pivot(index="Company", columns="Year", values="Sales")
df_sales_pivot["YoY_Growth_FY24"] = ((df_sales_pivot["FY24"] - df_sales_pivot["FY23"]) / df_sales_pivot["FY23"] * 100).round(2)
df_sales_pivot["YoY_Growth_FY25"] = ((df_sales_pivot["FY25"] - df_sales_pivot["FY24"]) / df_sales_pivot["FY24"] * 100).round(2)

print("=== REVENUE (in Millions for P&L source units) ===")
print(df_sales_pivot)
