# Bluestock Mutual Fund Data Dictionary

## Overview

This data dictionary documents the cleaned datasets and SQLite star schema used in the Bluestock Mutual Fund capstone project. The data sources include fund metadata, NAV history, investor transactions, scheme performance, AUM by fund house, portfolio holdings, SIP inflows, category inflows, folio counts, and benchmark index values.

## Source Files

| Source File | Processed File | Description |
|---|---|---|
| `01_fund_master.csv` | `clean_fund_master.csv` | Master list of mutual fund schemes and scheme metadata |
| `02_nav_history.csv` | `clean_nav_history.csv` | Historical NAV values by AMFI scheme code and date |
| `03_aum_by_fund_house.csv` | `clean_aum_by_fund_house.csv` | AUM data at fund house / AMC level |
| `04_monthly_sip_inflows.csv` | `clean_monthly_sip_inflows.csv` | Monthly SIP inflows and SIP account trends |
| `05_category_inflows.csv` | `clean_category_inflows.csv` | Monthly net inflows by mutual fund category |
| `06_industry_folio_count.csv` | `clean_industry_folio_count.csv` | Mutual fund folio count by category |
| `07_scheme_performance.csv` | `clean_scheme_performance.csv` | Scheme-level return, risk, rating, expense ratio, and AUM metrics |
| `08_investor_transactions.csv` | `clean_investor_transactions.csv` | Investor-level transaction records |
| `09_portfolio_holdings.csv` | `clean_portfolio_holdings.csv` | Scheme-level stock holdings and sector exposure |
| `10_benchmark_indices.csv` | `clean_benchmark_indices.csv` | Historical benchmark index closing values |

## SQLite Schema Tables

## `dim_fund`

Dimension table containing scheme-level fund metadata.

| Column | Data Type | Business Definition | Source |
|---|---|---|---|
| `amfi_code` | INTEGER | Unique AMFI scheme identifier | `01_fund_master.csv` |
| `fund_house` | TEXT | Mutual fund house / AMC name | `01_fund_master.csv` |
| `scheme_name` | TEXT | Full mutual fund scheme name | `01_fund_master.csv` |
| `category` | TEXT | Broad scheme category such as Equity or Debt | `01_fund_master.csv` |
| `sub_category` | TEXT | Detailed scheme category such as Large Cap, Small Cap, Gilt, Liquid, etc. | `01_fund_master.csv` |
| `plan` | TEXT | Scheme plan type such as Regular or Direct | `01_fund_master.csv` |
| `launch_date` | DATE | Date on which the scheme was launched | `01_fund_master.csv` |
| `benchmark` | TEXT | Benchmark index used for scheme comparison | `01_fund_master.csv` |
| `expense_ratio_pct` | REAL | Annual expense ratio percentage charged by the scheme | `01_fund_master.csv` |
| `exit_load_pct` | REAL | Exit load percentage charged on early redemption | `01_fund_master.csv` |
| `min_sip_amount` | INTEGER | Minimum SIP investment amount in INR | `01_fund_master.csv` |
| `min_lumpsum_amount` | INTEGER | Minimum lumpsum investment amount in INR | `01_fund_master.csv` |
| `fund_manager` | TEXT | Name of the scheme fund manager | `01_fund_master.csv` |
| `risk_category` | TEXT | Scheme risk level such as Low, Moderate, High, or Very High | `01_fund_master.csv` |
| `sebi_category_code` | TEXT | SEBI category code assigned to the scheme | `01_fund_master.csv` |

## `dim_date`

Date dimension table used for time-based joins and analysis.

| Column | Data Type | Business Definition | Source |
|---|---|---|---|
| `date_key` | INTEGER | Date identifier in YYYYMMDD format | Derived |
| `full_date` | DATE | Calendar date | Derived from date columns |
| `year` | INTEGER | Calendar year | Derived |
| `quarter` | INTEGER | Calendar quarter | Derived |
| `month` | INTEGER | Calendar month number | Derived |
| `month_name` | TEXT | Calendar month name | Derived |
| `day` | INTEGER | Day of month | Derived |

## `fact_nav`

Fact table containing daily NAV values.

| Column | Data Type | Business Definition | Source |
|---|---|---|---|
| `nav_id` | INTEGER | Auto-generated NAV record identifier | Derived |
| `amfi_code` | INTEGER | AMFI scheme identifier linked to `dim_fund` | `02_nav_history.csv` |
| `date_key` | INTEGER | Date identifier linked to `dim_date` | `02_nav_history.csv` |
| `nav` | REAL | Net Asset Value of the scheme for the date | `02_nav_history.csv` |

## `fact_transactions`

Fact table containing investor transaction records.

