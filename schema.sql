-- Create database if not exists
CREATE DATABASE IF NOT EXISTS weather_tracker;

-- Use the database
USE weather_tracker;

-- Create events table
CREATE TABLE IF NOT EXISTS events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(255) NOT NULL,
    venue VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    event_date DATE NOT NULL
);

-- Create weather_forecasts table
CREATE TABLE IF NOT EXISTS weather_forecasts (
    forecast_id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    temperature DECIMAL(5,2),
    weather_condition VARCHAR(255),
    weather_risk VARCHAR(255),
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);