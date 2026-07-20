import fitz

doc = fitz.open("Metro_FY21.pdf")
print("Searching for 'related party' in Metro_FY21.pdf...")
for p in range(len(doc)):
    text = doc[p].get_text("text").lower()
    if "related party disclosures" in text or "related party transactions" in text or "names of related parties" in text:
        print(f"Page {p+1} contains Related Party keywords")
