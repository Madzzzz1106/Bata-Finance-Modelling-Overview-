import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class ExecutivePortraitPDF(FPDF):
    def footer(self):
        # Bottom page number and sources
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7.5)
        self.set_text_color(0, 0, 0)
        
        # Page-specific source in footer
        if self.page_no() == 1:
            footer_text = "Page 1 of 2  |  Sources: McKinsey Problem-Solving Methodology & Minto Pyramid Principles (Page 45-62)"
        else:
            footer_text = "Page 2 of 2  |  Sources: Bata India Annual Report FY25 (P. 194 Balance Sheet, P. 195 P&L, Note 38 Leases, Note 42 Working Capital)"
            
        self.cell(0, 10, footer_text, align="C")

def generate_pdf_report():
    # A4 Portrait: 210mm width x 297mm height
    pdf = ExecutivePortraitPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=False)
    
    # -------------------------------------------------------------
    # PAGE 1: SLIDE 1 (MECE Methodology - Plain English & Detailed)
    # -------------------------------------------------------------
    pdf.add_page()
    
    # Slide Title
    pdf.set_y(15)
    pdf.set_text_color(0, 0, 0)  # Pure Black Text
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "THE MECE ISSUE TREE FRAMEWORK AND PROBLEM SOLVING", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    # Underline
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.6)
    pdf.line(15, 23, 195, 23)
    
    # Text Block (y=25, width=180mm)
    pdf.set_y(25)
    
    # Section 1: Core Concept
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(180, 4, "1. Core Concept and Structuring Parameters (The Drawer Analogy)", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 7.5)
    
    text_logic = [
        "1. Think of MECE as sorting a messy drawer into labeled boxes so that everything is tidy and easy to find.",
        "2. Non-overlapping parts (Mutually Exclusive): No single item can fit into more than one box. If you have one box for socks " +
        "and another for red clothes, a red sock fits in both, causing confusion. In business, grouping by Retail, Online, and " +
        "Wholesale ensures every transaction belongs to exactly one bucket, preventing double-counting of sales.",
        "3. Complete picture (Collectively Exhaustive): Every item must end up in a box with nothing left on the floor. If a few items " +
        "do not fit the main labels, you must create an 'Other' box to keep the collection complete and ensure 100 percent coverage.",
        "4. Minto Rule 1 (Summary): Ideas at any level must summarize the sub-points grouped below them for a top-down logical flow.",
        "5. Minto Rule 2 (Parallelism): Ideas in a group must share the same level of abstraction (do not mix macro trends with tactical tasks).",
        "6. Minto Rule 3 (Ordering): Ideas in a group must follow a logical order (structural/geographical, chronological, or qualitative)."
    ]
    for line in text_logic:
        pdf.set_x(15)
        pdf.multi_cell(180, 2.9, line)
        
    pdf.ln(1)
    
    # Section 2: Working Steps
    pdf.set_x(15)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(180, 4, "2. Four-Stage Working Steps to Construct an Issue Tree", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 7.5)
    
    text_types = [
        "1. Define the core question: Frame a specific, measurable, and time-bound problem statement at the top of the tree.",
        "2. Deconstruct horizontally (Level 1): Break the core question into 2 to 4 major, non-overlapping branches that cover the whole space. " +
        "For example, split profit into Revenue and Costs, or split retail growth into existing store growth and new store openings.",
        "3. Drill down vertically (Level 2 & 3): Breakdown each major branch into specific, actionable leaves that represent root causes.",
        "4. Validate and test logic: Apply the separation test (ensuring branches do not affect each other) and the coverage test " +
        "(ensuring no gaps exist) to finalize the tree structure before gathering client data."
    ]
    for line in text_types:
        pdf.set_x(15)
        pdf.multi_cell(180, 2.9, line)
        
    pdf.ln(1)
    
    # Section 3: Prioritization
    pdf.set_x(15)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(180, 4, "3. Prioritizing Levers (The 80/20 Rule)", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 7.5)
    
    text_prior = [
        "1. The 80/20 Rule: Focus strictly on the 20 percent of drivers that generate 80 percent of the total business value to save client time.",
        "2. Evaluation Matrix: Map deconstructed leaves on a 2x2 grid comparing Financial Impact vs. Feasibility.",
        "3. Impact parameters: Financial margin expansion, working capital cash velocity, and long-term strategic moats.",
        "4. Feasibility parameters: Capital requirement (CapEx), operational complexity, regulatory hurdles, and organizational friction.",
        "5. Quick Wins: High-impact and high-feasibility leaves (like inventory reduction) are prioritized first to release cash."
    ]
    for line in text_prior:
        pdf.set_x(15)
        pdf.multi_cell(180, 2.9, line)
        
    pdf.ln(1)
    
    # Section 4: Sources
    pdf.set_x(15)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(180, 4, "4. Sources for Methodology", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 7.5)
    
    text_sources_p1 = [
        "1. McKinsey and Company standard problem-solving frameworks.",
        "2. The Minto Pyramid Principle by Barbara Minto."
    ]
    for line in text_sources_p1:
        pdf.set_x(15)
        pdf.multi_cell(180, 2.9, line)
        
    # Stacked Images on Page 1 (Vertically Aligned, Centered at x=45, widened to w=120)
    pdf.image("/Users/mridulagarwal/Desktop/BATA/extracted/mece_issue_tree_diagram.png", x=45, y=142, w=120)
    pdf.image("/Users/mridulagarwal/Desktop/BATA/extracted/impact_feasibility_matrix.png", x=45, y=198, w=120)
    
    # -------------------------------------------------------------
    # PAGE 2: SLIDE 2 (Bata India case study & recommendations)
    # -------------------------------------------------------------
    pdf.add_page()
    
    # Slide Title
    pdf.set_y(15)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "BATA INDIA: DIAGNOSTIC CASE STUDY & RECOMMENDATIONS", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    # Underline
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.6)
    pdf.line(15, 23, 195, 23)
    
    # Left Column: Detailed Case Study (y=25, width=180mm)
    pdf.set_y(25)
    
    # Section 1: Bata Company Overview through MECE
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(180, 4, "1. Bata Company Overview Deconstructed via MECE", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 7.5)
    
    text_identify = [
        "1. Revenue Branch: Split into Company-Owned stores (904 stores, capital-heavy, high overhead) vs. Franchise stores (500+ stores, asset-light). " +
        "The deconstruction shows that Company-Owned stores are dragging down efficiency.",
        "2. Capital Employed Branch: Decomposed into Fixed Capital (ROU lease assets of Rs. 1,210.90 Cr, store renovations CapEx of Rs. 337.57 Cr) " +
        "and Working Capital (Inventory of Rs. 829.41 Cr, Receivables of Rs. 111.45 Cr). High fixed lease assets drag down asset turnover to 0.91.",
        "3. Cost Branch: Split into Cost of Goods Sold (43.7% of sales) vs. lease rental liabilities. Raw material inflation in the value segment " +
        "has squeezed margins, while store renovations (Rs. 337.57 Cr CapEx) failed to drive volume growth."
    ]
    for line in text_identify:
        pdf.set_x(15)
        pdf.multi_cell(180, 2.9, line)
        
    pdf.ln(1)
    
    # Section 2: Identifying Bata Issues via MECE
    pdf.set_x(15)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(180, 4, "2. Identifying Bata Issues via MECE Formula Deconstruction", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 7.5)
    
    text_audit = [
        "1. Formula Break: ROCE = Operating Margin x Asset Turnover. By checking each branch against peers, we isolate the problem.",
        "2. Operating Margin Branch: Bata core operating EBITDA (21.1%) lags Metro Brands (30.5%), isolating a premiumization and pricing issue.",
        "3. Asset Turnover Branch: Bata is 0.91x (down from 1.04x). Comparing Rs. 337.57 Cr CapEx against flat +0.3% YoY revenue isolates a " +
        "Fixed Asset Productivity issue (COCO store upgrades failed to drive volume, as consumers purchase sneakers online or from rivals).",
        "4. Working Capital Branch: Inventory days rose to 195 (vs. Relaxo's 177 days), isolating a Working Capital/Inventory velocity issue."
    ]
    for line in text_audit:
        pdf.set_x(15)
        pdf.multi_cell(180, 2.9, line)
        
    pdf.ln(1)
    
    # Section 3: Recommendations
    pdf.set_x(15)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(180, 4, "3. Strategic Recommendations & How They Help", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 7.5)
    
    text_recom = [
        "1. Standalone sneaker stores: Launch dedicated shoe spots to capture casual wear demand. Drives the Revenue/ASP branch.",
        "2. Shift to franchise model: Open new stores through partners in smaller cities. This directly reduces the Capital Employed branch " +
        "by transferring lease liabilities and CapEx, driving Asset Turnover above 1.15.",
        "3. Inventory days reduction (195 to 155): Transition to a demand-pull model to release trapped capital in the Working Capital branch.",
        "4. ROCE & Solvency: Removing heavy store leases from the balance sheet improves return on capital, self-funds expansion, and " +
        "reverses the Altman Z'-Score decline (FY25: 2.14)."
    ]
    for line in text_recom:
        pdf.set_x(15)
        pdf.multi_cell(180, 2.9, line)
        
    pdf.ln(1)
    
    # Section 4: Cash Release Math
    pdf.set_x(15)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(180, 4, "4. Derivation of Working Capital Cash Release", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 7.5)
    
    text_math = [
        "1. Base cash release: Reducing stock days by 40 days releases Rs. 167.10 Cr in cash based on current numbers.",
        "2. Consulting Target: Adjusted for growth and peer metrics, this shift releases Rs. 125.40 Cr in trapped cash by FY27 relative to the status quo, " +
        "funding brand marketing and technology rollouts with zero new debt.",
        "3. Reinvestment: This cash can fund marketing and new franchise stores without taking on any expensive bank loans."
    ]
    for line in text_math:
        pdf.set_x(15)
        pdf.multi_cell(180, 2.9, line)
        
    pdf.ln(1)
    
    # Section 5: Sources
    pdf.set_x(15)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(180, 4, "5. Sources for Case Study Data", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 7.5)
    
    text_sources_p2 = [
        "1. Consolidated Profit and Loss Account and Note 42 (Working Capital) of the Bata India Limited FY25 Annual Report.",
        "2. Peer consolidated databases for Metro Brands, Relaxo Footwear, and Campus Activewear."
    ]
    for line in text_sources_p2:
        pdf.set_x(15)
        pdf.multi_cell(180, 2.9, line)
        
    # Page 2 Images (Stacked at the bottom - y coordinates adjusted upward to prevent page number overlap)
    # Bata Tailored Tree (y=135, w=180, height is 67, goes to 202)
    pdf.image("/Users/mridulagarwal/Desktop/BATA/extracted/bata_issue_tree_diagram.png", x=15, y=135, w=180)
    # Altman Z-Score Chart (y=206, w=85, height is 60, goes to 266)
    pdf.image("/Users/mridulagarwal/Desktop/BATA/extracted/z_score_chart.png", x=15, y=206, w=85)
    # Peer EBITDA margin chart (y=206, w=85, height is 60, goes to 266)
    pdf.image("/Users/mridulagarwal/Desktop/BATA/extracted/peer_ebitda_margin_chart.png", x=105, y=206, w=90)
    
    # Save output PDF
    pdf.output("/Users/mridulagarwal/Desktop/BATA/bata_mece_issue_tree_presentation.pdf")
    print("PDF report successfully compiled at /Users/mridulagarwal/Desktop/BATA/bata_mece_issue_tree_presentation.pdf")

if __name__ == "__main__":
    pdf_file_path = "/Users/mridulagarwal/Desktop/BATA/bata_mece_issue_tree_presentation.pdf"
    if os.path.exists(pdf_file_path):
        try:
            os.remove(pdf_file_path)
        except OSError:
            pass
    generate_pdf_report()
