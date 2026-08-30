-- Database creation
CREATE DATABASE cars;

-- Table creation
CREATE TABLE cars (
	car_id 				SERIAL PRIMARY KEY,
	brand 				VARCHAR(50) NOT NULL,
	model 				VARCHAR(50) NOT NULL,
	release_year 		INT NOT NULL,
	vin_code			VARCHAR(17) UNIQUE,
	date_added			DATE NOT NULL DEFAULT CURRENT_DATE,
	engine_volume		NUMERIC(3,1) CHECK (engine_volume > 0.5),
	mileage_km			INTEGER,
	is_customs_cleared  BOOLEAN,
	price				NUMERIC(10,2),
	description			TEXT,
	is_sold				BOOLEAN
);

-- Insert sample data
INSERT INTO cars (brand, model, release_year, vin_code, engine_volume, mileage_km, is_customs_cleared, price, description, is_sold)
VALUES
('Toyota', 'Camry', 2018, '4T1BF1FK5JU123456', 2.5, 65000, TRUE, 18500.00, 'Well maintained sedan, one owner.', FALSE),
('Honda', 'Civic', 2020, '2HGFC2F59LH123457', 1.5, 32000, TRUE, 21000.00, 'Low mileage, excellent condition.', FALSE),
('Ford', 'Focus', 2015, '1FADP3F20FL123458', 2.0, 98000, FALSE, 9500.00, 'Some cosmetic wear, runs great.', TRUE),
('BMW', '320i', 2019, 'WBA8E9G50KNU12345', 2.0, 45000, TRUE, 27500.00, 'Sport package, leather interior.', FALSE),
('Mercedes-Benz', 'C200', 2017, 'WDDWF4KB5HR123456', 2.0, 72000, TRUE, 24500.00, 'Full service history.', FALSE),
('Nissan', 'Altima', 2016, '1N4AL3AP5GC123457', 2.5, 88000, FALSE, 11000.00, 'Reliable daily driver.', TRUE),
('Hyundai', 'Elantra', 2021, 'KMHD84LF5MU123458', 1.6, 15000, TRUE, 19500.00, 'Almost new, still under warranty.', FALSE),
('Kia', 'Sportage', 2019, 'KNDPMCAC5K7123459', 2.4, 54000, TRUE, 20500.00, 'SUV, all-wheel drive.', FALSE),
('Volkswagen', 'Passat', 2014, '1VWBH7A32EC123460', 1.8, 120000, FALSE, 8200.00, 'High mileage but well cared for.', TRUE),
('Audi', 'A4', 2020, 'WAUENAF40LN123461', 2.0, 28000, TRUE, 29900.00, 'Premium trim, low mileage.', FALSE),
('Mazda', 'CX-5', 2018, 'JM3KFBCM5J0123462', 2.5, 61000, TRUE, 19800.00, 'Great fuel economy, clean title.', FALSE);

-- Queries
SELECT * FROM cars;

SELECT brand, model, release_year, price FROM cars;

SELECT * FROM cars WHERE brand = 'Toyota';

SELECT * FROM cars WHERE release_year >= 2018 AND release_year <= 2020;

SELECT * FROM cars WHERE is_sold = false;

-- Add a new column for car color
ALTER TABLE cars ADD COLUMN color VARCHAR(50);

-- Update the color column for each car
UPDATE cars SET color = 'White'      WHERE car_id = 1;  -- Toyota Camry
UPDATE cars SET color = 'Black'      WHERE car_id = 2;  -- Honda Civic
UPDATE cars SET color = 'Silver'     WHERE car_id = 3;  -- Ford Focus
UPDATE cars SET color = 'Blue'       WHERE car_id = 4;  -- BMW 320i
UPDATE cars SET color = 'Gray'       WHERE car_id = 5;  -- Mercedes-Benz C200
UPDATE cars SET color = 'Red'        WHERE car_id = 6;  -- Nissan Altima
UPDATE cars SET color = 'White'      WHERE car_id = 7;  -- Hyundai Elantra
UPDATE cars SET color = 'Dark Green' WHERE car_id = 8;  -- Kia Sportage
UPDATE cars SET color = 'Beige'      WHERE car_id = 9;  -- Volkswagen Passat
UPDATE cars SET color = 'Black'      WHERE car_id = 10; -- Audi A4
UPDATE cars SET color = 'Silver'     WHERE car_id = 11; -- Mazda CX-5

-- Final query to display car_id, brand, model, and color
SELECT car_id, brand, model, color FROM cars;