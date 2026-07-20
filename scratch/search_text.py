import fitz

doc = fitz.open("Bata_FY25.pdf")
print("Searching for 'Management Discussion'")
for p in range(len(doc)):
    text = doc[p].get_text("text").lower()
    if "management discussion" in text:
        print(f"Page {p+1} contains 'management discussion'")
