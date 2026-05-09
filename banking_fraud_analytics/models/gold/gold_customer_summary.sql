SELECT
    t.customer_id,
    u.current_age,
    u.gender,
    u.credit_score,
    u.credit_score_category,
    u.yearly_income,
    u.total_debt,
    u.debt_to_income_ratio,
    COUNT(t.transaction_id)                          AS total_transactions,
    SUM(t.amount)                                    AS total_spend,
    AVG(t.amount)                                    AS avg_transaction_amount,
    MAX(t.amount)                                    AS max_transaction_amount,
    SUM(CASE WHEN t.is_fraud = 'Yes' THEN 1 ELSE 0 END) AS total_fraud_transactions,
    ROUND(SUM(CASE WHEN t.is_fraud = 'Yes' THEN 1 ELSE 0 END) * 100.0 
          / COUNT(t.transaction_id), 2)              AS fraud_rate_pct
FROM {{ ref('silver_transactions') }}                AS t
LEFT JOIN {{ ref('silver_users') }}                  AS u
    ON t.customer_id = u.customer_id
GROUP BY
    t.customer_id,
    u.current_age,
    u.gender,
    u.credit_score,
    u.credit_score_category,
    u.yearly_income,
    u.total_debt,
    u.debt_to_income_ratio