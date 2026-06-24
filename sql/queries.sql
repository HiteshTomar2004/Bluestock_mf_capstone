-- 1. Top 5 funds by AUM
SELECT
    f.scheme_name,
    f.fund_house,
    p.aum_crore
FROM fact_performance p
JOIN dim_fund f
    ON p.amfi_code = f.amfi_code
ORDER BY p.aum_crore DESC
LIMIT 5;

-- 2. Average NAV per month
SELECT
    f.scheme_name,
    d.year,
    d.month,
    ROUND(AVG(n.nav), 2) AS avg_monthly_nav
FROM fact_nav n
JOIN dim_fund f
    ON n.amfi_code = f.amfi_code
JOIN dim_date d
    ON n.date_key = d.date_key
GROUP BY
    f.scheme_name,
    d.year,
    d.month
ORDER BY
    f.scheme_name,
    d.year,
    d.month;

-- 3. SIP YoY growth
SELECT
    year,
    total_sip_amount,
    previous_year_sip_amount,
    ROUND(
        ((total_sip_amount - previous_year_sip_amount) * 100.0)
        / previous_year_sip_amount,
        2
    ) AS yoy_growth_pct
FROM (
    SELECT
        d.year,
        SUM(t.amount_inr) AS total_sip_amount,
        LAG(SUM(t.amount_inr)) OVER (ORDER BY d.year) AS previous_year_sip_amount
    FROM fact_transactions t
    JOIN dim_date d
        ON t.date_key = d.date_key
    WHERE t.transaction_type = 'SIP'
    GROUP BY d.year
)
WHERE previous_year_sip_amount IS NOT NULL;

-- 4. Transactions by state
SELECT
    state,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount_inr), 2) AS total_amount_inr
FROM fact_transactions
GROUP BY state
ORDER BY total_transactions DESC;

-- 5. Funds with expense ratio less than 1%
SELECT
    f.scheme_name,
    f.fund_house,
    f.category,
    f.sub_category,
    p.expense_ratio_pct
FROM fact_performance p
JOIN dim_fund f
    ON p.amfi_code = f.amfi_code
WHERE p.expense_ratio_pct < 1
ORDER BY p.expense_ratio_pct ASC;

-- 6. Top 5 funds by 3-year return
SELECT
    f.scheme_name,
    f.fund_house,
    f.category,
    f.sub_category,
    p.return_3yr_pct
FROM fact_performance p
JOIN dim_fund f
    ON p.amfi_code = f.amfi_code
ORDER BY p.return_3yr_pct DESC
LIMIT 5;

-- 7. Average transaction amount by transaction type
SELECT
    transaction_type,
    COUNT(*) AS transaction_count,
    ROUND(AVG(amount_inr), 2) AS average_amount_inr,
    ROUND(SUM(amount_inr), 2) AS total_amount_inr
FROM fact_transactions
GROUP BY transaction_type
ORDER BY total_amount_inr DESC;

-- 8. KYC status distribution
SELECT
    kyc_status,
    COUNT(*) AS investor_transaction_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage_share
FROM fact_transactions
GROUP BY kyc_status
ORDER BY investor_transaction_count DESC;

-- 9. Monthly redemption amount trend
SELECT
    d.year,
    d.month,
    ROUND(SUM(t.amount_inr), 2) AS total_redemption_amount
FROM fact_transactions t
JOIN dim_date d
    ON t.date_key = d.date_key
WHERE t.transaction_type = 'Redemption'
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- 10. Risk category wise average return and expense ratio
SELECT
    f.risk_category,
    COUNT(*) AS fund_count,
    ROUND(AVG(p.return_1yr_pct), 2) AS avg_1yr_return_pct,
    ROUND(AVG(p.return_3yr_pct), 2) AS avg_3yr_return_pct,
    ROUND(AVG(p.expense_ratio_pct), 2) AS avg_expense_ratio_pct
FROM fact_performance p
JOIN dim_fund f
    ON p.amfi_code = f.amfi_code
GROUP BY f.risk_category
ORDER BY avg_3yr_return_pct DESC;