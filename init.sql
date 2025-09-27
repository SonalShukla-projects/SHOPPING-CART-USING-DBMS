-- Products table
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT,
    image_url TEXT
);

-- Cart table
CREATE TABLE cart_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    qty INTEGER DEFAULT 1,
    FOREIGN KEY(product_id) REFERENCES products(id)
);

-- Orders table
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
