-- შექმენით ახალი ბაზა და დაიწყეთ მუშაობა
-- უნდა შექმნათ ცხრილები, გაითვალისწინეთ, ყველა ცხრილს უნდა ჰქონდეს აიდები და 
-- სათითაოდ აღარ ჩამოვწერ ყველა ცხრილისთვის

-- შექმენით ცხრილი customers რომელსაც ექნება შემდეგი ველები:
-- სახელი, არ უნდა იყოს განუსაზღვრელი
-- ემაილი, არ უნდა იყოს განუსაზღვრელი და უნდა იყოს უნიკალური

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name        VARCHAR(50) NOT NULL,
    email       VARCHAR(100) NOT NULL UNIQUE
);

-- შექმენით ცხრილი customer_profiles, რომელსაც ექნება one-to-one კავშირი customers ცხრილთან
-- დამატებით ექნება ველი ტელეფონის ნომერი და მისამართი

CREATE TABLE customer_profiles (
    profile_id  SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL UNIQUE
                REFERENCES customers(customer_id)
                ON DELETE CASCADE,
    phone       VARCHAR(9),
    address     VARCHAR(100)
);

-- შექმენით ცხრილი suppliers(მომწოდებელი) შემდეგი ველებით:
-- სახელი, არ უნდა იყოს განუსაზღვრელი
-- საკონტაქტო ემაილი, არ უნდა იყოს განუსაზღვრელი და უნდა იყოს უნიკალური

CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    name        VARCHAR(50) NOT NULL,
    email       VARCHAR(100) NOT NULL UNIQUE
);

-- შექმენით ცხრილი products, ველებით:
-- დასახელება, არ უნდა იყოს განუსაზღვრელი
-- ფასი, არ უნდა იყოს განუსაზღვრელი
-- მომწოდებელი(დაკავშირებული უნდა იყოს suppliers ცხრილთან, ერთი მომწოდებელი - მრავალი პროდუქტი)

CREATE TABLE products (
    product_id  SERIAL PRIMARY KEY,
    name        VARCHAR(50) NOT NULL,
    price       INTEGER NOT NULL,
    supplier_id INTEGER NOT NULL
                REFERENCES suppliers(supplier_id)
                ON DELETE RESTRICT
);

-- many-to-many კავშირისთვის გამოიყენეთ ქვემოთ მოცემული სქემა
-- შეკვეთები უნდა დაუკავშიროთ პროდუქტებს, ანუ თითო შეკვეთა შეიძლება მოიცავდეს ბევრ პროდუქტს და 
-- ასევე ერთი პროდუქტი შეიძლება 
-- იყოს ბევრ შეკვეთაში, ანუ უნდა შექმნათ orders ცხრილი და ე.წ. შუამავალი ცხრილი, შუამავალ 
-- ცხრილს დაუმატეთ პროდუქტის რაოდენობა
-- orders ცხრილს უნდა ჰქონდეს შეკვეთის თარიღი და ასევე უნდა იყოს მიბმული მომხმარებელთან 
-- (ერთი მომხმარებელი - მრავალი შეკვეთა)

CREATE TABLE orders (
    order_id    SERIAL PRIMARY KEY,
    order_date  TIMESTAMP NOT NULL DEFAULT NOW(),
    customer_id INTEGER NOT NULL
                REFERENCES customers(customer_id)
                ON DELETE CASCADE
);

CREATE TABLE order_items (
    id  SERIAL PRIMARY KEY,
    order_id    INTEGER NOT NULL
                REFERENCES orders(order_id)
                ON DELETE CASCADE,
    product_id  INTEGER NOT NULL
                REFERENCES products(product_id)
                ON DELETE RESTRICT,
    quantity    INTEGER NOT NULL CHECK (quantity > 0),
    UNIQUE(order_id, product_id)
);

-- დაგენერირებული სემპლ დატა რომ შევამოწმო

INSERT INTO customers (name, email) VALUES
    ('Nino Kapanadze',   'nino.kapanadze@example.com'),
    ('Giorgi Beridze',   'giorgi.beridze@example.com'),
    ('Ana Kiknadze',     'ana.kiknadze@example.com'),
    ('Levan Tsereteli',  'levan.tsereteli@example.com');

INSERT INTO customer_profiles (customer_id, phone, address) VALUES
    (1, '555112233', '12 Rustaveli Ave, Tbilisi'),
    (2, '555445566', '7 Chavchavadze St, Tbilisi'),
    (3, '555778899', '25 Agmashenebeli Ave, Kutaisi');

-- მომმარაგებლები დავამატოთ ჯერ, რადგან პროდუქტების მაგიდაში დარეფერენსებულია

INSERT INTO suppliers (name, email) VALUES
    ('Kakheti Wine House',     'contact@kakhetiwine.ge'),
    ('Tbilisi Foods Ltd',      'sales@tbilisifoods.ge'),
    ('Adjara Fresh Produce',   'info@adjarafresh.ge');

INSERT INTO products (name, price, supplier_id) VALUES
    ('Saperavi Red Wine 750ml',         18.50,  1),
    ('Rkatsiteli White Wine 750ml',     16.00,  1),
    ('Georgian Cheese (Sulguni) 500g',  7.20,   2),
    ('Churchkhela (pack of 5)',         5.90,   2),
    ('Fresh Hazelnuts 1kg',             12.00,  3),
    ('Fresh Almonds 500g',              9.75,   3);

INSERT INTO orders (order_date, customer_id) VALUES
    ('2026-08-15 10:30:00', 1),
    ('2026-08-20 14:00:00', 2),
    ('2026-08-25 09:15:00', 1),
    ('2026-08-28 17:45:00', 4);

INSERT INTO order_items (order_id, product_id, quantity) VALUES
-- ნინოს შეკვეთა
    (1, 1, 2),   -- 2x Saperavi Red Wine
    (1, 3, 1),   -- 1x Sulguni Cheese

-- გიორგის შეკვეთა
    (2, 2, 1),   -- 1x Rkatsiteli White Wine
    (2, 4, 3),   -- 3x Churchkhela
    (2, 5, 1),   -- 1x Fresh Hazelnuts

-- ნინოს მეორე შეკვეთა
    (3, 6, 2),   -- 2x Adjarian Khachapuri Kit

-- ლევანის შეკვეთა
    (4, 1, 1),   -- 1x Saperavi Red Wine
    (4, 3, 2);   -- 2x Sulguni Cheese

-- ვნახოთ ყველა ორდერი, ორდერის გამკეთებელი, რა შეუკვეთეს და რამდენი.
SELECT c.name, o.order_date, p.name, oi.quantity FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.product_id
ORDER BY o.order_date;

-- ვინ რამდენი შეკვეთა გააკეთა?
SELECT c.name, COUNT(o.order_id) AS order_count FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.name;

-- რა რაოდენობით გაიყიდა თითოუელი პროდუქტი
SELECT p.name, SUM(oi.quantity) AS total_quantity_sold
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.name;