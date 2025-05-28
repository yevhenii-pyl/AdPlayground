CREATE TABLE users (
  id INT PRIMARY KEY,
  age INT CHECK (age >= 0),
  gender_id INT NOT NULL,
  location_id INT NOT NULL,
  signup_date DATE NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  CONSTRAINT fk_user_gender FOREIGN KEY (gender_id) REFERENCES genders(id),
  CONSTRAINT fk_user_location FOREIGN KEY (location_id) REFERENCES locations(id)
);
