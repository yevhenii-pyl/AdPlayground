SELECT
  campaign_id,
  day,
  clicks,
  impressions,
  (clicks * 100.0) / impressions AS ctr
FROM campaign_stats_by_day
WHERE day >= '2024-12-01' AND day <= '2024-12-30'
ALLOW FILTERING;