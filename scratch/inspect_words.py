import fitz

doc = fitz.open("Bata_FY25.pdf")
page = doc[221] # page 222
words = page.get_text("words")
# filter words in y range of Revenue from operations (around y=135)
revenue_words = [w for w in words if 130 < w[1] < 140]
for w in revenue_words:
    print(f"Word: '{w[4]}' -> x0={w[0]:.1f}, y0={w[1]:.1f}, x1={w[2]:.1f}, y1={w[3]:.1f}")
