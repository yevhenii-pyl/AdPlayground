SELECT 
    c.id AS campaign_id,
    c.name AS campaign_name,
    a.name AS advertiser_name,
    c.budget,
    ROUND(SUM(e.ad_cost), 2) AS total_spent,
    ROUND(c.budget - SUM(e.ad_cost), 2) AS remaining_estimated_budget,
    ROUND(SUM(e.ad_cost) / c.budget * 100, 2) AS budget_consumed_percent
FROM campaigns c
JOIN advertisers a ON c.advertiser_id = a.id
JOIN ad_events e ON e.campaign_id = c.id
WHERE e.timestamp BETWEEN '2024-12-01' AND '2024-12-30'
GROUP BY c.id, c.name, a.name, c.budget
ORDER BY budget_consumed_percent DESC
LIMIT 10;