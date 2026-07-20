import pandas as pd

# Historical Data
fy25_rev = 3488.79
fy25_ebitda_operating = 3488.79 * 0.211  # 21.1% operating EBITDA
fy25_pat_operating = 3488.79 * 0.056      # ~5.6% operating Net Margin (excluding land sale gain of 134 Cr)
fy25_inventory_days = 195
fy25_asset_turnover = 0.91

# Projections under Scenario A: Status Quo
# Assuming flat/sluggish growth of 1.5% YoY, stagnant margins at 21%, inventory at 195 days, asset turnover declining due to continuous capex
status_quo = []
current_rev = fy25_rev
for year in ['FY26', 'FY27', 'FY28']:
    current_rev = current_rev * 1.015
    ebitda = current_rev * 0.211
    pat = current_rev * 0.058
    inv_days = 195
    asset_turnover = 0.88 if year == 'FY26' else (0.85 if year == 'FY27' else 0.82)
    status_quo.append({
        'Year': year,
        'Revenue': round(current_rev, 2),
        'EBITDA': round(ebitda, 2),
        'EBITDA_Margin': '21.10%',
        'PAT': round(pat, 2),
        'PAT_Margin': '5.80%',
        'Inventory_Days': inv_days,
        'Asset_Turnover': asset_turnover
    })

# Projections under Scenario B: Strategic Shift (Our Recommendations)
# Assuming 4% growth in FY26, 6% in FY27, 8% in FY28. 
# Margins expanding to 22.5% in FY26, 24.5% in FY27, 25.5% in FY28.
# Inventory days dropping to 175, 155, 145.
# Asset turnover recovering to 1.05, 1.15, 1.25.
strategic_shift = []
current_rev = fy25_rev
growth_rates = {'FY26': 0.04, 'FY27': 0.06, 'FY28': 0.08}
ebitda_margins = {'FY26': 0.225, 'FY27': 0.245, 'FY28': 0.255}
pat_margins = {'FY26': 0.065, 'FY27': 0.080, 'FY28': 0.095}
inventory_targets = {'FY26': 175, 'FY27': 155, 'FY28': 145}
asset_turnovers = {'FY26': 1.05, 'FY27': 1.15, 'FY28': 1.25}

for year in ['FY26', 'FY27', 'FY28']:
    current_rev = current_rev * (1 + growth_rates[year])
    ebitda = current_rev * ebitda_margins[year]
    pat = current_rev * pat_margins[year]
    strategic_shift.append({
        'Year': year,
        'Revenue': round(current_rev, 2),
        'EBITDA': round(ebitda, 2),
        'EBITDA_Margin': f"{ebitda_margins[year]*100:.2f}%",
        'PAT': round(pat, 2),
        'PAT_Margin': f"{pat_margins[year]*100:.2f}%",
        'Inventory_Days': inventory_targets[year],
        'Asset_Turnover': asset_turnovers[year]
    })

# Working Capital Cash Release Calculation (Strategic Shift)
# Inventory = (Inventory Days / 365) * COGS
# Let's approximate COGS as 43.7% of Revenue (based on 56.3% Gross Margin in FY25)
cogs_pct = 0.437
fy25_inventory = (195 / 365) * (fy25_rev * cogs_pct)
fy26_inventory = (175 / 365) * (strategic_shift[0]['Revenue'] * cogs_pct)
fy27_inventory = (155 / 365) * (strategic_shift[1]['Revenue'] * cogs_pct)
fy28_inventory = (145 / 365) * (strategic_shift[2]['Revenue'] * cogs_pct)

print("----- STATUS QUO PROJECTIONS -----")
print(pd.DataFrame(status_quo))
print("\n----- STRATEGIC SHIFT PROJECTIONS -----")
print(pd.DataFrame(strategic_shift))

print(f"\nFY25 Est. Inventory Value: {fy25_inventory:.2f} Cr")
print(f"FY26 Est. Inventory Value: {fy26_inventory:.2f} Cr")
print(f"FY27 Est. Inventory Value: {fy27_inventory:.2f} Cr")
print(f"FY28 Est. Inventory Value: {fy28_inventory:.2f} Cr")

# Cash released is difference between status quo inventory and strategic shift inventory
sq_fy26_inv = (195 / 365) * (status_quo[0]['Revenue'] * cogs_pct)
sq_fy27_inv = (195 / 365) * (status_quo[1]['Revenue'] * cogs_pct)
sq_fy28_inv = (195 / 365) * (status_quo[2]['Revenue'] * cogs_pct)

print(f"\nWorking Capital Cash Release in FY26 (vs Status Quo): {sq_fy26_inv - fy26_inventory:.2f} Cr")
print(f"Working Capital Cash Release in FY27 (vs Status Quo): {sq_fy27_inv - fy27_inventory:.2f} Cr")
print(f"Working Capital Cash Release in FY28 (vs Status Quo): {sq_fy28_inv - fy28_inventory:.2f} Cr")
