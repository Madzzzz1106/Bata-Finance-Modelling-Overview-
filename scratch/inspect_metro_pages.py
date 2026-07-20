import fitz

doc = fitz.open("Metro_FY21.pdf")
print("Total pages:", len(doc))

# Standalone pages
for p in range(50, 65):
    text = doc[p].get_text("text").strip()
    first_lines = [l.strip() for l in text.split("\n") if l.strip()][:3]
    print(f"Page {p+1}: {first_lines}")
    
# Consolidated pages
print("\n--- CONSOLIDATED ---")
for p in range(95, 115):
    text = doc[p].get_text("text").strip()
    first_lines = [l.strip() for l in text.split("\n") if l.strip()][:3]
    print(f"Page {p+1}: {first_lines}")
