import sqlite3
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

PROCESSED_DIR = Path("data/processed")
SQL_DIR = Path("sql")
DB_FILE = Path("bluestock_mf.db")
SCHEMA_FILE = SQL_DIR / "schema.sql"

if DB_FILE.exists():
    DB_FILE.unlink()

engine = create_engine(f"sqlite:///{DB_FILE}")

print("CREATING SQLITE DATABASE")

with sqlite3.connect(DB_FILE) as connection:
    schema_sql = SCHEMA_FILE.read_text()
    connection.executescript(schema_sql)

print("Database schema created:", DB_FILE)

fund_master = pd.read_csv(PROCESSED_DIR / "clean_fund_master.csv")
nav_history = pd.read_csv(PROCESSED_DIR / "clean_nav_history.csv")
transactions = pd.read_csv(PROCESSED_DIR / "clean_investor_transactions.csv")
performance = pd.read_csv(PROCESSED_DIR / "clean_scheme_performance.csv")
aum = pd.read_csv(PROCESSED_DIR / "clean_aum_by_fund_house.csv")

fund_master["launch_date"] = pd.to_datetime(fund_master["launch_date"], errors="coerce")
nav_history["date"] = pd.to_datetime(nav_history["date"], errors="coerce")
transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"], errors="coerce")
aum["date"] = pd.to_datetime(aum["date"], errors="coerce")

all_dates = pd.concat(
    [
        nav_history["date"],
        transactions["transaction_date"],
        aum["date"],
        fund_master["launch_date"],
    ],
    ignore_index=True,
).dropna().drop_duplicates()

dim_date = pd.DataFrame({"full_date": all_dates})
dim_date["full_date"] = pd.to_datetime(dim_date["full_date"])
dim_date = dim_date.sort_values("full_date").reset_index(drop=True)

dim_date["date_key"] = dim_date["full_date"].dt.strftime("%Y%m%d").astype(int)
dim_date["year"] = dim_date["full_date"].dt.year
dim_date["quarter"] = dim_date["full_date"].dt.quarter
dim_date["month"] = dim_date["full_date"].dt.month
dim_date["month_name"] = dim_date["full_date"].dt.month_name()
dim_date["day"] = dim_date["full_date"].dt.day

date_key_map = dict(zip(dim_date["full_date"].dt.date, dim_date["date_key"]))

dim_fund = fund_master.copy()

fact_nav = nav_history.copy()
fact_nav["date_key"] = fact_nav["date"].dt.date.map(date_key_map)
print("Missing NAV date_keys:",
      fact_nav["date_key"].isna().sum())
fact_nav = fact_nav[["amfi_code", "date_key", "nav"]]

fact_transactions = transactions.copy()
fact_transactions["date_key"] = fact_transactions["transaction_date"].dt.date.map(date_key_map)
print("Missing Transaction date_keys:",
      fact_transactions["date_key"].isna().sum())
fact_transactions = fact_transactions[
    [
        "investor_id",
        "date_key",
        "amfi_code",
        "transaction_type",
        "amount_inr",
        "state",
        "city",
        "city_tier",
        "age_group",
        "gender",
        "annual_income_lakh",
        "payment_mode",
        "kyc_status",
    ]
]

fact_performance = performance.copy()

columns_to_drop = []
if "expense_ratio_flag" in fact_performance.columns:
    columns_to_drop.append("expense_ratio_flag")
if "return_anomaly_flag" in fact_performance.columns:
    columns_to_drop.append("return_anomaly_flag")

fact_performance = fact_performance.drop(columns=columns_to_drop)

fact_performance = fact_performance[
    [
        "amfi_code",
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
]

fact_aum = aum.copy()
fact_aum["date_key"] = fact_aum["date"].dt.date.map(date_key_map)
print("Missing AUM date_keys:",
      fact_aum["date_key"].isna().sum())
fact_aum = fact_aum[
    [
        "date_key",
        "fund_house",
        "aum_lakh_crore",
        "aum_crore",
        "num_schemes",
    ]
]

print("\nLoading tables...")

dim_fund.to_sql("dim_fund", engine, if_exists="append", index=False)
dim_date.to_sql("dim_date", engine, if_exists="append", index=False)
fact_nav.to_sql("fact_nav", engine, if_exists="append", index=False)
fact_transactions.to_sql("fact_transactions", engine, if_exists="append", index=False)
fact_performance.to_sql("fact_performance", engine, if_exists="append", index=False)
fact_aum.to_sql("fact_aum", engine, if_exists="append", index=False)

print("Tables loaded successfully.")

print("ROW COUNT VERIFICATION")

tables = {
    "dim_fund": len(dim_fund),
    "dim_date": len(dim_date),
    "fact_nav": len(fact_nav),
    "fact_transactions": len(fact_transactions),
    "fact_performance": len(fact_performance),
    "fact_aum": len(fact_aum),
}

with engine.connect() as connection:
    for table_name, expected_count in tables.items():
        actual_count = pd.read_sql(f"SELECT COUNT(*) AS count FROM {table_name}", connection)["count"][0]
        status = "MATCH" if actual_count == expected_count else "MISMATCH"
        print(f"{table_name}: expected={expected_count}, actual={actual_count}, status={status}")

print("\nSQLite database saved as:", DB_FILE)