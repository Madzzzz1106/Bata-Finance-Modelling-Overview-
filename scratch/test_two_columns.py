import fitz
import pandas as pd

doc = fitz.open("Metro_FY25.pdf")
page = doc[116] # page 117
words = page.get_text("words")

# Split words into left column (Balance Sheet) and right column (Profit & Loss)
left_words = [w for w in words if w[0] < 280]
right_words = [w for w in words if w[0] >= 280]

def group_words_to_df(words_list):
    # Group by y
    words_list.sort(key=lambda w: w[1])
    lines = []
    current_line = []
    current_y = None
    y_tolerance = 4.0
    
    for w in words_list:
        x0, y0, x1, y1, word, _, _, _ = w
        if current_y is None:
            current_y = y0
            current_line.append(w)
        elif abs(y0 - current_y) <= y_tolerance:
            current_line.append(w)
        else:
            current_line.sort(key=lambda wl: wl[0])
            lines.append(current_line)
            current_line = [w]
            current_y = y0
    if current_line:
        current_line.sort(key=lambda wl: wl[0])
        lines.append(current_line)
        
    # Print lines
    for idx, line in enumerate(lines):
        line_str = " ".join([w[4] for w in line])
        print(f"Line {idx}: {line_str}")

print("=== LEFT COLUMN (Balance Sheet) ===")
group_words_to_df(left_words)

print("\n=== RIGHT COLUMN (Profit & Loss) ===")
group_words_to_df(right_words)
