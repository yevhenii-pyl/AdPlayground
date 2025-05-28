CREATE TABLE user_interests (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  interest_id INT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  CONSTRAINT fk_ui_user FOREIGN KEY (user_id) REFERENCES users(id),
  CONSTRAINT fk_ui_interest FOREIGN KEY (interest_id) REFERENCES interests(id),
  CONSTRAINT uq_user_interest UNIQUE (user_id, interest_id)
);
