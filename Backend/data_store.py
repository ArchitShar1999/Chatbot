import pandas as pd
import re

EXCEL_PATH = "alarm_database.xlsx"

df = pd.read_excel(EXCEL_PATH)

# Normalize columns
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(".", "", regex=False)
)

CODE_COL = "alarm no"
DESC_COL = "alarm description"
SOLUTION_COL = "solution"

# Normalize alarm numbers
def normalize_code(val):
    nums = re.findall(r"\d+", str(val))
    return nums[0] if nums else None

df["_alarm_num"] = df[CODE_COL].apply(normalize_code)

STOPWORDS = {
    "why", "what", "how", "comes", "come", "alarm", "issue",
    "problem", "error", "is", "the", "does", "occur"
}

def tokenize(text):
    words = re.findall(r"[a-zA-Z]+", text.lower())
    return [w for w in words if w not in STOPWORDS]

def get_alarm_by_code(code: str):
    nums = re.findall(r"\d+", code)
    if not nums:
        return None

    alarm_num = nums[0]
    result = df[df["_alarm_num"] == alarm_num]

    if result.empty:
        return None

    row = result.iloc[0]
    return {
        "Alarm Code": f"AL{alarm_num}",
        "Description": row[DESC_COL],
        "Solution": row[SOLUTION_COL]
    }

def search_alarm_by_description(text: str):
    tokens = tokenize(text)

    if not tokens:
        return None

    best_row = None
    best_score = 0

    for _, row in df.iterrows():
        desc = str(row[DESC_COL]).lower()
        score = sum(1 for t in tokens if t in desc)

        if score > best_score:
            best_score = score
            best_row = row

    if best_row is None or best_score == 0:
        return None

    alarm_num = best_row["_alarm_num"]

    return {
        "Alarm Code": f"AL{alarm_num}",
        "Description": best_row[DESC_COL],
        "Solution": best_row[SOLUTION_COL]
    }
