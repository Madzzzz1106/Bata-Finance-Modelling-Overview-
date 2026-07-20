import csv

with open('/Users/mridulagarwal/Desktop/BATA/extracted/master_financials.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

bata_rows = [row for row in rows if row['Company'].lower() == 'bata' and row['Statement'].lower() == 'pnl']

print("Bata P&L Revenue metrics:")
for row in bata_rows:
    if "revenue from operations" in row['Metric'].lower() or "sales" in row['Metric'].lower() or "total income" in row['Metric'].lower():
        print(f"Year: {row['FinancialYear']} | Metric: {row['Metric']} | Value: {row['Value']} | Unit: {row['unit']} | Type: {row['statement_type']}")
