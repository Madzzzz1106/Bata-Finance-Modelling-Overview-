import fitz

doc = fitz.open("Bata_FY25.pdf")
print("--- PAGE 193 ---")
print(doc[192].get_text("text"))
