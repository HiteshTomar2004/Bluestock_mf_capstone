import requests
import pandas as pd
from pathlib import Path

RAW_DATA_DIR = Path("data/raw")
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

SCHEMES = {
    "HDFC Top 100 Direct": 125497,
    "SBI Bluechip": 119551,
    "ICICI Bluechip": 120503,
    "Nippon Large Cap": 118632,
    "Axis Bluechip": 119092,
    "Kotak Bluechip": 120841,
}


def fetch_nav_data(scheme_name, scheme_code):
    url = f"https://api.mfapi.in/mf/{scheme_code}"

    print(f"Fetching: {scheme_name} ({scheme_code})")

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    json_data = response.json()

    meta = json_data.get("meta", {})
    nav_data = json_data.get("data", [])

    if not nav_data:
        print(f"No NAV data found for {scheme_name}")
        return

    df = pd.DataFrame(nav_data)

    print("\nMeta Information:")
    print(meta)

    print("\nColumns received:")
    print(df.columns.tolist())

    df["scheme_code"] = scheme_code
    df["scheme_name"] = meta.get("scheme_name")
    df["fund_house"] = meta.get("fund_house")
    df["scheme_category"] = meta.get("scheme_category")
    df["scheme_type"] = meta.get("scheme_type")

    df = df[
        [
            "scheme_code",
            "scheme_name",
            "fund_house",
            "scheme_category",
            "scheme_type",
            "date",
            "nav",
        ]
    ]

    safe_file_name = (
        scheme_name.lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
    )

    output_file = RAW_DATA_DIR / f"live_nav_{scheme_code}_{safe_file_name}.csv"
    df.to_csv(output_file, index=False)

    print(f"Rows fetched: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print(f"Saved to: {output_file}")
    print("\nFirst 5 rows:")
    print(df.head())


for scheme_name, scheme_code in SCHEMES.items():
    try:
        fetch_nav_data(scheme_name, scheme_code)
    except Exception as error:
        print(f"Error fetching {scheme_name}: {error}")