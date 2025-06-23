SELECT user_id, clicks
FROM user_clicks_by_day
WHERE day >= '2024-12-01' AND day <= '2024-12-30'
ALLOW FILTERING;