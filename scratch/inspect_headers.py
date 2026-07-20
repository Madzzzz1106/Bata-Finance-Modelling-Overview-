import fitz

doc = fitz.open("Bata_FY25.pdf")
page = doc[221] # page 222
words = page.get_text("words")
header_words = [w for w in words if 110 < w[1] < 128]
for w in header_words:
    print(f"Word: '{w[4]}' -> x0={w[0]:.1f}, y0={w[1]:.1f}, x1={w[2]:.1f}, y1={w[3]:.1f}")
