CREATE TABLE ad_events (
  id CHAR(36) PRIMARY KEY,
  campaign_id INT NOT NULL,
  ad_slot_size_id INT NOT NULL,
  user_id INT NOT NULL,
  device_id INT NOT NULL,
  location_id INT NOT NULL,
  timestamp DATETIME NOT NULL,
  bid_amount FLOAT NOT NULL CHECK (bid_amount >= 0),
  ad_cost FLOAT NOT NULL CHECK (ad_cost >= 0),
  was_clicked BOOLEAN NOT NULL,
  click_timestamp DATETIME NULL,
  ad_revenue FLOAT NOT NULL CHECK (ad_revenue >= 0),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  CONSTRAINT fk_event_campaign FOREIGN KEY (campaign_id) REFERENCES campaigns(id),
  CONSTRAINT fk_event_slot FOREIGN KEY (ad_slot_size_id) REFERENCES ad_slot_sizes(id),
  CONSTRAINT fk_event_user FOREIGN KEY (user_id) REFERENCES users(id),
  CONSTRAINT fk_event_device FOREIGN KEY (device_id) REFERENCES devices(id),
  CONSTRAINT fk_event_location FOREIGN KEY (location_id) REFERENCES locations(id)
);
