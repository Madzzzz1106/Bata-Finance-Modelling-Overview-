import fitz

doc = fitz.open("Bata_FY25.pdf")
for p in range(210, 230):
    page = doc[p - 1]
    text = page.get_text("text")
    lines = [line.strip() for line in text.split("\n") if line.strip()][:5]
    print(f"Page {p}: {lines}")
