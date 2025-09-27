import sqlite3
from flask import Flask, render_template, redirect, url_for
import os

app = Flask(__name__)
DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "shop.db")

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# ------------------ Routes ------------------
@app.route('/')
def home():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    cart_items = conn.execute('''
        SELECT cart_items.id, cart_items.qty, products.*
        FROM cart_items
        JOIN products ON cart_items.product_id = products.id
        WHERE cart_items.user_id = 1
    ''').fetchall()
    total = sum(item['price'] * item['qty'] for item in cart_items)
    conn.close()
    return render_template('index.html', products=products, cart_items=cart_items, total=total)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM cart_items WHERE product_id = ? AND user_id = 1', (product_id,)).fetchone()
    if item:
        conn.execute('UPDATE cart_items SET qty = qty + 1 WHERE id = ?', (item['id'],))
    else:
        conn.execute('INSERT INTO cart_items (product_id, qty, user_id) VALUES (?, 1, 1)', (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route('/remove/<int:item_id>')
def remove_item(item_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM cart_items WHERE id = ? AND user_id = 1', (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route('/checkout')
def checkout():
    conn = get_db_connection()
    cart_items = conn.execute('''
        SELECT cart_items.id, cart_items.qty, products.id as product_id, products.name, products.price
        FROM cart_items
        JOIN products ON cart_items.product_id = products.id
        WHERE cart_items.user_id = 1
    ''').fetchall()

    if not cart_items:
        conn.close()
        return redirect(url_for('home'))

    total = sum(item['price'] * item['qty'] for item in cart_items)

    # Create order
    cursor = conn.execute('INSERT INTO orders (total) VALUES (?)', (total,))
    order_id = cursor.lastrowid

    # Add order items and clear cart
    for item in cart_items:
        conn.execute('''
            INSERT INTO order_items (order_id, product_id, product_name, product_price, qty)
            VALUES (?, ?, ?, ?, ?)
        ''', (order_id, item['product_id'], item['name'], item['price'], item['qty']))
        conn.execute('DELETE FROM cart_items WHERE id = ?', (item['id'],))

    conn.commit()
    conn.close()
    return "✅ Order Placed Successfully!"

@app.route('/orders')
def orders():
    conn = get_db_connection()
    orders = conn.execute('SELECT * FROM orders ORDER BY created_at DESC').fetchall()
    order_items_dict = {}
    for order in orders:
        items = conn.execute('SELECT * FROM order_items WHERE order_id = ?', (order['id'],)).fetchall()
        order_items_dict[order['id']] = items
    conn.close()
    return render_template('orders.html', orders=orders, order_items_dict=order_items_dict)

# ------------------ Run App ------------------
if __name__ == '__main__':
    from init_db import init_db
    init_db()  # automatically create/update DB
    app.run(debug=True)
