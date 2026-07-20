import matplotlib.pyplot as plt
import numpy as np

# Data
years = ['FY22', 'FY23', 'FY24', 'FY25']
z_scores = [1.99, 2.42, 2.37, 2.14]

# Create figure and axis with a solid white background
fig, ax = plt.subplots(figsize=(10, 7), dpi=300, facecolor='white')
ax.set_facecolor('white')

# Define zones
# Safe Zone (Grey): 2.9 to 4.0
ax.axhspan(2.9, 4.0, facecolor='#E2E8F0', alpha=0.9)  # Light slate grey
# Grey Zone (Yellow): 1.23 to 2.9
ax.axhspan(1.23, 2.9, facecolor='#FEF3C7', alpha=0.9)  # Light amber/yellow
# Distress Zone (Orange/Amber): 0 to 1.23
ax.axhspan(0.0, 1.23, facecolor='#FEE2E2', alpha=0.9)  # Light red/pink

# Plot line
ax.plot(years, z_scores, color='#1E3A8A', linewidth=3, marker='o', markersize=10, zorder=5)  # Dark blue line

# Add data labels
for i, txt in enumerate(z_scores):
    ax.annotate(f'{txt:.2f}', (years[i], z_scores[i]), textcoords="offset points", xytext=(0,15), ha='center', fontsize=12, fontweight='bold', color='#1E293B')

# Callouts
# Peak Callout
ax.annotate('Peak: 2.42', xy=('FY23', 2.42), xytext=('FY23', 3.1),
            arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.5),
            ha='center', va='center', bbox=dict(boxstyle='square,pad=0.5', fc='white', ec='black', lw=1), fontsize=11)

# Decline Callout
ax.annotate('FY25: 2.14 —\n2yr decline', xy=('FY25', 2.14), xytext=('FY25', 2.65),
            arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.5),
            ha='center', va='center', bbox=dict(boxstyle='square,pad=0.5', fc='white', ec='black', lw=1), fontsize=11)

# Formatting
ax.set_ylim(0, 4.0)
ax.set_xlim(-0.5, 4.2)
ax.set_ylabel("Z'-Score Value", fontweight='bold', fontsize=11, color='#1E293B')
ax.set_title("Altman Z'-Score Trend with Zone Bands", pad=30, fontsize=18, fontweight='bold', color='#1E293B')

# Zone Labels
ax.text(3.5, 3.5, "Safe Zone\n(Z' > 2.9)", ha='center', va='center', fontsize=11, color='#1E293B')
ax.text(3.5, 1.8, "Grey Zone\n(1.23 < Z' <= 2.9)", ha='center', va='center', fontsize=11, color='#B45309')
ax.text(3.5, 0.6, "Distress Zone\n(Z' <= 1.23)", ha='center', va='center', fontsize=11, color='#991B1B')

# Gridlines (dashed, horizontal only)
ax.yaxis.grid(True, linestyle='--', color='gray', alpha=0.3)
ax.xaxis.grid(False)

# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Save the figure with a solid white background
plt.savefig('/Users/mridulagarwal/Desktop/BATA/extracted/z_score_chart.png', transparent=False, bbox_inches='tight', facecolor='white')
print("Chart generated successfully at /Users/mridulagarwal/Desktop/BATA/extracted/z_score_chart.png")
