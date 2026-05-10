{{ config(
    materialized='incremental',
    unique_key='transaction_id',
    incremental_strategy='merge',
    on_schema_change='sync_all_columns'
) }}

SELECT
    t.transaction_id,
    t.transaction_date,
    t.customer_id,
    t.card_id,
    t.amount,
    t.transaction_direction,
    t.merchant_category,
    t.merchant_city,
    t.merchant_state,
    t.use_chip,
    t.has_error,
    t.is_fraud,
    CASE
        WHEN t.amount > 10000                        THEN 'high_amount'
        WHEN t.has_error = TRUE                      THEN 'transaction_error'
        WHEN t.transaction_hour BETWEEN 0 AND 4      THEN 'unusual_hours'
        WHEN c.is_compromised = TRUE                 THEN 'compromised_card'
        WHEN u.credit_score_category = 'Poor'        THEN 'poor_credit'
        ELSE 'clean'
    END                                              AS fraud_flag,
    u.credit_score,
    u.credit_score_category,
    c.card_type,
    c.card_brand,
    c.is_compromised
FROM {{ ref('silver_transactions') }}                AS t
LEFT JOIN {{ ref('silver_users') }}                  AS u
    ON t.customer_id = u.customer_id
LEFT JOIN {{ ref('silver_cards') }}                  AS c
    ON t.card_id = c.card_id

{% if is_incremental() %}
WHERE t.transaction_date > (SELECT MAX(transaction_date) FROM {{ this }})
{% endif %}