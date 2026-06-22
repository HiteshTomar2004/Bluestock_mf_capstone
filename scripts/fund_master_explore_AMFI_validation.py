import pandas as pd
from pathlib import Path

RAW_DATA_DIR = Path("data/raw")
FUND_MASTER_FILE = RAW_DATA_DIR / "01_fund_master.csv"
fund_master = pd.read_csv(FUND_MASTER_FILE)

# for fund master exploration
print("FUND MASTER EXPLORATION")
print("\nUnique Fund Houses:")
print(fund_master["fund_house"].unique())

print("\nUnique Categories:")
print(fund_master["category"].unique())

print("\nUnique Sub-Categories:")
print(fund_master["sub_category"].unique())

print("\nUnique Risk Grades:")
print(fund_master["risk_category"].unique())

print("\nAMFI Code Structure:")
print(fund_master["amfi_code"].head(10))

#for AMFI validation
NAV_HISTORY_FILE = RAW_DATA_DIR / "02_nav_history.csv"
nav_history = pd.read_csv(NAV_HISTORY_FILE)
print("AMFI CODE VALIDATION")

fund_master_codes = set(fund_master["amfi_code"].astype(str))
nav_history_codes = set(nav_history["amfi_code"].astype(str))

missing_codes = fund_master_codes - nav_history_codes
matched_codes = fund_master_codes.intersection(nav_history_codes)

print(f"\nTotal AMFI codes in fund_master: {len(fund_master_codes)}")
print(f"Total AMFI codes in nav_history: {len(nav_history_codes)}")
print(f"Matching AMFI codes: {len(matched_codes)}")
print(f"Missing AMFI codes in nav_history: {len(missing_codes)}")

if missing_codes:
    print("\nCodes present in fund_master but missing from nav_history:")
    print(sorted(missing_codes))
else:
    print("\nAll AMFI codes from fund_master exist in nav_history.")


print("DATA QUALITY SUMMARY")

if missing_codes:
    validation_result = (
        f"{len(missing_codes)} AMFI codes from fund_master are missing in nav_history."
    )
else:
    validation_result = (
        "All AMFI codes in fund_master are available in nav_history."
    )

summary = f"""
    Data Quality Summary:

    The fund_master dataset contains {len(fund_master)} mutual fund scheme records.
    It includes {fund_master["fund_house"].nunique()} unique fund houses,
    {fund_master["category"].nunique()} unique categories,
    {fund_master["sub_category"].nunique()} unique sub-categories,
    and {fund_master["risk_category"].nunique()} unique risk grades.

    AMFI codes serve as unique scheme identifiers and act as the primary key for linking mutual fund metadata with NAV history and other related datasets.
    The fund_master file contains {len(fund_master_codes)} unique AMFI codes.
    The nav_history file contains {len(nav_history_codes)} unique AMFI codes.

    Validation result:
    {validation_result}
"""

print(summary)