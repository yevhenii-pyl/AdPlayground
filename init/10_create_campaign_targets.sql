CREATE TABLE campaign_targets (
  id INT AUTO_INCREMENT PRIMARY KEY,
  campaign_id INT NOT NULL,
  interest_id INT,
  min_age INT,
  max_age INT,
  location_id INT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  CONSTRAINT fk_ct_campaign FOREIGN KEY (campaign_id) REFERENCES campaigns(id),
  CONSTRAINT fk_ct_interest FOREIGN KEY (interest_id) REFERENCES interests(id),
  CONSTRAINT fk_ct_location FOREIGN KEY (location_id) REFERENCES locations(id)
);
