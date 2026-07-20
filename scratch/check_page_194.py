import fitz

doc = fitz.open("Bata_FY25.pdf")
print("--- PAGE 194 ---")
print("\n".join(doc[193].get_text("text").split("\n")[:15]))
