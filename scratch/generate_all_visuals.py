import matplotlib.pyplot as plt
import numpy as np
import os

# Ensure output directory exists
os.makedirs('/Users/mridulagarwal/Desktop/BATA/extracted', exist_ok=True)

# -------------------------------------------------------------
# 1. DIAGRAM 1: MECE Issue Tree Structure (Page 1) - Wide Layout
# -------------------------------------------------------------
def generate_mece_tree_diagram():
    # Adjusted to (12, 5.2) to make it wide and short
    fig, ax = plt.subplots(figsize=(12, 5.2), dpi=300, facecolor='white')
    ax.set_facecolor('white')
    
    # Hide axes
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0.5, 6)
    
    # Define box styling properties
    box_root = dict(boxstyle="round,pad=0.5", fc="#1E3A8A", ec="#172554", lw=2)
    box_branch = dict(boxstyle="round,pad=0.5", fc="#0D9488", ec="#0F766E", lw=1.5)
    box_leaf = dict(boxstyle="round,pad=0.5", fc="#F3F4F6", ec="#9CA3AF", lw=1)
    
    # Draw boxes
    # Level 0 (Root)
    ax.text(5, 5.2, "Level 0: Root Question\n(Core Problem Statement)", ha="center", va="center", color="white", bbox=box_root, fontsize=11, fontweight='bold')
    
    # Level 1 (Branches)
    ax.text(2.5, 3.2, "Level 1: Branch A\n(Mutually Exclusive)", ha="center", va="center", color="white", bbox=box_branch, fontsize=10, fontweight='bold')
    ax.text(7.5, 3.2, "Level 1: Branch B\n(Mutually Exclusive)", ha="center", va="center", color="white", bbox=box_branch, fontsize=10, fontweight='bold')
    
    # Level 2 (Leaves)
    ax.text(1.2, 1.4, "Level 2: Lever A1\n(Actionable)", ha="center", va="center", color="#1F2937", bbox=box_leaf, fontsize=9)
    ax.text(3.8, 1.4, "Level 2: Lever A2\n(Actionable)", ha="center", va="center", color="#1F2937", bbox=box_leaf, fontsize=9)
    ax.text(6.2, 1.4, "Level 2: Lever B1\n(Actionable)", ha="center", va="center", color="#1F2937", bbox=box_leaf, fontsize=9)
    ax.text(8.8, 1.4, "Level 2: Lever B2\n(Actionable)", ha="center", va="center", color="#1F2937", bbox=box_leaf, fontsize=9)
    
    # Draw connection lines (arrows)
    arrow_props = dict(arrowstyle="->", color="#4B5563", lw=1.5, shrinkA=15, shrinkB=15)
    
    # Level 0 to Level 1
    ax.annotate("", xy=(2.5, 3.2), xytext=(5, 5.2), arrowprops=arrow_props)
    ax.annotate("", xy=(7.5, 3.2), xytext=(5, 5.2), arrowprops=arrow_props)
    
    # Level 1 to Level 2
    ax.annotate("", xy=(1.2, 1.4), xytext=(2.5, 3.2), arrowprops=arrow_props)
    ax.annotate("", xy=(3.8, 1.4), xytext=(2.5, 3.2), arrowprops=arrow_props)
    ax.annotate("", xy=(6.2, 1.4), xytext=(7.5, 3.2), arrowprops=arrow_props)
    ax.annotate("", xy=(8.8, 1.4), xytext=(7.5, 3.2), arrowprops=arrow_props)
    
    # Add annotations
    ax.text(5, 0.6, "Collectively Exhaustive (CE): Sum of all branches covers 100% of problem space.", ha="center", va="center", color="#374151", fontsize=10, style='italic', bbox=dict(boxstyle="square,pad=0.3", fc="#EFF6FF", ec="#BFDBFE", lw=1))
    
    plt.title("Anatomy of a MECE Issue Tree", fontsize=14, fontweight='bold', pad=15, color='#1E293B')
    plt.tight_layout()
    plt.savefig('/Users/mridulagarwal/Desktop/BATA/extracted/mece_issue_tree_diagram.png', bbox_inches='tight', facecolor='white')
    plt.close()

