SELECT *
FROM user_ad_events
WHERE user_id = %s
ORDER BY event_time DESC
LIMIT 10;