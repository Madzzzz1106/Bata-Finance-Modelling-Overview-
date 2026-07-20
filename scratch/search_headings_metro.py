import fitz

doc = fitz.open("Metro_FY21.pdf")
print("Scanning lines in Metro_FY21.pdf...")
for p in range(14, 46):
    text = doc[p].get_text("text")
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    # Print lines that look like headers (uppercase, short, or start with numbers)
    headers = [l for l in lines[:10] if l.isupper() or "annexure" in l.lower() or "report" in l.lower()]
    print(f"Page {p+1} headers: {headers}")
