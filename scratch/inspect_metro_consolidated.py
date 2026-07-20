import fitz

doc = fitz.open("Metro_FY21.pdf")
for p in [99, 100, 101, 102]:
    print(f"--- Page {p} ---")
    text = doc[p - 1].get_text("text")
    print("\n".join(text.split("\n")[:12]))
