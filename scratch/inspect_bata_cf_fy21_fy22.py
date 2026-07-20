import fitz

for year, p1, p2 in [("FY21", 152, 202), ("FY22", 132, 184)]:
    doc = fitz.open(f"Bata_{year}.pdf")
    print(f"\n--- Bata {year} Standalone CF (Page {p1}) ---")
    print(doc[p1 - 1].get_text("text")[:200])
    
    print(f"\n--- Bata {year} Consolidated CF (Page {p2}) ---")
    print(doc[p2 - 1].get_text("text")[:200])
