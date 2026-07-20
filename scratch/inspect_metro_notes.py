import fitz

doc = fitz.open("Metro_FY21.pdf")
for p in [76, 123]:
    print(f"--- Page {p} ---")
    text = doc[p - 1].get_text("text")
    print(text[:300])
