SELECT advertiser_id, region, SUM(spend) AS total_spend
FROM advertiser_spend_by_day
WHERE region = %s AND day >= '2024-12-01' AND day <= '2024-12-30'
ALLOW FILTERING;
