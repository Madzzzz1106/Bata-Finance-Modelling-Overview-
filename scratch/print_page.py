import fitz

doc = fitz.open("Bata_FY25.pdf")
print("--- PAGE 47 ---")
print(doc[46].get_text("text"))
print("--- PAGE 48 ---")
print(doc[47].get_text("text"))
