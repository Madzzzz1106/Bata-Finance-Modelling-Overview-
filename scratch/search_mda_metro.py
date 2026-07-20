import fitz

doc = fitz.open("Metro_FY21.pdf")
print("Searching for 'discussion' or 'management' in Metro_FY21.pdf...")
for p in range(len(doc)):
    text = doc[p].get_text("text").lower()
    if "discussion" in text or "mda" in text:
        print(f"Page {p+1} contains 'discussion'")
