from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

# -------------------- Models --------------------
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    image_url = db.Column(db.String(100))  # relative to static folder

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    qty = db.Column(db.Integer, default=1)
    product = db.relationship('Product')

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

# -------------------- Routes --------------------
@app.route('/')
def home():
    products = Product.query.limit(5).all()
    cart_items = CartItem.query.all()
    total = sum(item.product.price * item.qty for item in cart_items if item.product)
    return render_template('index.html', products=products, cart_items=cart_items, total=total)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    item = CartItem.query.filter_by(product_id=product_id).first()
    if item:
        item.qty += 1
    else:
        item = CartItem(product_id=product_id, qty=1)
        db.session.add(item)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/remove/<int:item_id>')
def remove_item(item_id):
    item = CartItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/checkout')
def checkout():
    cart_items = CartItem.query.all()
    if not cart_items:
        return redirect(url_for('home'))

    total = sum(item.product.price * item.qty for item in cart_items if item.product)
    order = Order(total=total)
    db.session.add(order)

    # Clear cart
    for item in cart_items:
        db.session.delete(item)
    db.session.commit()

    return "✅ Order Placed Successfully!"

# -------------------- Initialize Database --------------------
def init_db():
    db.create_all()
    if not Product.query.first():
        sample_products = [
            Product(name="Laptop", price=45000, description="High performance laptop", image_url="images/laptop.jpg"),
            Product(name="Headphones", price=1200, description="Noise-cancelling", image_url="images/headphones.jpg"),
            Product(name="Smartphones", price=20000, description="Ultra charging", image_url="images/smartphones.jpg"),
            Product(name="Mouses", price=800, description="Wireless mouse", image_url="images/mouses.jpg"),
            Product(name="Monitors", price=12000, description="Full HD monitor", image_url="images/monitors.jpg")
        ]
        db.session.add_all(sample_products)
        db.session.commit()

# -------------------- Run App --------------------
if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
