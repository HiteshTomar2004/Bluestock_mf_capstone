import pandas as pd
from pathlib import Path

RAW_FILE = Path("data/raw/02_nav_history.csv")
PROCESSED_DIR = Path("data/processed")
OUTPUT_FILE = PROCESSED_DIR / "clean_nav_history.csv"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

nav = pd.read_csv(RAW_FILE)

print("Original shape:", nav.shape)

nav["date"] = pd.to_datetime(nav["date"], errors="coerce")
nav["nav"] = pd.to_numeric(nav["nav"], errors="coerce")

invalid_dates = nav["date"].isna().sum()
invalid_nav = nav["nav"].isna().sum()
non_positive_nav = (nav["nav"] <= 0).sum()

print("Invalid dates:", invalid_dates)
print("Invalid NAV values:", invalid_nav)
print("NAV <= 0:", non_positive_nav)

nav = nav.dropna(subset=["amfi_code", "date", "nav"])
nav = nav[nav["nav"] > 0]

duplicates_before = nav.duplicated(subset=["amfi_code", "date"]).sum()
print("Duplicate amfi_code + date rows:", duplicates_before)

nav = nav.drop_duplicates(subset=["amfi_code", "date"], keep="last")
nav = nav.sort_values(["amfi_code", "date"])

filled_nav_data = []

for amfi_code, fund_data in nav.groupby("amfi_code"):
    fund_data = fund_data.sort_values("date")

    full_date_range = pd.date_range(
        start=fund_data["date"].min(),
        end=fund_data["date"].max(),
        freq="D"
    )

    fund_data = fund_data.set_index("date")
    fund_data = fund_data.reindex(full_date_range)

    fund_data["amfi_code"] = amfi_code
    fund_data["nav"] = fund_data["nav"].ffill()
    fund_data = fund_data.reset_index().rename(columns={"index": "date"})

    filled_nav_data.append(fund_data)

clean_nav = pd.concat(filled_nav_data, ignore_index=True)

clean_nav = clean_nav.dropna(subset=["nav"])
clean_nav = clean_nav.sort_values(["amfi_code", "date"])

print("Cleaned shape:", clean_nav.shape)
print("Unique AMFI codes:", clean_nav["amfi_code"].nunique())
print("Final invalid NAV values:", clean_nav["nav"].isna().sum())
print("Final NAV <= 0:", (clean_nav["nav"] <= 0).sum())

clean_nav.to_csv(OUTPUT_FILE, index=False)

print("Saved cleaned file to:", OUTPUT_FILE)
print(clean_nav.head())