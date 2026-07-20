import fitz

doc = fitz.open("Metro_FY21.pdf")
page = doc[98] # page 99
words = page.get_text("words")

# Filter words to active coordinates
words = [w for w in words if 0 <= w[0] <= 1500]

header_words = [w for w in words if 80 < w[1] < 140]
note_x = None
y_curr_x = None
y_prev_x = None
year_words = ["2025", "2024", "2023", "2022", "2021", "2020"]

for w in header_words:
    word_text = w[4].lower().strip().replace(".", "").replace(",", "")
    cx = (w[0] + w[2]) / 2.0
    if "note" in word_text:
        note_x = cx
    elif any(yr in word_text for yr in year_words):
        print(f"Matched year word: '{w[4]}' at cx={cx}")
        if y_curr_x is None:
            y_curr_x = cx
        else:
            y_prev_x = cx

print(f"Detected: Note={note_x}, Curr={y_curr_x}, Prev={y_prev_x}")

t1 = note_x - 30.0
t2 = (note_x + y_curr_x) / 2.0
t3 = (y_curr_x + y_prev_x) / 2.0
print(f"t1={t1}, t2={t2}, t3={t3}")

# Table words around y=360
table_words = [w for w in words if 355 < w[1] < 365]
table_words.sort(key=lambda w: w[0])
print("\nWords in row y=360:")
for w in table_words:
    cx = (w[0] + w[2]) / 2.0
    col = 0
    if cx < t1: col = 0
    elif cx < t2: col = 1
    elif cx < t3: col = 2
    else: col = 3
    print(f"Word: '{w[4]}' -> cx={cx:.1f}, Col={col}")
