import fitz

doc = fitz.open("Metro_FY24.pdf")
for p in [107, 108, 109, 110, 111, 112]:
    print(f"--- Page {p} ---")
    text = doc[p - 1].get_text("text")
    print("\n".join(text.split("\n")[:10]))