# -------------------------------------------------------------
# 2. GRAPH 1: Impact vs. Feasibility Matrix (Page 1) - Wide Layout
# -------------------------------------------------------------
def generate_impact_matrix():
    # Adjusted to (12, 5.2) to make it wide and short
    fig, ax = plt.subplots(figsize=(12, 5.2), dpi=300, facecolor='white')
    ax.set_facecolor('white')
    
    # Create 2x2 quadrants
    # Top-Right: Quick Wins (Green)
    ax.axvspan(5, 10, ymin=0.5, ymax=1.0, facecolor='#ECFDF5', alpha=0.9)
    ax.text(7.5, 7.5, "QUICK WINS\n(High Impact, High Feasibility)", ha='center', va='center', color='#065F46', fontweight='bold', fontsize=9)
    
    # Top-Left: Strategic Initiatives (Blue)
    ax.axvspan(0, 5, ymin=0.5, ymax=1.0, facecolor='#EFF6FF', alpha=0.9)
    ax.text(2.5, 7.5, "STRATEGIC INITIATIVES\n(High Impact, Low Feasibility)", ha='center', va='center', color='#1E40AF', fontweight='bold', fontsize=9)
    
    # Bottom-Right: Fill-Ins (Gray)
    ax.axvspan(5, 10, ymin=0.0, ymax=0.5, facecolor='#F9FAFB', alpha=0.9)
    ax.text(7.5, 2.5, "FILL-INS\n(Low Impact, High Feasibility)", ha='center', va='center', color='#374151', fontweight='bold', fontsize=9)
    
    # Bottom-Left: Hard Slogs (Red)
    ax.axvspan(0, 5, ymin=0.0, ymax=0.5, facecolor='#FEF2F2', alpha=0.9)
    ax.text(2.5, 2.5, "HARD SLOGS / AVOID\n(Low Impact, Low Feasibility)", ha='center', va='center', color='#991B1B', fontweight='bold', fontsize=9)
    
    # Plot sample points
    points = {
        "Scale Sneaker\nStudios": (7.8, 8.5),
        "Asset-Light\nFranchise Shift": (8.2, 8.0),
        "Reduce Inventory\n(195 -> 155 days)": (7.0, 7.5),
        "Re-negotiate\nLeases": (4.5, 6.8),
        "Standalone Premium\nNine West Stores": (3.5, 5.8),
        "Value Price Cuts": (2.0, 2.0)
    }
    
    for label, coord in points.items():
        ax.scatter(coord[0], coord[1], color='#1E3A8A', s=120, edgecolors='black', zorder=5)
        ax.annotate(label, (coord[0], coord[1]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9, fontweight='bold', color='#1F2937', bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#CBD5E1", alpha=0.9), zorder=6)
        
    # Formatting
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xlabel("Feasibility (Implementation Ease) ──>", fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_ylabel("Financial Impact (ROI & Cash Release) ──>", fontsize=11, fontweight='bold', color='#1E293B')
    
    # Divide lines
    ax.axvline(5, color='#94A3B8', linestyle='--', linewidth=1.5)
    ax.axhline(5, color='#94A3B8', linestyle='--', linewidth=1.5)
    
    ax.set_title("Issue Prioritization Matrix (Consulting Framework)", fontsize=13, fontweight='bold', pad=15, color='#1E293B')
    
    # Hide standard spines
    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_visible(False)
        
    plt.tight_layout()
    plt.savefig('/Users/mridulagarwal/Desktop/BATA/extracted/impact_feasibility_matrix.png', bbox_inches='tight', facecolor='white')
    plt.close()

# -------------------------------------------------------------
# 3. DIAGRAM 2: Bata Tailored MECE Issue Tree (Page 2) - Wide Layout
# -------------------------------------------------------------
def generate_bata_issue_tree():
    # Adjusted to (14, 5.2) to make it wide and short
    fig, ax = plt.subplots(figsize=(14, 5.2), dpi=300, facecolor='white')
    ax.set_facecolor('white')
    ax.axis('off')
    ax.set_xlim(0, 12)
    ax.set_ylim(0.5, 7)
    
    # Styling
    box_root = dict(boxstyle="round,pad=0.5", fc="#7F1D1D", ec="#450A0A", lw=2)  # Dark Red
    box_branch = dict(boxstyle="round,pad=0.5", fc="#D97706", ec="#78350F", lw=1.5) # Amber
    box_leaf = dict(boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#CBD5E1", lw=1)  # Light Slate
    
    # Level 0 (Root)
    ax.text(6, 6.2, "Bata India Stagnant Growth & Capital Inefficiency\nRoot Question: How to reverse stagnating revenue and improve asset turnover?", ha="center", va="center", color="white", bbox=box_root, fontsize=11, fontweight='bold')
    
    # Level 1 (Branches)
    ax.text(2.2, 4.0, "1. Revenue Growth Levers\n(Volume & Brand Mix)", ha="center", va="center", color="white", bbox=box_branch, fontsize=9, fontweight='bold')
    ax.text(6.0, 4.0, "2. Capital & Working Capital Levers\n(Inventory & Franchise Shift)", ha="center", va="center", color="white", bbox=box_branch, fontsize=9, fontweight='bold')
    ax.text(9.8, 4.0, "3. Fixed & Overhead Cost Levers\n(Leases & Marketing ROI)", ha="center", va="center", color="white", bbox=box_branch, fontsize=9, fontweight='bold')
    
    # Level 2 (Leaves for Branch 1)
    ax.text(0.8, 1.8, "1.1 Scale Sneaker Studios\n(Combat Campus/Puma)", ha="center", va="center", color="#0F172A", bbox=box_leaf, fontsize=8)
    ax.text(2.2, 2.5, "1.2 Premium Brand Mix\n(Hush Puppies/Nine West)", ha="center", va="center", color="#0F172A", bbox=box_leaf, fontsize=8)
    ax.text(3.6, 1.8, "1.3 Drive Omnichannel\n(Monetize 46M Loyalty)", ha="center", va="center", color="#0F172A", bbox=box_leaf, fontsize=8)
    
    # Level 2 (Leaves for Branch 2)
    ax.text(4.8, 1.8, "2.1 Drop Inventory Days\n(195 -> 155 Target)", ha="center", va="center", color="#0F172A", bbox=box_leaf, fontsize=8)
    ax.text(6.0, 2.5, "2.2 Asset-Light Franchise\n(Expand in Tier 3-5 cities)", ha="center", va="center", color="#0F172A", bbox=box_leaf, fontsize=8)
    ax.text(7.2, 1.8, "2.3 Cash Receivables\n(Maintain 11-Day Cash cycle)", ha="center", va="center", color="#0F172A", bbox=box_leaf, fontsize=8)
    
    # Level 2 (Leaves for Branch 3)
    ax.text(8.6, 1.8, "3.1 Manage Leases\n(Optimize Rs.1210.9Cr ROU)", ha="center", va="center", color="#0F172A", bbox=box_leaf, fontsize=8)
    ax.text(9.8, 2.5, "3.2 Maximize Marketing ROI\n(Rationalize A&P spend)", ha="center", va="center", color="#0F172A", bbox=box_leaf, fontsize=8)
    ax.text(11.0, 1.8, "3.3 Comm. Savings\n(High-Efficiency Distrib.)", ha="center", va="center", color="#0F172A", bbox=box_leaf, fontsize=8)
    
    # Connections
    arrow_props = dict(arrowstyle="->", color="#64748B", lw=1.2, shrinkA=15, shrinkB=15)
    
    # Root to Level 1
    ax.annotate("", xy=(2.2, 4.0), xytext=(6, 6.2), arrowprops=arrow_props)
    ax.annotate("", xy=(6.0, 4.0), xytext=(6, 6.2), arrowprops=arrow_props)
    ax.annotate("", xy=(9.8, 4.0), xytext=(6, 6.2), arrowprops=arrow_props)
    
    # Branch 1 to Leaves
    ax.annotate("", xy=(0.8, 1.8), xytext=(2.2, 4.0), arrowprops=arrow_props)
    ax.annotate("", xy=(2.2, 2.5), xytext=(2.2, 4.0), arrowprops=arrow_props)
    ax.annotate("", xy=(3.6, 1.8), xytext=(2.2, 4.0), arrowprops=arrow_props)
    
    # Branch 2 to Leaves
    ax.annotate("", xy=(4.8, 1.8), xytext=(6.0, 4.0), arrowprops=arrow_props)
    ax.annotate("", xy=(6.0, 2.5), xytext=(6.0, 4.0), arrowprops=arrow_props)
    ax.annotate("", xy=(7.2, 1.8), xytext=(6.0, 4.0), arrowprops=arrow_props)
    
    # Branch 3 to Leaves
    ax.annotate("", xy=(8.6, 1.8), xytext=(9.8, 4.0), arrowprops=arrow_props)
    ax.annotate("", xy=(9.8, 2.5), xytext=(9.8, 4.0), arrowprops=arrow_props)
    ax.annotate("", xy=(11.0, 1.8), xytext=(9.8, 4.0), arrowprops=arrow_props)
    
    plt.title("Bata India Tailored Strategic MECE Issue Tree", fontsize=14, fontweight='bold', pad=15, color='#0F172A')
    plt.tight_layout()
    plt.savefig('/Users/mridulagarwal/Desktop/BATA/extracted/bata_issue_tree_diagram.png', bbox_inches='tight', facecolor='white')
    plt.close()

# -------------------------------------------------------------
# 4. GRAPH 2: Peer EBITDA Margin Comparison (Page 2)
# -------------------------------------------------------------
def generate_peer_ebitda_chart():
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300, facecolor='white')
    ax.set_facecolor('white')
    
    companies = ['Metro Brands', 'Bata India (Core)', 'Campus Activewear', 'Khadims', 'Relaxo Footwear', 'Liberty Shoes']
    margins = [30.5, 21.1, 16.2, 15.8, 14.7, 9.9]
    colors = ['#1E3A8A', '#0D9488', '#475569', '#475569', '#475569', '#475569']
    
    # Draw horizontal bars
    bars = ax.barh(companies, margins, color=colors, edgecolor='none', height=0.6)
    
    # Formatting
    ax.set_xlabel("Operating EBITDA Margin (%)", fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_xlim(0, 35)
    ax.set_title("Peer EBITDA Margin Comparison (FY25 %)", fontsize=13, fontweight='bold', pad=20, color='#1E293B')
    
    # Add values at the end of bars
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.8, bar.get_y() + bar.get_height()/2, f"{width:.1f}%", 
                va='center', ha='left', fontsize=10, fontweight='bold', color='#1F2937')
                
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#94A3B8')
    ax.spines['bottom'].set_color('#94A3B8')
    
    # Invert y-axis to have Metro Brands on top
    ax.invert_yaxis()
    
    # Show vertical gridlines (dashed)
    ax.xaxis.grid(True, linestyle='--', color='gray', alpha=0.3)
    ax.yaxis.grid(False)
    
    plt.tight_layout()
    plt.savefig('/Users/mridulagarwal/Desktop/BATA/extracted/peer_ebitda_margin_chart.png', bbox_inches='tight', facecolor='white')
    plt.close()

if __name__ == "__main__":
    generate_mece_tree_diagram()
    generate_impact_matrix()
    generate_bata_issue_tree()
    generate_peer_ebitda_chart()
    print("All report visuals generated successfully in /Users/mridulagarwal/Desktop/BATA/extracted/")
