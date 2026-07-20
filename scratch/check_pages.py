import fitz

doc = fitz.open("Bata_FY25.pdf")
print("Total pages:", len(doc))

# Let's inspect pages from 130 to 170 to check where the Standalone financial statements actually are.
for page_num in range(130, 170):
    page = doc[page_num - 1]
    text = page.get_text("text")
    lines = [line.strip() for line in text.split("\n") if line.strip()][:5]
    print(f"Page {page_num}: {lines}")
