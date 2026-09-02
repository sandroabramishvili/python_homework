-- სასტუმროს მონაცემთა ბაზა

-- შექმენით სასტუმროს მონაცემთა ბაზა. მონაცემთა ბაზა უნდა შედგებოდეს რამდენიმე ცხრილისგან და 
-- გამოყენებული უნდა იყოს მხოლოდ ერთი-მრავალთან (one-to-many) კავშირები.

CREATE DATABASE hotel_management;

-- მონაცემთა ბაზაში უნდა არსებობდეს შემდეგი ცხრილები:

-- სასტუმროები (hotels) — ინახავს სასტუმროს სახელწოდებას, ქალაქს და ვარსკვლავების რაოდენობას
-- (ვარსკვალების რაოდენობაზე გააკეთეთ ვალიდაცია -  უნდა იყოს 1-დან 5-ის ჩათვლით). ერთ სასტუმროს შეუძლია ჰქონდეს რამდენიმე ნომერი.

CREATE TABLE hotels (
    hotel_id SERIAL PRIMARY KEY,
    hotel_name VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    stars INT NOT NULL,
    CONSTRAINT check_stars CHECK (stars BETWEEN 1 AND 5)
);

-- ნომრები (rooms) — ინახავს ოთახის ნომერს, სართულს და ღირებულებას ერთ ღამეზე. თითოეული ნომერი ეკუთვნის მხოლოდ ერთ სასტუმროს, 
-- ხოლო ერთ სასტუმროს შეუძლია ჰქონდეს მრავალი ნომერი.

CREATE TABLE rooms (
    room_id         SERIAL PRIMARY KEY,
    room_number     INT NOT NULL,
    floor           INT NOT NULL,
    price_per_night DECIMAL(10,2) NOT NULL,
    hotel_id        INT NOT NULL,
    CONSTRAINT fk_rooms_hotel
        FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id)
        ON DELETE CASCADE
);

-- სტუმრები (guests) — ინახავს სტუმრის სახელს, გვარს და ტელეფონის ნომერს. თითოეული სტუმარი ცხოვრობს ერთ ნომერში, ხოლო ერთ 
-- ნომერში შეიძლება იყოს რამდენიმე სტუმარი.

CREATE TABLE guests (
    guest_id         SERIAL PRIMARY KEY,
    first_name       VARCHAR(50) NOT NULL,
    last_name        VARCHAR(50) NOT NULL,
    telephone_number VARCHAR(9),
    room_id          INT NOT NULL,
    CONSTRAINT fk_guests_room
        FOREIGN KEY (room_id) REFERENCES rooms(room_id)
        ON DELETE CASCADE
);

-- სერვისები (services) — ინახავს ნომრისთვის შეკვეთილ სერვისებს და მათ ღირებულებას. ერთ ნომერს შეიძლება ჰქონდეს რამდენიმე სერვისი.

CREATE TABLE services (
    service_id    SERIAL PRIMARY KEY,
    service_name  VARCHAR(50) NOT NULL,
    price         DECIMAL(10,2) NOT NULL,
    room_id       INT NOT NULL,
    CONSTRAINT fk_services_room
        FOREIGN KEY (room_id) REFERENCES rooms(room_id)
        ON DELETE CASCADE
);

-- ცხრილებს შორის კავშირები უნდა განხორციელდეს PRIMARY KEY და FOREIGN KEY გამოყენებით. წაშლის დროს დამოკიდებული ჩანაწერები უნდა 
-- იშლებოდეს ავტომატურად.

-- ცხრილების შექმნის შემდეგ დაამატეთ მონაცემები:

-- მინიმუმ ორი სასტუმრო;

INSERT INTO hotels (name, city, stars) VALUES
('The Telegraph Hotel', 'Tbilisi', 5),
('Tbilisi Marriot Hotel', 'Tbilisi', 4),
('Hilton Batumi', 'Batumi', 4);

-- თითო სასტუმროზე მინიმუმ სამი ნომერი;

INSERT INTO rooms (room_number, floor, price_per_night, hotel_id) VALUES
('101', 1, 150.00, 1),
('102', 1, 180.00, 1),
('201', 2, 220.00, 1),
('101', 1, 100.00, 2),
('102', 1, 120.00, 2),
('301', 3, 250.00, 2),
('101', 1, 230.00, 3),
('402', 4, 300.00, 3),
('404', 4, 300.00, 3);

-- თითო ნომერზე მინიმუმ ორი სტუმარი;

