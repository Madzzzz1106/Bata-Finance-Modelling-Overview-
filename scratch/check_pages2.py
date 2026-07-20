import fitz

doc = fitz.open("Bata_FY25.pdf")
for p in [151, 152, 153, 154, 155, 156]:
    page = doc[p - 1]
    text = page.get_text("text")
    print(f"--- Page {p} ---")
    print("\n".join(text.split("\n")[:15]))
