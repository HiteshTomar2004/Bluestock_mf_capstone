import pandas as pd
from pathlib import Path

Raw_data_directory = Path("data/raw")

def load_and_inspect_csv():
    csv_files = list(Raw_data_directory.glob("*.csv"))

    if len(csv_files) == 0:
        print("none found")
        return
    print(f"Total csv found: {len(csv_files)}")

    for file_path in csv_files:
        print(f"file: {file_path.name}" + "\n")
        try:  
            df = pd.read_csv(file_path)
            print("\nShape: ")
            print(df.shape)

            print("\nData types: ")
            print(df.dtypes)
            
            print("\nFirst 5 rows: ")
            print(df.head())

            print("\nAnomalies:")
            anomalies = detect_anomalies(df)

            if anomalies:
                for anomaly in anomalies:
                    print(anomaly)
            else:
                print("No obvious anomalies found")
        
        except Exception as error:
            print(f"Error loading {file_path.name}: {error}")

def detect_anomalies(df):
    anomalies = []

    if df.empty:
        anomalies.append("dataset is empty")
    
    duplicate_rows = df.duplicated().sum()
    if duplicate_rows > 0:
        anomalies.append(f"{duplicate_rows} duplicate rows found")

    missing_values = df.isnull().sum()
    columns_with_missing = missing_values[missing_values > 0]

    if not columns_with_missing.empty:
        anomalies.append("Missing values found:")
        for column, count in columns_with_missing.items():
            anomalies.append(f"  - {column}: {count} missing values")

    unnamed_columns = [col for col in df.columns if "Unnamed" in str(col)]
    if unnamed_columns:
        anomalies.append(f"Unnamed columns found: {unnamed_columns}")

    return anomalies       


load_and_inspect_csv()