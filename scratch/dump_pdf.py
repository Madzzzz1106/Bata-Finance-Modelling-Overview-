import fitz

def dump_pdf_to_txt(pdf_path, txt_path):
    doc = fitz.open(pdf_path)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"Total pages: {len(doc)}\n")
        for i, page in enumerate(doc):
            f.write(f"\n--- PAGE {i+1} ---\n")
            text = page.get_text()
            f.write(text)
            f.write("\n")
    print(f"Dumped PDF to {txt_path}")

if __name__ == "__main__":
    dump_pdf_to_txt("Bata Overview.pdf", "scratch/bata_complete_overview_text.txt")
