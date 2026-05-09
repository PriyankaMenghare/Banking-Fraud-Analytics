SELECT
    id                      AS card_id,
    client_id               AS customer_id,
    card_brand,
    card_type,
    card_number,
    expires,
    cvv,
    has_chip,
    num_cards_issued,
    CAST(REPLACE(credit_limit, '$', '') AS DECIMAL(18,2))  AS credit_limit,
    acct_open_date,
    year_pin_last_changed,
    card_on_dark_web
FROM {{ source('banking_source', 'cards_data') }}