import sqlite3
import os

DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "shop.db")

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()

    # Create tables if they don't exist
    conn.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        description TEXT,
        image_url TEXT
    )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS cart_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        qty INTEGER DEFAULT 1,
        user_id INTEGER DEFAULT 1,
        FOREIGN KEY(product_id) REFERENCES products(id)
    )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total REAL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_id INTEGER,
        product_name TEXT,
        product_price REAL,
        qty INTEGER,
        FOREIGN KEY(order_id) REFERENCES orders(id),
        FOREIGN KEY(product_id) REFERENCES products(id)
    )
    """)

    # ------------------ Remove old 'Headphone' entries ------------------
    conn.execute("DELETE FROM products WHERE name = 'Headphone'")

    # ------------------ Insert sample products if table is empty ------------------
    existing_products = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    if existing_products == 0:
        sample_products = [
            ('Laptop', 45000, 'High performance laptop', "images/laptop.jpg"),
            ('Smartphone', 20000, 'Ultra charging', "images/smartphone.jpg"),
            ('Mouse', 800, 'Wireless mouse', "images/mouse.jpg"),
            ('Monitor', 12000, 'Full HD monitor', "images/monitor.jpg"),
            ('Smartwatch', 5000, 'Heart rate detector', "images/smartwatch.jpg")
        ]

        conn.executemany(
            'INSERT INTO products (name, price, description, image_url) VALUES (?, ?, ?, ?)',
            sample_products
        )
        print("Inserted sample products.")

    conn.commit()
    conn.close()
    print("Database initialized/updated successfully.")

if __name__ == "__main__":
    init_db()
