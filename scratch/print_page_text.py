import fitz

doc = fitz.open("Bata_FY25.pdf")
print("--- Page 221 Text ---")
print(doc[220].get_text("text"))

print("\n--- Page 222 Text ---")
print(doc[221].get_text("text"))
