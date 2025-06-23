WITH top_spenders AS (
    SELECT 
        a.id AS advertiser_id,
        a.name AS advertiser_name,
        SUM(e.ad_cost) AS total_spent
    FROM ad_events e
    JOIN campaigns c ON e.campaign_id = c.id
    JOIN advertisers a ON c.advertiser_id = a.id
    WHERE e.timestamp BETWEEN '2024-12-01' AND '2024-12-30'
    GROUP BY a.id, a.name
    ORDER BY total_spent DESC
    LIMIT 5
)

SELECT 
    ts.advertiser_id,
    ts.advertiser_name,
    ROUND(SUM(e.ad_cost), 2) AS total_spent,
    ROUND(SUM(e.was_clicked) / COUNT(*) * 100, 2) AS avg_ctr_percent,
    ROUND(SUM(e.ad_cost) / COUNT(*) * 1000, 2) AS avg_cpm,
    ROUND(SUM(e.ad_cost) / SUM(e.was_clicked), 2) AS cpc
FROM ad_events e
JOIN campaigns c ON e.campaign_id = c.id
JOIN advertisers a ON c.advertiser_id = a.id
JOIN top_spenders ts ON a.id = ts.advertiser_id
WHERE e.timestamp BETWEEN '2024-12-01' AND '2024-12-30'
GROUP BY ts.advertiser_id, ts.advertiser_name
ORDER BY total_spent DESC;
