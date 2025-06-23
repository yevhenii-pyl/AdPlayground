SELECT 
    u.id AS user_id,
    COUNT(e.id) AS total_clicks
FROM ad_events e
JOIN users u ON e.user_id = u.id
WHERE e.was_clicked = 1
  AND e.timestamp BETWEEN '2024-12-01' AND '2024-12-30'
GROUP BY u.id
ORDER BY total_clicks DESC
LIMIT 10;
