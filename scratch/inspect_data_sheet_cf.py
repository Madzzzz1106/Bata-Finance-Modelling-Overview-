import openpyxl

wb = openpyxl.load_workbook("Campus Activewe.xlsx", data_only=True)
ws = wb["Data Sheet"]
print("--- Data Sheet Rows 80 to 93 ---")
for r in range(80, 94):
    row_vals = [ws.cell(row=r, column=c).value for c in range(1, 12)]
    print(f"Row {r}: {row_vals}")
