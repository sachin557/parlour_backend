import pandas as pd
import os

# 📁 Always resolve path relative to this file (NOT cwd)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EXCEL_FILE_MAP = {
    ("men", "makeup"): "Backend_men_makeup_data.xlsx",
    ("men", "spa"): "Backend_men_spa_data.xlsx",
    ("men", "hair"): "Backend_parlour_men_data.xlsx",

    ("women", "makeup"): "Backend_women_makeup.xlsx",
    ("women", "spa"): "Backend_women_spa_data.xlsx",
    ("women", "hair"): "Backend_parlour_women_data.xlsx",
}

REQUIRED_COLUMNS = [
    "name",
    "address",
    "rating",
    "open_now",
    "opening_hours",
    "international_phone",
    "website",
    "map_link",
]

def get_parlour_list(gender: str, category: str, limit: int = 15):
    key = (gender.lower(), category.lower())

    # ❌ Invalid gender/category
    if key not in EXCEL_FILE_MAP:
        raise ValueError("Invalid gender/category combination")

    file_name = EXCEL_FILE_MAP[key]
    file_path = os.path.join(BASE_DIR, file_name)

    # ❌ File missing
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_name} not found")

    # 📊 Load Excel
    df = pd.read_excel(file_path)

    # ❌ Remove rows without salon name
    df.dropna(subset=["name"], inplace=True)

    # ❌ Validate required columns
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in Excel: {missing}")

    # 🔥 CRITICAL FIX: Replace NaN → empty string (JSON-safe)
    df = df.where(pd.notna(df), "")

    # 🔢 Limit rows
    df = df.head(limit)

    # ✅ Convert to JSON-safe dict
    return df.to_dict(orient="records")
