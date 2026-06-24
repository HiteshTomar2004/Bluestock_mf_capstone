import pandas as pd
from pathlib import Path

RAW_FILE = Path("data/raw/08_investor_transactions.csv")
PROCESSED_DIR = Path("data/processed")
OUTPUT_FILE = PROCESSED_DIR / "clean_investor_transactions.csv"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

transactions = pd.read_csv(RAW_FILE)

print("Original shape:", transactions.shape)

transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"],
    errors="coerce"
)

transactions["amount_inr"] = pd.to_numeric(
    transactions["amount_inr"],
    errors="coerce"
)

transactions["transaction_type"] = (
    transactions["transaction_type"]
    .astype(str)
    .str.strip()
    .str.lower()
)

transaction_type_mapping = {
    "sip": "SIP",
    "lumpsum": "Lumpsum",
    "lump sum": "Lumpsum",
    "redemption": "Redemption",
    "redeem": "Redemption",
}

transactions["transaction_type"] = transactions["transaction_type"].map(
    transaction_type_mapping
)

transactions["kyc_status"] = (
    transactions["kyc_status"]
    .astype(str)
    .str.strip()
    .str.title()
)

valid_kyc_statuses = ["Verified", "Pending", "Rejected"]
valid_transaction_types = ["SIP", "Lumpsum", "Redemption"]

invalid_dates = transactions["transaction_date"].isna().sum()
invalid_amounts = transactions["amount_inr"].isna().sum()
non_positive_amounts = (transactions["amount_inr"] <= 0).sum()
invalid_transaction_types = (~transactions["transaction_type"].isin(valid_transaction_types)).sum()
invalid_kyc_statuses = (~transactions["kyc_status"].isin(valid_kyc_statuses)).sum()

print("Invalid transaction dates:", invalid_dates)
print("Invalid amount values:", invalid_amounts)
print("Amount <= 0:", non_positive_amounts)
print("Invalid transaction_type values:", invalid_transaction_types)
print("Invalid KYC status values:", invalid_kyc_statuses)

print("\nTransaction type counts:")
print(transactions["transaction_type"].value_counts(dropna=False))

print("\nKYC status counts:")
print(transactions["kyc_status"].value_counts(dropna=False))

transactions = transactions.dropna(
    subset=["investor_id", "transaction_date", "amfi_code", "transaction_type", "amount_inr"]
)

transactions = transactions[
    transactions["amount_inr"] > 0
]

transactions = transactions[
    transactions["transaction_type"].isin(valid_transaction_types)
]

transactions = transactions[
    transactions["kyc_status"].isin(valid_kyc_statuses)
]

transactions = transactions.sort_values(["transaction_date", "investor_id", "amfi_code"])

print("\nCleaned shape:", transactions.shape)

transactions.to_csv(OUTPUT_FILE, index=False)

print("Saved cleaned file to:", OUTPUT_FILE)
print(transactions.head())