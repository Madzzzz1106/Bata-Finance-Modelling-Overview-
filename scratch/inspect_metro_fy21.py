import fitz

doc = fitz.open("Metro_FY21.pdf")
print("Total pages:", len(doc))

print("--- PAGE 47 ---")
print("\n".join(doc[46].get_text("text").split("\n")[:15]))

print("\n--- PAGE 48 ---")
print("\n".join(doc[47].get_text("text").split("\n")[:15]))

print("\n--- PAGE 93 ---")
print("\n".join(doc[92].get_text("text").split("\n")[:15]))

print("\n--- PAGE 94 ---")
print("\n".join(doc[93].get_text("text").split("\n")[:15]))
