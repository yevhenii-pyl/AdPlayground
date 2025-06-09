SELECT 
    l.name,
    COUNT(e.id) AS total_impressions,
    SUM(e.was_clicked) AS total_clicks,
    ROUND(SUM(e.ad_revenue), 2) AS total_revenue,
    ROUND(SUM(e.ad_revenue) / NULLIF(SUM(e.was_clicked), 0), 2) AS avg_revenue_per_click,
    ROUND(SUM(e.ad_revenue) / COUNT(*) * 1000, 2) AS revenue_per_1000_impressions
FROM ad_events e
JOIN locations l ON e.location_id = l.id
WHERE e.timestamp BETWEEN '2024-12-01' AND '2024-12-30'
GROUP BY l.name
ORDER BY total_revenue DESC;
