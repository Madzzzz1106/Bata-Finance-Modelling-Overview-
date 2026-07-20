import fitz

doc = fitz.open("Bata_FY25.pdf")
page = doc[220] # page 221
blocks = page.get_text("blocks")
# Sort blocks by y0 (top to bottom), then x0 (left to right)
blocks.sort(key=lambda b: (b[1], b[0]))
for b in blocks:
    x0, y0, x1, y1, text, block_no, block_type = b
    text_clean = text.replace('\n', ' | ').strip()
    print(f"Block {block_no} ({x0:.1f}, {y0:.1f}) -> ({x1:.1f}, {y1:.1f}): {text_clean}")
