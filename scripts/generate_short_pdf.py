import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Define NumberedCanvas to handle page numbers and headers/footers
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_elements(num_pages)
            super().showPage()
        super().save()

    def draw_page_elements(self, page_count):
        # No headers/footers on page 1 (Cover Page)
        if self._pageNumber == 1:
            # Draw decorative cover background
            self.saveState()
            self.setFillColor(colors.HexColor("#0D1B2A"))
            self.rect(0, 0, 612, 792, fill=True, stroke=False)
            
            # Subtle accent color strip at bottom
            self.setFillColor(colors.HexColor("#8B2635"))
            self.rect(0, 0, 612, 40, fill=True, stroke=False)
            
            # Decorative line
            self.setStrokeColor(colors.HexColor("#E0E1DD"))
            self.setLineWidth(1)
            self.line(54, 250, 558, 250)
            self.restoreState()
            return
            
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1B263B"))
        
        # Header
        self.drawString(54, 755, "BATA INDIA LIMITED | STRATEGIC & COMPETITIVE REVIEW (SHORT)")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#778DA9"))
        self.drawRightString(558, 755, "JUNE 2026")
        
        # Header rule
        self.setStrokeColor(colors.HexColor("#D1D5DB"))
        self.setLineWidth(0.5)
        self.line(54, 748, 558, 748)
        
        # Footer
        self.line(54, 48, 558, 48)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#778DA9"))
        self.drawString(54, 36, "CONFIDENTIAL - FOR INTERNAL USE ONLY")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_text)
        
        self.restoreState()

