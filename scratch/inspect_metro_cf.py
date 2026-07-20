import fitz

doc = fitz.open("Metro_FY21.pdf")
for p in [56, 58]:
    print(f"--- Page {p} ---")
    text = doc[p - 1].get_text("text")
    print(text[:300])