| Column | Data Type | Business Definition | Source |
|---|---|---|---|
| `transaction_id` | INTEGER | Auto-generated transaction identifier | Derived |
| `investor_id` | TEXT | Unique investor identifier | `08_investor_transactions.csv` |
| `date_key` | INTEGER | Transaction date linked to `dim_date` | `08_investor_transactions.csv` |
| `amfi_code` | INTEGER | AMFI scheme identifier linked to `dim_fund` | `08_investor_transactions.csv` |
| `transaction_type` | TEXT | Type of transaction: SIP, Lumpsum, or Redemption | `08_investor_transactions.csv` |
| `amount_inr` | REAL | Transaction amount in Indian Rupees | `08_investor_transactions.csv` |
| `state` | TEXT | Investor state | `08_investor_transactions.csv` |
| `city` | TEXT | Investor city | `08_investor_transactions.csv` |
| `city_tier` | TEXT | City tier classification | `08_investor_transactions.csv` |
| `age_group` | TEXT | Investor age group | `08_investor_transactions.csv` |
| `gender` | TEXT | Investor gender | `08_investor_transactions.csv` |
| `annual_income_lakh` | REAL | Investor annual income in lakh INR | `08_investor_transactions.csv` |
| `payment_mode` | TEXT | Payment mode used for transaction | `08_investor_transactions.csv` |
| `kyc_status` | TEXT | Investor KYC status such as Verified or Pending | `08_investor_transactions.csv` |

## `fact_performance`

Fact table containing scheme-level performance and risk metrics.

| Column | Data Type | Business Definition | Source |
|---|---|---|---|
| `performance_id` | INTEGER | Auto-generated performance record identifier | Derived |
| `amfi_code` | INTEGER | AMFI scheme identifier linked to `dim_fund` | `07_scheme_performance.csv` |
| `return_1yr_pct` | REAL | One-year scheme return percentage | `07_scheme_performance.csv` |
| `return_3yr_pct` | REAL | Three-year scheme return percentage | `07_scheme_performance.csv` |
| `return_5yr_pct` | REAL | Five-year scheme return percentage | `07_scheme_performance.csv` |
| `benchmark_3yr_pct` | REAL | Three-year benchmark return percentage | `07_scheme_performance.csv` |
| `alpha` | REAL | Excess return compared to benchmark after risk adjustment | `07_scheme_performance.csv` |
| `beta` | REAL | Sensitivity of scheme returns to benchmark movements | `07_scheme_performance.csv` |
| `sharpe_ratio` | REAL | Risk-adjusted return measure using total volatility | `07_scheme_performance.csv` |
| `sortino_ratio` | REAL | Risk-adjusted return measure using downside volatility | `07_scheme_performance.csv` |
| `std_dev_ann_pct` | REAL | Annualized standard deviation percentage | `07_scheme_performance.csv` |
| `max_drawdown_pct` | REAL | Maximum peak-to-trough decline percentage | `07_scheme_performance.csv` |
| `aum_crore` | REAL | Scheme assets under management in crore INR | `07_scheme_performance.csv` |
| `expense_ratio_pct` | REAL | Scheme annual expense ratio percentage | `07_scheme_performance.csv` |
| `morningstar_rating` | INTEGER | Scheme rating from 1 to 5 | `07_scheme_performance.csv` |

## `fact_aum`

Fact table containing AMC-level AUM values.

| Column | Data Type | Business Definition | Source |
|---|---|---|---|
| `aum_id` | INTEGER | Auto-generated AUM record identifier | Derived |
| `date_key` | INTEGER | Reporting date linked to `dim_date` | `03_aum_by_fund_house.csv` |
| `fund_house` | TEXT | Mutual fund house / AMC name | `03_aum_by_fund_house.csv` |
| `aum_lakh_crore` | REAL | AUM in lakh crore INR | `03_aum_by_fund_house.csv` |
| `aum_crore` | REAL | AUM in crore INR | `03_aum_by_fund_house.csv` |
| `num_schemes` | INTEGER | Number of schemes managed by the fund house | `03_aum_by_fund_house.csv` |

## Cleaning Notes

| Dataset | Cleaning / Validation Performed |
|---|---|
| `nav_history` | Parsed dates, sorted by AMFI code and date, removed duplicates, validated NAV greater than 0, forward-filled NAV for holidays/weekends |
| `investor_transactions` | Standardised transaction types, parsed transaction dates, validated amount greater than 0, checked KYC status values |
| `scheme_performance` | Converted return and performance fields to numeric, checked expense ratio range from 0.1% to 2.5%, flagged return and expense anomalies during cleaning |
| Remaining datasets | Removed duplicates and standardised date columns where applicable |

## Data Quality Summary

All 10 source CSV files were successfully cleaned and saved to `data/processed/`. The NAV history, investor transactions, and scheme performance datasets passed validation checks with no invalid dates, non-positive NAV values, invalid transaction amounts, or invalid scheme performance values. The SQLite database was loaded successfully, and row-count verification confirmed that all loaded table counts matched the cleaned source datasets.