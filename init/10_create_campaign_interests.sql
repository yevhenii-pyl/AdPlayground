CREATE TABLE campaign_interests (
  id INT AUTO_INCREMENT PRIMARY KEY,
  campaign_id INT NOT NULL,
  interest_id INT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  CONSTRAINT fk_ci_campaign FOREIGN KEY (campaign_id) REFERENCES campaigns(id),
  CONSTRAINT fk_ci_interest FOREIGN KEY (interest_id) REFERENCES interests(id),
  CONSTRAINT uq_campaign_interest UNIQUE (campaign_id, interest_id)
);
