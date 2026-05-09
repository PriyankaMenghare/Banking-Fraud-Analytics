SELECT
    id                  AS transaction_id,
    date                AS transaction_date,
    client_id           AS customer_id,
    card_id,
    CAST(REPLACE(amount, '$', '') AS DECIMAL(18,2))  AS amount,
    use_chip,
    merchant_id,
    merchant_city,
    merchant_state,
    CAST(zip AS BIGINT)  AS zip,
    mcc                 AS mcc_code,
    errors
FROM {{ source('banking_source', 'transactions_data') }}