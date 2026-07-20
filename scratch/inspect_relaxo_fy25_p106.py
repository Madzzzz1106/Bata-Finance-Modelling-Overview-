import fitz

doc = fitz.open("Relaxo_FY25.pdf")
print("--- PAGE 106 ---")
print(doc[105].get_text("text")[:500])

print("\n--- PAGE 107 ---")
print(doc[106].get_text("text")[:500])

print("\n--- PAGE 108 ---")
print(doc[107].get_text("text")[:500])
