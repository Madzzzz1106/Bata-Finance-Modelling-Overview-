import fitz

doc = fitz.open("Metro_FY21.pdf")
page = doc[98] # page 99
words = page.get_text("words")
header_words = [w for w in words if 100 < w[1] < 135]
header_words.sort(key=lambda w: (w[1], w[0]))
for w in header_words:
    print(f"Word: '{w[4]}' -> x0={w[0]:.1f}, x1={w[2]:.1f}, y0={w[1]:.1f}")
