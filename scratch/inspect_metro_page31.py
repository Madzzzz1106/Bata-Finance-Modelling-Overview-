import fitz

doc = fitz.open("Metro_FY21.pdf")
print("--- PAGE 31 ---")
print(doc[30].get_text("text"))
