import fitz

doc = fitz.open("Metro_FY21.pdf")
print("--- PAGE 29 ---")
print(doc[28].get_text("text")[:1000])
