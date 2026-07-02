from pathlib import Path
import subprocess
import sys

BASE_DIR = Path(__file__).resolve().parent

scripts = [
    "data_ingestion.py",
    "live_nav_fetch.py",
    "clean_nav_history.py",
    "clean_scheme_performance.py",
    "prepare_remaining_cleaned_csvs.py",
    "load_sqlite_db.py",
]

for script in scripts:
    print(f"Running {script}...")
    subprocess.run(
        [sys.executable, BASE_DIR / script],
        check=True
    )

print("ETL pipeline completed successfully.")