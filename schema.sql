CREATE DATABASE citrus_ai;

USE citrus_ai;

CREATE TABLE diagnoses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  diagnosis_date DATETIME,
  disease_name VARCHAR(100),
  confidence FLOAT,
  temperature FLOAT,
  humidity FLOAT,
  weather VARCHAR(100),
  image_path VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);