INSERT INTO guests (first_name, last_name, telephone_number, room_id) VALUES
('Natali', 'Buadze', '599234378', 1),
('Salome', 'Chachanidze', '595943943', 1),
('Mariam', 'Barbakadze', '577549090', 2),
('Sandro', 'Tsivtsivadze', '599509123', 2),
('Saba', 'Razmadze', '557337866', 3),
('Shalva', 'Mosia', '598478999', 3),
('Luka', 'Razmadze', '599444988', 4),
('Ninutsa', 'Metreveli', '595776599', 4),
('Oto', 'Lejava', '555555000', 5),
('Elene', 'Pataraia', '555555111', 5),
('Beka', 'Tsiklauri', '555666222', 6),
('Salome', 'Metreveli', '555666333', 6),
('Nika', 'Beridze', '555111222', 7),
('Ana', 'Kldiashvili', '555111333', 7),
('Giorgi', 'Lomidze', '555222444', 8),
('Mari', 'Gogoladze', '555222555', 8),
('Misho', 'Kvichidze', '577594545', 9),
('Levan', 'Kvichidze', '577597889', 9);

-- თითო ნომერზე მინიმუმ ორი სერვისი.

INSERT INTO services (service_name, price, room_id) VALUES
('Breakfast', 15.00, 1),
('Spa', 60.00, 1),
('Laundry', 10.00, 2),
('Airport Transfer', 40.00, 2),
('Breakfast', 15.00, 3),
('Minibar', 20.00, 3),
('Breakfast', 12.00, 4),
('Laundry', 8.00, 4),
('Spa', 55.00, 5),
('Minibar', 18.00, 5),
('Breakfast', 15.00, 6),
('Laundry', 10.00, 6),
('Breakfast', 14.00, 7),
('Laundry', 9.00, 7),
('Entertainment', 25.00, 8),
('Laundry', 12.00, 8),
('Massage', 50.00, 9),
('Therapy', 70.00, 9);

-- მონაცემების დამატების შემდეგ დაწერეთ SQL მოთხოვნები, რომლებიც დააბრუნებს:

-- ყველა ნომერს შესაბამისი სასტუმროს სახელთან ერთად;

SELECT r.room_id, r.room_number, r.floor, r.price_per_night, h.hotel_name
FROM rooms r
JOIN hotels h ON r.hotel_id = h.hotel_id;

-- ყველა სტუმარს მისი ნომრის ნომრითა და სასტუმროს სახელით;

SELECT g.first_name, g.last_name, r.room_number, h.hotel_name
FROM guests g
JOIN rooms r ON g.room_id = r.room_id
JOIN hotels h ON r.hotel_id = h.hotel_id;

-- კონკრეტული სასტუმროს ყველა სტუმარს;

SELECT h.hotel_name, g.first_name, g.last_name, r.room_number
FROM guests g
JOIN rooms r ON g.room_id = r.room_id
JOIN hotels h ON r.hotel_id = h.hotel_id
WHERE h.hotel_name = 'The Telegraph Hotel';

-- თითო სასტუმროში არსებული ნომრების რაოდენობას;

SELECT h.hotel_name, COUNT(r.room_id) AS room_count
FROM hotels h
LEFT JOIN rooms r ON h.hotel_id = r.hotel_id
GROUP BY h.hotel_id, h.hotel_name;

-- იმ ნომრებს, რომელთათვისაც სერვისი ჯერ არ არის შეკვეთილი.

DELETE FROM services
WHERE room_id = 3;

SELECT r.room_id, r.room_number, h.hotel_name
FROM rooms r
JOIN hotels h ON r.hotel_id = h.hotel_id
LEFT JOIN services s ON r.room_id = s.room_id
WHERE s.service_id IS NULL;

-- დავალების ბოლოს შეასრულეთ შემდეგი ოპერაციები:

-- წაშალეთ ერთი ნომერი და დააკვირდით, როგორ აისახება ეს მასთან დაკავშირებულ სტუმრებსა და სერვისებზე;

-- ჯერ ვნახულობ რა ხდება სტუმრების და სერვისების ცხრილებში წაშლამდე.

SELECT * FROM guests WHERE room_id = 8;
SELECT * FROM services WHERE room_id = 8;

-- ოთახის წაშლა ცხრილიდან

DELETE FROM rooms WHERE room_id = 8;

-- შედეგი

SELECT * FROM guests WHERE room_id = 8;
SELECT * FROM services WHERE room_id = 8;

-- შეცვალეთ კონკრეტული ნომრის ღირებულება;

UPDATE rooms
SET price_per_night = 180.00
WHERE room_id = 2;

-- ერთი სტუმარი გადააწერეთ სხვა ნომერზე.

UPDATE guests
SET room_id = 5
WHERE guest_id = 7;
