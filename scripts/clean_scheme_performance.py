import pandas as pd
from pathlib import Path

RAW_FILE = Path("data/raw/07_scheme_performance.csv")
PROCESSED_DIR = Path("data/processed")
OUTPUT_FILE = PROCESSED_DIR / "clean_scheme_performance.csv"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

performance = pd.read_csv(RAW_FILE)

print("Original shape:", performance.shape)

numeric_columns = [
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct",
    "benchmark_3yr_pct",
    "alpha",
    "beta",
    "sharpe_ratio",
    "sortino_ratio",
    "std_dev_ann_pct",
    "max_drawdown_pct",
    "aum_crore",
    "expense_ratio_pct",
    "morningstar_rating",
]

for column in numeric_columns:
    performance[column] = pd.to_numeric(performance[column], errors="coerce")

print("\nMissing or non-numeric values after numeric conversion:")
for column in numeric_columns:
    missing_count = performance[column].isna().sum()
    print(f"{column}: {missing_count}")

expense_ratio_anomalies = performance[
    (performance["expense_ratio_pct"] < 0.1)
    | (performance["expense_ratio_pct"] > 2.5)
]

rating_anomalies = performance[
    (performance["morningstar_rating"] < 1)
    | (performance["morningstar_rating"] > 5)
]

negative_aum = performance[performance["aum_crore"] <= 0]

extreme_return_anomalies = performance[
    (performance["return_1yr_pct"].abs() > 100)
    | (performance["return_3yr_pct"].abs() > 100)
    | (performance["return_5yr_pct"].abs() > 100)
]

print("\nExpense ratio anomalies outside 0.1% to 2.5%:")
print(expense_ratio_anomalies[["amfi_code", "scheme_name", "expense_ratio_pct"]])

print("\nMorningstar rating anomalies outside 1 to 5:")
print(rating_anomalies[["amfi_code", "scheme_name", "morningstar_rating"]])

print("\nAUM anomalies where aum_crore <= 0:")
print(negative_aum[["amfi_code", "scheme_name", "aum_crore"]])

print("\nExtreme return anomalies where absolute return > 100%:")
print(
    extreme_return_anomalies[
        ["amfi_code", "scheme_name", "return_1yr_pct", "return_3yr_pct", "return_5yr_pct"]
    ]
)

performance = performance.dropna(subset=["amfi_code", "scheme_name"])

performance["expense_ratio_flag"] = performance["expense_ratio_pct"].apply(
    lambda value: "Anomaly" if value < 0.1 or value > 2.5 else "Valid"
)

performance["return_anomaly_flag"] = performance.apply(
    lambda row: "Anomaly"
    if abs(row["return_1yr_pct"]) > 100
    or abs(row["return_3yr_pct"]) > 100
    or abs(row["return_5yr_pct"]) > 100
    else "Valid",
    axis=1
)

print("\nExpense ratio flag counts:")
print(performance["expense_ratio_flag"].value_counts())

print("\nReturn anomaly flag counts:")
print(performance["return_anomaly_flag"].value_counts())

print("\nCleaned shape:", performance.shape)

performance.to_csv(OUTPUT_FILE, index=False)

print("Saved cleaned file to:", OUTPUT_FILE)
print(performance.head())