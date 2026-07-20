import fitz

doc = fitz.open("Bata_FY25.pdf")
print("--- PAGE 200 ---")
print("\n".join(doc[199].get_text("text").split("\n")[:15]))
