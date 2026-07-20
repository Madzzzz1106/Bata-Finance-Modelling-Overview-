import fitz

doc = fitz.open("Bata_FY25.pdf")
print("--- PAGE 193 ---")
print("\n".join(doc[192].get_text("text").split("\n")[:15]))

print("\n--- PAGE 195 ---")
print("\n".join(doc[194].get_text("text").split("\n")[:15]))
