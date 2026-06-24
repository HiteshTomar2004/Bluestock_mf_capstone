import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

files_to_clean = {
    "01_fund_master.csv": "clean_fund_master.csv",
    "03_aum_by_fund_house.csv": "clean_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv": "clean_monthly_sip_inflows.csv",
    "05_category_inflows.csv": "clean_category_inflows.csv",
    "06_industry_folio_count.csv": "clean_industry_folio_count.csv",
    "09_portfolio_holdings.csv": "clean_portfolio_holdings.csv",
    "10_benchmark_indices.csv": "clean_benchmark_indices.csv",
}

date_columns = {
    "01_fund_master.csv": ["launch_date"],
    "03_aum_by_fund_house.csv": ["date"],
    "04_monthly_sip_inflows.csv": ["month"],
    "05_category_inflows.csv": ["month"],
    "06_industry_folio_count.csv": ["month"],
    "09_portfolio_holdings.csv": ["portfolio_date"],
    "10_benchmark_indices.csv": ["date"],
}

for raw_file_name, output_file_name in files_to_clean.items():
    raw_path = RAW_DIR / raw_file_name
    output_path = PROCESSED_DIR / output_file_name

    df = pd.read_csv(raw_path)

    print("\n" + "=" * 80)
    print(f"Cleaning {raw_file_name}")
    print("Original shape:", df.shape)

    df = df.drop_duplicates()

    for column in date_columns.get(raw_file_name, []):
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce")

    df.to_csv(output_path, index=False)

    print("Cleaned shape:", df.shape)
    print("Saved to:", output_path)