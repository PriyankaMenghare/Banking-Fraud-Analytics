SELECT
    t.transaction_id,
    t.transaction_date,
    YEAR(t.transaction_date)                AS transaction_year,
    MONTH(t.transaction_date)               AS transaction_month,
    DAY(t.transaction_date)                 AS transaction_day,
    HOUR(t.transaction_date)                AS transaction_hour,
    t.customer_id,
    t.card_id,
    ABS(t.amount)                           AS amount,
    CASE
        WHEN t.amount < 0 THEN 'debit'
        WHEN t.amount > 0 THEN 'credit'
        ELSE 'zero'
    END                                     AS transaction_direction,
    t.use_chip,
    t.merchant_id,
    t.merchant_city,
    t.merchant_state,
    t.zip,
    t.mcc_code,
    m.description                           AS merchant_category,
    COALESCE(t.errors, 'NO Error')         AS errors,
    CASE
        WHEN t.errors IS NOT NULL THEN TRUE
        ELSE FALSE
    END                                     AS has_error,
    f.is_fraud
FROM {{ ref('bronze_transactions') }}       AS t
LEFT JOIN {{ ref('mcc_codes') }}            AS m
    ON CAST(t.mcc_code AS STRING) = CAST(m.mcc_code AS STRING)
LEFT JOIN {{ ref('train_fraud_labels') }}   AS f
    ON CAST(t.transaction_id AS STRING) = CAST(f.transaction_id AS STRING)