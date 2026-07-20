import fitz

doc = fitz.open("Metro_FY25.pdf")
page = doc[116] # page 117
words = page.get_text("words")
# filter words in y range around 180 (corresponding to line 9)
line9_words = [w for w in words if 175 < w[1] < 185]
# sort by x0
line9_words.sort(key=lambda w: w[0])
for w in line9_words:
    print(f"Word: '{w[4]}' -> x0={w[0]:.1f}, x1={w[2]:.1f}, y0={w[1]:.1f}")
