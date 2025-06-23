SELECT 
    c.id AS campaign_id,
    c.name AS campaign_name,
    a.id AS advertiser_id,
    a.name AS advertiser_name,
    COUNT(e.id) AS total_impressions,
    SUM(e.was_clicked) AS total_clicks,
    ROUND(SUM(e.ad_cost), 2) AS total_spent,
    ROUND(SUM(e.was_clicked) / COUNT(*) * 100, 2) AS ctr_percent,
    ROUND(SUM(e.ad_cost) / NULLIF(SUM(e.was_clicked), 0), 2) AS avg_cpc,
    ROUND(SUM(e.ad_cost) / COUNT(*) * 1000, 2) AS avg_cpm
FROM ad_events e
JOIN campaigns c ON e.campaign_id = c.id
JOIN advertisers a ON c.advertiser_id = a.id
WHERE e.timestamp BETWEEN '2024-12-01' AND '2024-12-30'
GROUP BY c.id, c.name, a.id, a.name
ORDER BY avg_cpc ASC;
