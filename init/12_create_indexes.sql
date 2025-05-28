-- Indexes for users
CREATE INDEX idx_users_location ON users(location_id);
CREATE INDEX idx_users_gender ON users(gender_id);

-- Indexes for user_interests
CREATE INDEX idx_ui_user ON user_interests(user_id);
CREATE INDEX idx_ui_interest ON user_interests(interest_id);

-- Indexes for campaigns
CREATE INDEX idx_campaigns_advertiser ON campaigns(advertiser_id);
CREATE INDEX idx_campaigns_slot ON campaigns(ad_slot_size_id);

-- Indexes for campaign_interests
CREATE INDEX idx_ci_campaign ON campaign_interests(campaign_id);
CREATE INDEX idx_ci_interest ON campaign_interests(interest_id);

-- Indexes for ad_events
CREATE INDEX idx_events_user ON ad_events(user_id);
CREATE INDEX idx_events_campaign ON ad_events(campaign_id);
CREATE INDEX idx_events_timestamp ON ad_events(timestamp);
CREATE INDEX idx_events_clickcombo ON ad_events(was_clicked, timestamp);
