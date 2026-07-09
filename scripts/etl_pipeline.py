from pathlib import Path
import subprocess
import sys


BASE_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "data_ingestion.py",
    "live_nav_fetch.py",
    "clean_nav_history.py",
    "clean_scheme_performance.py",
    "prepare_remaining_cleaned_csvs.py",
    "load_sqlite_db.py",
]


def run_script(script_name):
    """Execute an individual ETL step."""
    print(f"\nRunning {script_name}...")

    try:
        subprocess.run(
            [sys.executable, BASE_DIR / script_name],
            check=True
        )
        print(f"{script_name} completed successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Error while executing {script_name}")
        print(e)
        sys.exit(1)


def main():
    print("=" * 50)
    print("Bluestock Mutual Fund ETL Pipeline")
    print("=" * 50)

    for script in SCRIPTS:
        run_script(script)

    print("\nETL Pipeline completed successfully.")


if __name__ == "__main__":
    main()