SELECT 
    l.name,
    COUNT(e.id) AS total_clicks,
    ROUND(SUM(e.ad_revenue), 2) AS revenue_from_clicks,
    ROUND(AVG(e.ad_revenue), 2) AS avg_revenue_per_click
FROM ad_events e
JOIN locations l ON e.location_id = l.id
WHERE e.was_clicked = 1
  AND e.timestamp BETWEEN '2024-12-01' AND '2024-12-30'
GROUP BY l.name
ORDER BY revenue_from_clicks DESC;
