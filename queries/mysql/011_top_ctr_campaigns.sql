SELECT 
    c.id AS campaign_id,
    c.name AS campaign_name,
    COUNT(*) AS total_impressions,
    SUM(ae.was_clicked) AS total_clicks,
    ROUND(SUM(ae.was_clicked) / COUNT(*) * 100, 2) AS ctr_percent
FROM ad_events ae
JOIN campaigns c ON ae.campaign_id = c.id
WHERE ae.timestamp BETWEEN '2024-12-01' AND '2024-12-30'
GROUP BY c.id, c.name
HAVING total_impressions > 0
ORDER BY ctr_percent DESC
LIMIT 5;