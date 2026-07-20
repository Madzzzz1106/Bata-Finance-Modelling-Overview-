import fitz

doc = fitz.open("Metro_FY21.pdf")
page = doc[98] # page 99
words = page.get_text("words")
# filter words in y range around Total Assets
assets_words = [w for w in words if "total" in w[4].lower() or "assets" in w[4].lower()]
for w in assets_words:
    print(f"Word: '{w[4]}' -> x0={w[0]:.1f}, x1={w[2]:.1f}, y0={w[1]:.1f}")
