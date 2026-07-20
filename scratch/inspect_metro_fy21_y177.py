import fitz

doc = fitz.open("Metro_FY21.pdf")
page = doc[98] # page 99
words = page.get_text("words")
lines_words = [w for w in words if 135 < w[1] < 155]
lines_words.sort(key=lambda w: (w[1], w[0]))
for w in lines_words:
    print(f"Word: '{w[4]}' -> x0={w[0]:.1f}, x1={w[2]:.1f}, y0={w[1]:.1f}")
