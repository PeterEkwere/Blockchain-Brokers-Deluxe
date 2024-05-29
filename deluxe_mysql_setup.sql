-- Prepares a mysql server for deluxe crypto site

-- Drop database
DROP DATABASE IF EXISTS deluxe_db;

-- Create database + user if doesn't exist
CREATE DATABASE IF NOT EXISTS deluxe_db;
CREATE USER IF NOT EXISTS 'admin'@'localhost';
SET PASSWORD FOR 'admin'@'localhost' = 'Admin1234';
GRANT ALL ON deluxe_db.* TO 'admin'@'localhost';
GRANT SELECT ON performance_schema.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;