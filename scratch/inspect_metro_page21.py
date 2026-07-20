import fitz

doc = fitz.open("Metro_FY21.pdf")
print("--- PAGE 21 ---")
print(doc[20].get_text("text")[:1000])
