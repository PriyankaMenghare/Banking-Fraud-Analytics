SELECT
    customer_id,
    current_age,
    retirement_age,
    birth_year,
    birth_month,
    gender,
    address,
    latitude,
    longitude,
    per_capita_income,
    yearly_income,
    total_debt,
    credit_score,
    CASE
        WHEN credit_score >= 800 THEN 'Exceptional'
        WHEN credit_score >= 740 THEN 'Very Good'
        WHEN credit_score >= 670 THEN 'Good'
        WHEN credit_score >= 580 THEN 'Fair'
        ELSE 'Poor'
    END                                     AS credit_score_category,
    num_credit_cards,
    ROUND(total_debt / NULLIF(yearly_income, 0), 2) AS debt_to_income_ratio
FROM {{ ref('bronze_users') }}