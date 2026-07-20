import fitz

doc = fitz.open("Bata Overview.pdf")
print("--- Page 23 text blocks ---")
page_23 = doc[22]
for b in page_23.get_text("blocks"):
    print(b[4].strip())
