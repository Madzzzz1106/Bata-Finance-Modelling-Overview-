import fitz

doc = fitz.open("Bata Overview.pdf")
print("Number of pages:", len(doc))

# Let's inspect page 30 text blocks
print("\n--- Page 30 text blocks ---")
page_30 = doc[29] # 0-indexed
for b in page_30.get_text("blocks"):
    print(b[4].strip())

print("\n--- Page 13 text blocks ---")
page_13 = doc[12]
for b in page_13.get_text("blocks"):
    print(b[4].strip())
