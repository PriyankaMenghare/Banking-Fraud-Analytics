SELECT
    id                  AS customer_id,
    current_age,
    retirement_age,
    birth_year,
    birth_month,
    gender,
    address,
    latitude,
    longitude,
    CAST(REPLACE(per_capita_income, '$', '') AS DECIMAL(18,2))  AS per_capita_income,
    CAST(REPLACE(yearly_income, '$', '') AS DECIMAL(18,2))      AS yearly_income,
    CAST(REPLACE(total_debt, '$', '') AS DECIMAL(18,2))         AS total_debt,
    credit_score,
    num_credit_cards
FROM {{ source('banking_source', 'users_data') }}