import pandas as pd

df = pd.read_csv("extracted/master_financials.csv")
bata = df[df["Company"] == "Bata"]

cash_equivalents = bata[bata["Metric"].str.contains("Cash and cash equivalents", case=False, na=False)]
bank_balances = bata[bata["Metric"].str.contains("Bank balances other than", case=False, na=False)]

print("=== Cash and Cash Equivalents ===")
print(cash_equivalents[["FinancialYear", "Value"]])

print("\n=== Bank Balances other than above ===")
print(bank_balances[["FinancialYear", "Value"]])
