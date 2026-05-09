SELECT
    card_id,
    customer_id,
    card_brand,
    card_type,
    card_number,
    expires,
    has_chip,
    num_cards_issued,
    credit_limit,
    acct_open_date,
    CAST(SPLIT_PART(acct_open_date, '/', 1) AS INT)  AS acct_open_month,
    CAST(SPLIT_PART(acct_open_date, '/', 2) AS INT)  AS acct_open_year,
    year_pin_last_changed,
    card_on_dark_web,
    CASE
        WHEN card_on_dark_web = 'Yes' THEN TRUE
        ELSE FALSE
    END                                     AS is_compromised
FROM {{ ref('bronze_cards') }}