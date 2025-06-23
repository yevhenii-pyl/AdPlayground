SELECT 
    d.type,
    COUNT(e.id) AS total_impressions,
    SUM(e.was_clicked) AS total_clicks,
    ROUND(SUM(e.was_clicked) / COUNT(*) * 100, 2) AS ctr_percent
FROM ad_events e
JOIN devices d ON e.device_id = d.id
WHERE e.timestamp BETWEEN '2024-12-01' AND '2024-12-30'
GROUP BY d.type
ORDER BY ctr_percent DESC;
