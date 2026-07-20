import openpyxl

wb = openpyxl.load_workbook("Campus Activewe.xlsx", data_only=True)
ws = wb["Profit & Loss"]
print(f"Profit & Loss dimensions: {ws.dimensions}")
# Print first 15 rows and first 10 columns
for r in range(1, 16):
    row_vals = [ws.cell(row=r, column=c).value for c in range(1, 15)]
    print(f"Row {r}: {row_vals}")
