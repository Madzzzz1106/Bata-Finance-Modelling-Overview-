import fitz

doc = fitz.open("Bata_FY25.pdf")
print("Searching for Notes details in Standalone section (pages 156 to 209)...")
for p in range(155, 209):
    text = doc[p].get_text("text").lower()
    if "related party" in text:
        print(f"Page {p+1} contains 'related party'")
    if "contingent liabilit" in text:
        print(f"Page {p+1} contains 'contingent liabilit'")
