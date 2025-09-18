USE shopping_C;

-- Insert sample products
INSERT INTO product (name, price, stock) VALUES
('Dell Laptop', 55000.00, 10),
('HP Laptop', 60000.00, 8),
('iPhone 14', 75000.00, 5),
('Samsung Galaxy S23', 68000.00, 7),
('Sony Headphones', 2500.00, 30),
('Logitech Mouse', 1200.00, 25),
('USB-C Charger', 800.00, 50),
('Smartwatch', 5000.00, 15),
('Bluetooth Speaker', 3000.00, 20),
('External Hard Drive', 4500.00, 12);

-- Insert sample carts
INSERT INTO carts (user_id, product_id, quantity) VALUES
(1, 1, 1),   -- User 1 added Dell Laptop
(1, 5, 2),   -- User 1 added 2 Sony Headphones
(2, 3, 1),   -- User 2 added iPhone 14
(2, 7, 3),   -- User 2 added 3 USB-C Chargers
(3, 8, 1);   -- User 3 added 1 Smartwatch

-- Insert sample orders
INSERT INTO orderss (user_id, total_price, status) VALUES
(1, 60000.00, 'Completed'),
(2, 78000.00, 'Pending'),
(3, 5000.00, 'Completed');
