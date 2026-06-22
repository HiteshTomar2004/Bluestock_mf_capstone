import pandas as pd
fund_master = pd.read_csv("data/raw/01_fund_master.csv")

print(
    fund_master[
        fund_master["scheme_name"]
        .str.contains("Bluechip", case=False, na=False)
    ][["amfi_code", "scheme_name"]]
)

# the script was used to check if the AMFI codes inside the fund master were equivalent to those obatined from the API's