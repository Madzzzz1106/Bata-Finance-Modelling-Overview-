import fitz

doc = fitz.open("Bata_FY25.pdf")
text = doc[194].get_text("text").lower()
print("related party disclosures in text:", "related party disclosures" in text)
print("names of related parties in text:", "names of related parties" in text)
print("text is:")
print(text[:200])
