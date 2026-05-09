SELECT
    transaction_year,
    transaction_month,
    COUNT(transaction_id)                            AS total_transactions,
    SUM(amount)                                      AS total_amount,
    AVG(amount)                                      AS avg_amount,
    SUM(CASE WHEN transaction_direction = 'debit' 
        THEN amount ELSE 0 END)                      AS total_debits,
    SUM(CASE WHEN transaction_direction = 'credit' 
        THEN amount ELSE 0 END)                      AS total_credits,
    SUM(CASE WHEN is_fraud = 'Yes' THEN 1 ELSE 0 END) AS total_fraud,
    ROUND(SUM(CASE WHEN is_fraud = 'Yes' THEN 1 ELSE 0 END) * 100.0
          / COUNT(transaction_id), 2)                AS fraud_rate_pct
FROM {{ ref('silver_transactions') }}
GROUP BY
    transaction_year,
    transaction_month
ORDER BY
    transaction_year,
    transaction_month