import fitz

doc = fitz.open("Relaxo_FY25.pdf")
for p in [121, 122, 123, 124, 125]:
    print(f"--- Page {p} ---")
    text = doc[p - 1].get_text("text")
    print("\n".join(text.split("\n")[:10]))
