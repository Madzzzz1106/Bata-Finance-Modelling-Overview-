import fitz

doc = fitz.open("Metro_FY21.pdf")
print("--- PAGE 28 ---")
print(doc[27].get_text("text")[:1000])
