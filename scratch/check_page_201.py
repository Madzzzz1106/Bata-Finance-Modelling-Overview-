import fitz

doc = fitz.open("Bata_FY25.pdf")
print("--- PAGE 201 ---")
print("\n".join(doc[200].get_text("text").split("\n")[:15]))