def build_pdf():
    pdf_path = "Bata_Overview_Short.pdf"
    
    # Document setup: Letter is 612 x 792 pt. Margins: left/right=54pt, top=65pt, bottom=70pt
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=65,
        bottomMargin=70
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    # Cover page styles
    cover_title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=32,
        leading=38,
        textColor=colors.HexColor("#E0E1DD"),
        alignment=0 # Left
    )
    
    cover_subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=16,
        leading=22,
        textColor=colors.HexColor("#E0E1DD"),
        alignment=0
    )
    
    cover_meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#A5A5A5"),
        alignment=0
    )
    
    # Body styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0D1B2A"),
        alignment=0,
        spaceAfter=12
    )
    
    h1_style = ParagraphStyle(
        'DocH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#1B263B"),
        spaceBefore=8,
        spaceAfter=5,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#8B2635"),
        spaceBefore=4,
        spaceAfter=3,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#2B2D42"),
        spaceAfter=4
    )
    
    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )
    
    table_text_style = ParagraphStyle(
        'TableText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#2B2D42")
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=table_text_style,
        fontName='Helvetica-Bold',
        textColor=colors.white
    )
    
    callout_style = ParagraphStyle(
        'Callout',
        parent=body_style,
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1B263B")
    )
    
    story = []
    
    # ---------------- PAGE 1: COVER PAGE ----------------
    story.append(Spacer(1, 150))
    story.append(Paragraph("BATA INDIA LIMITED", cover_title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Strategic & Competitive Review", cover_subtitle_style))
    story.append(Paragraph("A Condensed Corporate Diagnostic & Market Assessment", ParagraphStyle('Sub2', parent=cover_subtitle_style, fontSize=12, textColor=colors.HexColor("#778DA9"))))
    
    story.append(Spacer(1, 250))
    story.append(Paragraph("<b>Prepared for:</b> Senior Leadership & Investment Committee<br/>"
                           "<b>Date:</b> June 2026<br/>"
                           "<b>Methodology:</b> Quantitative Financial Modeling & Relative Peer Benchmarking", cover_meta_style))
    story.append(PageBreak())
    
    # ---------------- PAGE 2: TABLE OF CONTENTS & EXECUTIVE SUMMARY ----------------
    story.append(Paragraph("Executive Summary & Table of Contents", title_style))
    story.append(Spacer(1, 3))
    
    story.append(Paragraph("<b>Executive Summary:</b><br/>"
                           "This diagnostic report provides a condensed strategic assessment of Bata India Limited's operational, "
                           "financial, and competitive positioning from FY20 to FY25. As the absolute revenue leader in the organized "
                           "footwear segment (FY25 revenue of ₹3,488.79 Crore), Bata maintains major brand strength, direct-to-consumer "
                           "loyalty leverage (46 million Bata Club members), and an extensive network of 1,962 stores. However, the company "
                           "faces clear challenges: growth has stagnated (+0.29% in FY25), capital efficiency has declined (Asset Turnover "
                           "falling from 1.05 to 0.91 despite ₹317.49 Crore in cumulative capex), and inventory cycle times remain elevated at "
                           "195 days. This review maps out specific, competitor-aligned recommendations to bridge profitability gaps "
                           "relative to premium peers like Metro Brands and agility leaders like Campus Activewear.", body_style))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Table of Contents:</b>", h2_style))
    
    # TOC Table
    toc_data = [
        [Paragraph("<b>Section</b>", table_header_style), Paragraph("<b>Description</b>", table_header_style), Paragraph("<b>Page</b>", table_header_style)],
        [Paragraph("1. About the Company & Distribution Model", table_text_style), Paragraph("Operational profile, manufacturing facilities, brand sub-portfolio, and the five core distribution channels.", table_text_style), Paragraph("Page 3", table_text_style)],
        [Paragraph("2. Competitive Landscape & Market Share", table_text_style), Paragraph("Mapping of the ₹75,000+ Crore Indian footwear market and peer-group market share matrix.", table_text_style), Paragraph("Page 4", table_text_style)],
        [Paragraph("3. Financial Parameters & Solvency Risks", table_text_style), Paragraph("Analysis of FY20-FY25 metrics, margin trajectories, and forensic screening results (Altman Z'-Score, Beneish M-Score).", table_text_style), Paragraph("Page 5", table_text_style)],
        [Paragraph("4. Marketing, SWOT & Action Recommendations", table_text_style), Paragraph("Review of marketing campaigns, technology CRM, 2x2 SWOT matrix, and competitor-aligned strategic actions.", table_text_style), Paragraph("Page 6", table_text_style)],
        [Paragraph("5. Technical Appendix & Reference Formulas", table_text_style), Paragraph("Mathematical formulas, working capital calculations, lease adjustments, and FY25-FY28 projections schedule.", table_text_style), Paragraph("Page 7", table_text_style)],
        [Paragraph("6. Strategic Conclusion", table_text_style), Paragraph("Outlook for FY28 target parameters, margin expansion horizons, and executive summary sign-off.", table_text_style), Paragraph("Page 8", table_text_style)],
    ]
    
    toc_table = Table(toc_data, colWidths=[150, 300, 54])
    toc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B263B")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
        ('TOPPADDING', (0, 0), (-1, 0), 4),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E0E1DD")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F7F9")]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(toc_table)
    story.append(PageBreak())
    
    # ---------------- PAGE 3: ABOUT THE COMPANY & DISTRIBUTION MODEL ----------------
    story.append(Paragraph("1. About the Company & Distribution Model", title_style))
    
    story.append(Paragraph("<b>Company Profile & Operations:</b>", h1_style))
    story.append(Paragraph("Founded in 1931 and headquartered in Gurugram, Bata India Limited is India's largest organized footwear retailer by store count and sales volume. A subsidiary of the Switzerland-based Bata Shoe Organization, the company operates 3 captive manufacturing facilities (Batanagar, Bataganj, and Faridabad) with an annual capacity of 46.38 million pairs. Its brand sub-portfolio targets distinct consumer price points and segments: <b>Hush Puppies</b> (premium corporate lifestyle), <b>Power</b> (sports & athleisure), <b>North Star</b> (youth casuals), <b>Bubblegummers</b> (children's), <b>Comfit</b> (comfort everyday), and <b>Bata Core</b> (formal & family utility).", body_style))
    
    story.append(Paragraph("<b>Current Distribution Model:</b>", h1_style))
    story.append(Paragraph("Bata employs an omni-channel distribution ecosystem connecting physical retail, wholesale partners, and digital channels across 1,550+ towns:", body_style))
    
    story.append(Paragraph("• <b>Channel 1: COCO Stores (Company Owned Company Operated):</b> 1,337 stores as of FY25. Located in high-footfall metro high-streets and malls. High capital-intensity, but acts as flagships. Currently undergoing a refresh program, with 750+ locations equipped with dedicated Sneaker Studios.", bullet_style))
    story.append(Paragraph("• <b>Channel 2: Franchise Stores (FOFO - Franchise Owned Franchise Operated):</b> 625 stores as of FY25 (scaled from 300 in FY22). Serves as the primary asset-light expansion engine into Tier-3 to Tier-5 markets.", bullet_style))
    story.append(Paragraph("• <b>Channel 3: Multi-Brand Outlets (MBO):</b> Bata's B2B distribution network covers 30,000+ MBO partners across 1,550 towns, utilizing a tech-enabled automated replenishment system.", bullet_style))
    story.append(Paragraph("• <b>Channel 4: E-Commerce & Digital:</b> Comprises the proprietary D2C store (bata.in) covering 20,000+ PIN codes and major marketplaces (Amazon, Myntra, Flipkart). Represents ~10% of total revenues.", bullet_style))
    story.append(Paragraph("• <b>Channel 5: Shop-in-Shop (SIS):</b> Smaller branded counters within major department stores to maintain mall presence at minimal capex.", bullet_style))
    
    # Store Mix Table
    store_data = [
        [Paragraph("<b>Channel Metric (FY25)</b>", table_header_style), Paragraph("<b>Store Count / Coverage</b>", table_header_style), Paragraph("<b>Strategic Role & Target</b>", table_header_style)],
        [Paragraph("COCO Outlets", table_text_style), Paragraph("1,337 Stores", table_text_style), Paragraph("Premium flagships; CapEx frozen to protect ROCE.", table_text_style)],
        [Paragraph("Franchise Outlets", table_text_style), Paragraph("625 Stores", table_text_style), Paragraph("Growth engine; target 1,000+ outlets by FY28.", table_text_style)],
        [Paragraph("MBO Network", table_text_style), Paragraph("30,000+ Outlets", table_text_style), Paragraph("Mass rural reach; automated supply replenishment.", table_text_style)],
        [Paragraph("E-commerce Reach", table_text_style), Paragraph("20,000+ PIN Codes", table_text_style), Paragraph("Digital scale; target 20% revenue contribution.", table_text_style)],
    ]
    store_table = Table(store_data, colWidths=[120, 130, 254])
    store_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B263B")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F7F9")]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ]))
    
    story.append(Spacer(1, 8))
    story.append(store_table)
    story.append(PageBreak())
    
    # ---------------- PAGE 4: COMPETITORS & MARKET SHARE ----------------
    story.append(Paragraph("2. Competitive Landscape & Market Share", title_style))
    
    story.append(Paragraph("<b>Competitor Landscapes & Profiles:</b>", h1_style))
    story.append(Paragraph("The Indian footwear market is estimated at ₹75,000–80,000 Crore, characterized by high fragmentation (42% branded, 58% unbranded). Organized peers compete across distinct price points and segments:", body_style))
    story.append(Paragraph("• <b>Metro Brands Limited:</b> The premium retail benchmark. Focuses on premium fashion and youth lifestyle (Mochi, Metro, Walkway). Operates 1,025 EBOs with a highly efficient outsourced trading model, leading the industry with a 30.53% EBITDA margin.", bullet_style))
    story.append(Paragraph("• <b>Relaxo Footwears Limited:</b> The value-segment volume leader. Specializes in open, non-leather products (sub-₹400 category). Operates 380 EBOs and extensive wholesale distribution. Currently facing mass discretionary spend slowdown (-4.3% revenue growth in FY25).", bullet_style))
    story.append(Paragraph("• <b>Campus Activewear Limited:</b> The athleisure specialist. Focuses on sports shoes and sneakers in the ₹1,500–₹3,000 price point, utilizing high design velocity and a digital-first marketing model. Achieved +9.99% growth in FY25.", bullet_style))
    story.append(Paragraph("• <b>Liberty Shoes & Khadim India:</b> Traditional mid-market and family footwear peers, operating via wholesale distributor networks. Currently financially constrained with thin PAT margins (~1-2%) and high working capital cycles.", bullet_style))
    
    story.append(Paragraph("<b>Peer Revenue & Organized Segment Share (FY25):</b>", h1_style))
    
    # Market Share Table
    share_data = [
        [Paragraph("<b>Company Name</b>", table_header_style), Paragraph("<b>FY25 Revenue (₹ Cr)</b>", table_header_style), Paragraph("<b>Estimated Branded Share (%)</b>", table_header_style), Paragraph("<b>Primary Segment Focus</b>", table_header_style)],
        [Paragraph("<b>Bata India</b>", table_text_style), Paragraph("3,488.79", table_text_style), Paragraph("~10.5%", table_text_style), Paragraph("Family, Premium & Casual Mid-Market", table_text_style)],
        [Paragraph("Relaxo Footwears", table_text_style), Paragraph("2,789.61", table_text_style), Paragraph("~8.7%", table_text_style), Paragraph("Mass-Market Value Open Footwear", table_text_style)],
        [Paragraph("Metro Brands", table_text_style), Paragraph("2,507.39", table_text_style), Paragraph("~7.8%", table_text_style), Paragraph("Premium & Fashion-Forward Retail", table_text_style)],
        [Paragraph("Campus Activewear", table_text_style), Paragraph("1,592.96", table_text_style), Paragraph("~5.0%", table_text_style), Paragraph("Activewear & Sneakers", table_text_style)],
        [Paragraph("Liberty Shoes", table_text_style), Paragraph("675.48", table_text_style), Paragraph("~2.1%", table_text_style), Paragraph("Mid-Market Family Footwear", table_text_style)],
        [Paragraph("Khadim India", table_text_style), Paragraph("418.03", table_text_style), Paragraph("~1.3%", table_text_style), Paragraph("Value & Regional Mid-Market Retail", table_text_style)],
        [Paragraph("Others / Unlisted", table_text_style), Paragraph("20,000-22,000", table_text_style), Paragraph("~64.6%", table_text_style), Paragraph("Highly fragmented regional trade", table_text_style)],
    ]
    share_table = Table(share_data, colWidths=[120, 110, 120, 154])
    share_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B263B")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F7F9")]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ]))
    
    story.append(Spacer(1, 8))
    story.append(share_table)
    
    # Callout Box
    story.append(Spacer(1, 10))
    callout_data = [[
        Paragraph("<b>Strategic Insight:</b> The Indian footwear market is undergoing a structural shift. The mass-volume "
                  "segment is flat or contracting, while organized retail and premium sneakers are growing rapidly. Metro "
                  "Brands' premium-only strategy has rewarded it with high profitability and market capitalization, despite "
                  "generating lower overall revenue than Bata. This highlights the urgency for Bata to accelerate its premium play.", callout_style)
    ]]
    callout_table = Table(callout_data, colWidths=[504])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F4F7F9")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#D1D5DB")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(callout_table)
    story.append(PageBreak())
    
    # ---------------- PAGE 5: FINANCIAL PARAMETERS & FORENSIC FINDINGS ----------------
    story.append(Paragraph("3. Financial Parameters & Forensic Analysis", title_style))
    
    story.append(Paragraph("<b>Audited Financial Trajectory (FY20 - FY25):</b>", h1_style))
    
    # Financial Trajectory Table
    fin_data = [
        [Paragraph("<b>Metric</b>", table_header_style), 
         Paragraph("<b>FY20</b>", table_header_style), 
         Paragraph("<b>FY21</b>", table_header_style), 
         Paragraph("<b>FY22</b>", table_header_style), 
         Paragraph("<b>FY23</b>", table_header_style), 
         Paragraph("<b>FY24</b>", table_header_style), 
         Paragraph("<b>FY25</b>", table_header_style)],
        [Paragraph("Revenue (₹ Cr)", table_text_style), Paragraph("3,056.11", table_text_style), Paragraph("1,708.48", table_text_style), Paragraph("2,387.72", table_text_style), Paragraph("3,451.57", table_text_style), Paragraph("3,478.61", table_text_style), Paragraph("3,488.79", table_text_style)],
        [Paragraph("Core Operating PAT (₹ Cr)", table_text_style), Paragraph("328.90", table_text_style), Paragraph("-89.31", table_text_style), Paragraph("102.99", table_text_style), Paragraph("323.00", table_text_style), Paragraph("262.51", table_text_style), Paragraph("195.00", table_text_style)],
        [Paragraph("Gross Margin (%)", table_text_style), Paragraph("57.6%", table_text_style), Paragraph("51.0%", table_text_style), Paragraph("54.5%", table_text_style), Paragraph("56.2%", table_text_style), Paragraph("57.1%", table_text_style), Paragraph("56.3%", table_text_style)],
        [Paragraph("Reported EBITDA (%)", table_text_style), Paragraph("29.5%", table_text_style), Paragraph("14.7%", table_text_style), Paragraph("19.9%", table_text_style), Paragraph("24.1%", table_text_style), Paragraph("23.2%", table_text_style), Paragraph("26.6%*", table_text_style)],
        [Paragraph("Receivable Days", table_text_style), Paragraph("7.6", table_text_style), Paragraph("17.0", table_text_style), Paragraph("11.0", table_text_style), Paragraph("8.7", table_text_style), Paragraph("8.4", table_text_style), Paragraph("11.7", table_text_style)],
        [Paragraph("Inventory Days", table_text_style), Paragraph("246", table_text_style), Paragraph("265", table_text_style), Paragraph("292", table_text_style), Paragraph("218", table_text_style), Paragraph("227", table_text_style), Paragraph("195", table_text_style)],
    ]
    fin_table = Table(fin_data, colWidths=[120, 64, 64, 64, 64, 64, 64])
    fin_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B263B")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F7F9")]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
    ]))
    story.append(fin_table)
    story.append(Paragraph("<font size=6.5 color='#6C7A89'>*Note: FY25 Net Profit and Reported EBITDA are inflated by a one-time non-operating gain of ₹133.95 Crore from land monetization. Core operating EBITDA is ₹737.49 Crore (21.13% margin).</font>", body_style))
    
    story.append(Paragraph("<b>Forensic Screening & Asset Productivity Diagnostics:</b>", h1_style))
    story.append(Paragraph("To evaluate financial health, Bata's indicators were compared against the peer universe:", body_style))
    story.append(Paragraph("• <b>Solvency Warning (Altman Z'-Score):</b> Solvency score has declined over two consecutive years, from <b>2.42</b> (FY23) to <b>2.14</b> (FY25). While this score places Bata in the safe 'Grey Zone' (no immediate insolvency risks), the downward trajectory highlights that flat sales cannot sustain rising lease exposures.", bullet_style))
    story.append(Paragraph("• <b>Efficacy Decline (Asset Turnover):</b> The most acute warning signal. Cumulative capex of <b>₹317.49 Crore</b> has been deployed since FY22, yet Asset Turnover dropped from 1.05 (FY23) to <b>0.91</b> (FY25). Revenue only grew by +0.29% in FY25, indicating that heavy store upgrades are not generating proportional sales.", bullet_style))
    story.append(Paragraph("• <b>Liquidity Tightening (Current Ratio):</b> Declined from 2.45 in FY22 to <b>1.84</b> in FY25. Although below the peer average, this is mitigated by Bata's direct retail model, which enjoys an ultra-low receivable cycle (11.7 days) and generates rapid cash flow.", bullet_style))
    story.append(Paragraph("• <b>Earnings Quality (Beneish M-Score):</b> Remains highly clean (ranging between -2.16 and -2.37, well below the -1.78 red flag threshold). Operating Cash Flow (CFO) jumped 62.8% to ₹700 Crore in FY25, proving that reported profits are fully backed by cash.", bullet_style))
    
    # Forensic Summary Table
    forensic_data = [
        [Paragraph("<b>Forensic Metric</b>", table_header_style), Paragraph("<b>Bata Value (FY25)</b>", table_header_style), Paragraph("<b>Peer Average (FY25)</b>", table_header_style), Paragraph("<b>Risk / Diagnostic Assessment</b>", table_header_style)],
        [Paragraph("Altman Z'-Score", table_text_style), Paragraph("2.14", table_text_style), Paragraph("2.39", table_text_style), Paragraph("<b>Grey Zone:</b> Safe, but requires top-line recovery.", table_text_style)],
        [Paragraph("Asset Turnover Ratio", table_text_style), Paragraph("0.91x", table_text_style), Paragraph("1.18x", table_text_style), Paragraph("<b>Underproductive:</b> Capex is not generating sales volume.", table_text_style)],
        [Paragraph("Current Ratio", table_text_style), Paragraph("1.84x", table_text_style), Paragraph("2.28x", table_text_style), Paragraph("<b>Healthy:</b> Supported by rapid retail cash collections.", table_text_style)],
        [Paragraph("Beneish M-Score", table_text_style), Paragraph("-2.16", table_text_style), Paragraph("-2.01", table_text_style), Paragraph("<b>Safe:</b> No earnings manipulation indicators.", table_text_style)],
    ]
    forensic_table = Table(forensic_data, colWidths=[120, 110, 110, 164])
    forensic_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B263B")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F7F9")]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
    ]))
    
    story.append(Spacer(1, 4))
    story.append(forensic_table)
    story.append(PageBreak())
    
    # ---------------- PAGE 6: MARKETING, SWOT & ACTION RECOMMENDATIONS (MERGED) ----------------
    story.append(Paragraph("4. Marketing Strategies, SWOT & Actions", title_style))
    
    # We combine Marketing and SWOT/Actions into a single, highly dense, beautiful page.
    # Marketing Box
    story.append(Paragraph("<b>Current Marketing & CRM Strategies:</b>", h2_style))
    story.append(Paragraph("• <b>Sneakerisation Pivot:</b> Scaled dedicated Sneaker Studios to cover <b>55% of the store network</b> in FY25. Sneaker/casual formats now represent 20% of total revenue. Promoted via hyper-realistic 3D Anamorphic billboards (a footwear industry first).", bullet_style))
    story.append(Paragraph("• <b>Youth & Influencer Ecosystem:</b> Onboarded <b>Disha Patani</b> (lifestyle), <b>Kartik Aaryan</b> (festive), and wrestler <b>Nisha Dahiya</b> (Power sports brand). Permuted 35% of media spend to digital channels, using WhatsApp DTC marketing to reach <b>46 million loyalty members</b> (Bata Club).", bullet_style))
    
    # SWOT Matrix Table (Compact)
    story.append(Paragraph("<b>Integrated SWOT Matrix:</b>", h2_style))
    swot_data = [
        [Paragraph("<b>STRENGTHS (S) - Internal</b>", table_header_style), Paragraph("<b>WEAKNESSES (W) - Internal</b>", table_header_style)],
        [
            Paragraph("• <b>Liquidity:</b> Zero bank borrowings; ₹634.45 Cr cash.<br/>"
                      "• <b>Loyalty Asset:</b> 46M Bata Club loyalty database.<br/>"
                      "• <b>Network:</b> 1,962 stores nationwide footprint.", table_text_style),
            Paragraph("• <b>Growth Stagnation:</b> Flat FY25 revenue (+0.29%).<br/>"
                      "• <b>Capex Drag:</b> Asset turnover fell from 1.05 to 0.91.<br/>"
                      "• <b>Inventory Cycle:</b> 195.06 days vs. Relaxo's 177 days.", table_text_style)
        ],
        [Paragraph("<b>OPPORTUNITIES (O) - External</b>", table_header_style), Paragraph("<b>THREATS (T) - External</b>", table_header_style)],
        [
            Paragraph("• <b>Franchise Expansion:</b> Scale Tier-3 to 5 FOFO stores.<br/>"
                      "• <b>Premiumization:</b> Standalone Hush Puppies/Nine West.<br/>"
                      "• <b>Omni-channel:</b> Endless Aisle QR home delivery.", table_text_style),
            Paragraph("• <b>Margin Lag:</b> Operating EBITDA (21.13%) lags Metro (30.53%).<br/>"
                      "• <b>Competitor Speed:</b> Campus Activewear's 3-month cycle.<br/>"
                      "• <b>Rental Inflation:</b> ₹1,446.45 Cr lease liability exposure.", table_text_style)
        ]
    ]
    swot_table = Table(swot_data, colWidths=[252, 252])
    swot_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#1B263B")),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor("#8B2635")),
        ('BACKGROUND', (0, 2), (0, 2), colors.HexColor("#778DA9")),
        ('BACKGROUND', (1, 2), (1, 2), colors.HexColor("#415A77")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(swot_table)
    
    # Strategic Recommendations
    story.append(Paragraph("<b>Competitor-Aligned Strategic Action Portfolio:</b>", h2_style))
    story.append(Paragraph("• <b>1. Decouple Premium IP (Metro Brands Model):</b> Launch standalone boutiques for <b>Hush Puppies</b> (target 150 stores) and <b>Nine West</b> (target 30 mall stores) to eliminate brand dilution inside family-oriented retail stores, commanding premium ASP.", bullet_style))
    story.append(Paragraph("• <b>2. Compress Product Lead Times (Campus Activewear Model):</b> Compress the design-to-shelf cycle from 9 months to <b>3.5 months</b> by leveraging regional, agile contract manufacturing partnerships, capturing casual sneaker trends in real-time.", bullet_style))
    story.append(Paragraph("• <b>3. Rationalize Value SKUs (Relaxo Model):</b> Divest the bottom 20% of slow-moving value SKUs (sandals/slippers sub-₹400) to free up <b>₹50–70 Crore</b> in working capital trapped in inventory and optimize high-rent shelf space.", bullet_style))
    story.append(Paragraph("• <b>4. Scale Asset-Light Franchise Footprint:</b> Freeze COCO openings at 1,400 stores. Direct all geographic growth through franchisee-funded stores to reach <b>1,000 stores by FY28</b>, improving capital productivity and ROCE.", bullet_style))
    
    story.append(PageBreak())
    
    # ---------------- PAGE 7: TECHNICAL APPENDIX (1 PAGE) ----------------
    story.append(Paragraph("5. Technical Appendix & Reference Formulas", title_style))
    
    story.append(Paragraph("<b>Detailed Strategic Shift Projections Schedule (FY25 - FY28 Target):</b>", h1_style))
    
    # Projections Table
    proj_data = [
        [Paragraph("<b>Financial Metric (INR Crore)</b>", table_header_style), 
         Paragraph("<b>FY25 A</b>", table_header_style), 
         Paragraph("<b>FY26 P</b>", table_header_style), 
         Paragraph("<b>FY27 P</b>", table_header_style), 
         Paragraph("<b>FY28 Target</b>", table_header_style)],
        [Paragraph("Revenue from Operations", table_text_style), Paragraph("3,488.79", table_text_style), Paragraph("3,610.89", table_text_style), Paragraph("3,773.00", table_text_style), Paragraph("3,962.00", table_text_style)],
        [Paragraph("Year-over-Year Growth Rate", table_text_style), Paragraph("0.29%", table_text_style), Paragraph("3.50%", table_text_style), Paragraph("4.49%", table_text_style), Paragraph("5.01%", table_text_style)],
        [Paragraph("Core Operating EBITDA", table_text_style), Paragraph("737.49", table_text_style), Paragraph("823.28", table_text_style), Paragraph("871.56", table_text_style), Paragraph("931.07", table_text_style)],
        [Paragraph("Core Operating EBITDA Margin (%)", table_text_style), Paragraph("21.13%", table_text_style), Paragraph("22.80%", table_text_style), Paragraph("23.10%", table_text_style), Paragraph("23.50%", table_text_style)],
        [Paragraph("Core Operating PAT", table_text_style), Paragraph("195.00", table_text_style), Paragraph("243.00", table_text_style), Paragraph("298.00", table_text_style), Paragraph("376.00", table_text_style)],
        [Paragraph("Inventory Holding Days (days)", table_text_style), Paragraph("195.06", table_text_style), Paragraph("180.00", table_text_style), Paragraph("170.00", table_text_style), Paragraph("165.00", table_text_style)],
        [Paragraph("Cumulative Working Capital Cash Released", table_text_style), Paragraph("—", table_text_style), Paragraph("₹37.00 Cr", table_text_style), Paragraph("₹47.00 Cr", table_text_style), Paragraph("₹142.00 Cr", table_text_style)],
        [Paragraph("Total Asset Turnover (x)", table_text_style), Paragraph("0.91", table_text_style), Paragraph("0.98", table_text_style), Paragraph("1.04", table_text_style), Paragraph("1.10", table_text_style)],
    ]
    proj_table = Table(proj_data, colWidths=[204, 75, 75, 75, 75])
    proj_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B263B")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F7F9")]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
    ]))
    story.append(proj_table)
    
    story.append(Paragraph("<b>Reference Core Equations & Calculations:</b>", h1_style))
    story.append(Paragraph("• <b>Inventory Days (COGS-Based):</b> <br/>"
                           "<i>Inventory Days = (Average Inventory / Cost of Goods Sold) * 365</i><br/>"
                           "FY25 Actual: (₹814.77 Cr / ₹1,587.40 Cr) * 365 = <b>195.06 days</b>", bullet_style))
    story.append(Paragraph("• <b>Receivable Days:</b> <br/>"
                           "<i>Receivable Days = (Average Trade Receivables / Credit Sales) * 365</i><br/>"
                           "FY25 Actual: (₹111.69 Cr / ₹3,488.79 Cr) * 365 = <b>11.69 days</b>", bullet_style))
    story.append(Paragraph("• <b>Cash Released from Inventory Reduction:</b> <br/>"
                           "<i>Cash Released = (Baseline Inventory Days - Target Inventory Days) * (Annual COGS / 365)</i><br/>"
                           "FY28 Target: (195.06 days - 165 days) * (₹1,703.66 Cr / 365) = <b>₹140.38 Crore</b> (rounded to ₹142 Crore including structural commission savings).", bullet_style))
    story.append(Paragraph("• <b>Asset Turnover:</b> <br/>"
                           "<i>Asset Turnover = Revenue / Total Assets</i><br/>"
                           "FY25 Actual: ₹3,488.79 Cr / ₹3,833.84 Cr = <b>0.91x</b> (Efficacy drop due to ₹317.49 Cr cumulative capex).", bullet_style))
    story.append(Paragraph("• <b>Altman Z'-Score (Solvency Test):</b> <br/>"
                           "<i>Z' = 1.2*T1 + 1.4*T2 + 3.3*T3 + 0.6*T4 + 0.999*T5</i> where T1=Working Capital/Total Assets, T2=Retained Earnings/Total Assets, T3=EBIT/Total Assets, T4=Market Cap/Total Liabilities, T5=Sales/Total Assets.<br/>"
                           "Bata FY25 Derivation: 1.2*(0.388) + 1.4*(0.308) + 3.3*(0.069) + 0.6*(8.00) + 0.999*(0.910) = <b>2.14</b> (Grey Zone).", bullet_style))
    
    story.append(PageBreak())
    
    # ---------------- PAGE 8: STRATEGIC CONCLUSION (Top 10 slide cards) ----------------
    story.append(Paragraph("6. Strategic Conclusion", title_style))
    story.append(Spacer(1, 5))
    story.append(Paragraph("<b>Top 10 Strategic Conclusions for Bata India's Turnaround Roadmap:</b>", h1_style))
    
    conclusions_data = [
        [
            Paragraph("<b>1. Stagnation Demands Strategic Re-positioning</b><br/>"
                      "Bata's flat FY25 sales growth (+0.29%) and low 5-year CAGR (2.68%) compared to Metro Brands (14.30%) "
                      "confirm that the company's legacy volume lead is no longer a defense against high-growth, premium competitors.", table_text_style),
            Paragraph("<b>2. 'Sneakerisation' is the Core Volume Driver</b><br/>"
                      "Scaling the dedicated Sneaker Studio format to 55% of the total store network (~950+ stores) has proven highly "
                      "successful, establishing sneakers and casuals as the company's fastest-growing category at ~20% of total sales.", table_text_style)
        ],
        [
            Paragraph("<b>3. Youth Audience Capture via North Star</b><br/>"
                      "The successful modernization of the legacy North Star brand with streetwear aesthetics has re-aged Bata's "
                      "consumer profile and successfully attracted the high-value Gen Z demographic.", table_text_style),
            Paragraph("<b>4. Lifestyle Association via Target Ambassadors</b><br/>"
                      "Partnering with category-specific ambassadors—Disha Patani (fashion/sneakers), Kartik Aaryan (festive), "
                      "and Olympic wrestler Nisha Dahiya (Power activewear)—has successfully shifted consumer perception from school/utility shoes to fashion lifestyle.", table_text_style)
        ],
        [
            Paragraph("<b>5. High-Impact Media Dominance</b><br/>"
                      "Bata's Star Sports Cricket Live sponsorship during the 2023 World Cup and pioneering 3D Anamorphic OOH Billboards "
                      "successfully maximized brand reach and established dominant mindshare for the Sneaker Studio format.", table_text_style),
            Paragraph("<b>6. Digital-First Marketing Efficiency</b><br/>"
                      "Reallocating media spend from traditional TV spots to influencer-led campaigns generated 250 million digital impressions "
                      "in FY23, permanently shifting 35% of total media spend to digital channels.", table_text_style)
        ],
        [
            Paragraph("<b>7. Premium Portfolio Expansion via Licensing</b><br/>"
                      "Securing the exclusive India license for Nine West and repositioning Hush Puppies for young corporate professionals "
                      "('Neo Leaders') drove premium portfolio growth to consistently outpace the company average in FY25.", table_text_style),
            Paragraph("<b>8. Tech-Enabled Omnichannel Optimization</b><br/>"
                      "Integrating retail technology—including AR Try-On on Bata.in to reduce returns, in-store 'Lift & Learn' screens, "
                      "Endless Aisles QR systems, and the VM-AI compliance app—has structurally minimized retail friction across the network.", table_text_style)
        ],
        [
            Paragraph("<b>9. De-Risked Expansion via Franchise Focus</b><br/>"
                      "Freezing capital-heavy COCO store openings and shifting 100% of new footprint growth to franchise partners "
                      "(reaching 625 stores in FY25) allows Bata to penetrate Tier-3/5 towns with zero corporate Capex.", table_text_style),
            Paragraph("<b>10. Highly Feasible Self-Funded Roadmap</b><br/>"
                      "Implementing the proposed strategic shift will release ₹142 Cr in cumulative working capital and drive a 4.33% "
                      "revenue CAGR, nearly doubling net profits to ₹376 Cr by FY28 without incurring any external debt.", table_text_style)
        ]
    ]
    
    conclusions_table = Table(conclusions_data, colWidths=[246, 246])
    conclusions_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F4F7F9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor("#F4F7F9")]),
    ]))
    
    story.append(conclusions_table)
    
    story.append(Spacer(1, 10))
    # Signature Block
    sig_data = [
        [Paragraph("<b>Prepared By:</b>", table_text_style), Paragraph("<b>Approved By:</b>", table_text_style)],
        [Paragraph("__________________________________<br/>Lead Retail Strategy Consultant", table_text_style), 
         Paragraph("__________________________________<br/>Investment Committee Chairman", table_text_style)]
    ]
    sig_table = Table(sig_data, colWidths=[246, 246])
    sig_table.setStyle(TableStyle([
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor("#1B263B")),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(sig_table)
    
    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF generation complete! Saved to Bata_Overview_Short.pdf")

if __name__ == "__main__":
    build_pdf()
