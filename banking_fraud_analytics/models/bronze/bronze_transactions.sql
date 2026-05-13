{{ config(
    materialized='incremental',
    unique_key='transaction_id',
    incremental_strategy='merge',
    on_schema_change='sync_all_columns'
) }}

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

{% if is_incremental() %}
WHERE date > (SELECT MAX(transaction_date) FROM {{ this }})
{% endif %}