import fitz

doc = fitz.open("Metro_FY24.pdf")
print("--- PAGE 109 ---")
print(doc[108].get_text("text"))
