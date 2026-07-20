import fitz

doc = fitz.open("Metro_FY21.pdf")
print("--- PAGE 13 ---")
print(doc[12].get_text("text")[:1000])
