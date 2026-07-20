import re

test_cases = [
    "697.53 590.08",
    "(2,140.55) (1,629.32)",
    "697.53 590.08,Firoz,Pradhan...",
    "1.33 5.06"
]

def clean_num(s):
    s = s.strip()
    if not s:
        return None
    is_neg = False
    if '(' in s or ')' in s or '-' in s:
        is_neg = True
    s = s.replace(')', '').replace('(', '').replace('-', '').replace(',', '')
    try:
        val = float(s)
        return -val if is_neg else val
    except ValueError:
        return None

def split_merged(s):
    s = str(s).strip()
    matches = re.findall(r'[(-]?\d[\d,]*\.\d{2}[)]?', s)
    if len(matches) >= 2:
        part1 = matches[-2]
        part2 = matches[-1]
        v1 = clean_num(part1)
        v2 = clean_num(part2)
        return v1, v2
    return None

for tc in test_cases:
    print(f"Input: {tc:<60} -> Split: {split_merged(tc)}")
