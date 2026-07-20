import csv

with open('/Users/mridulagarwal/Desktop/BATA/extracted/master_financials.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

bata_rows = [row for row in rows if row['Company'].lower() == 'bata']
bata_years = sorted(list(set(row['FinancialYear'] for row in bata_rows)))
print("Bata years:", bata_years)

metrics = set(row['Metric'] for row in bata_rows)
print("\nBata metrics related to marketing/advertising/other:")
matching_metrics = []
for m in sorted(list(metrics)):
    m_lower = m.lower()
    if any(k in m_lower for k in ['expense', 'advert', 'market', 'public', 'promo', 'sell', 'other', 'distribution', 'commission', 'agent']):
        matching_metrics.append(m)
        print("  ", m)

print("\nDetail of matching rows for Bata:")
for row in bata_rows:
    if row['Metric'] in matching_metrics:
        print(f"Year: {row['FinancialYear']} | Metric: {row['Metric']} | Value: {row['Value']} | Unit: {row['unit']}")
