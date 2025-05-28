CREATE TABLE campaigns (
  id INT PRIMARY KEY, 
  name VARCHAR(100) NOT NULL,
  advertiser_id INT NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  ad_slot_size_id INT NOT NULL,
  budget FLOAT NOT NULL CHECK (budget >= 0),
  remaining_budget FLOAT NOT NULL CHECK (remaining_budget >= 0),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  CONSTRAINT fk_campaign_advertiser FOREIGN KEY (advertiser_id) REFERENCES advertisers(id),
  CONSTRAINT fk_campaign_adslot FOREIGN KEY (ad_slot_size_id) REFERENCES ad_slot_sizes(id)
);
