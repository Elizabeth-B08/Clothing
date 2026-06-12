import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT DEFAULT 'customer'
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    description TEXT,
    color TEXT,
    image_path TEXT,
    price REAL,
    stock INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS cart(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product_id INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS wishlist(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product_id INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    total REAL
)
""")

cursor.execute("SELECT COUNT(*) FROM products")

if cursor.fetchone()[0] == 0:
    products = [
        ("Classic T-Shirt", "Shirts", "Soft cotton shirt", 19.99, 50),
            ("Premium Hoodie", "Outerwear", "Warm fleece hoodie", 49.99, 25),
            ("Slim Jeans", "Pants", "Stretch denim jeans", 59.99, 30),
            ("Running Shoes", "Shoes", "Lightweight sneakers", 79.99, 20),
            ("Baseball Cap", "Accessories", "Adjustable cap", 14.99, 40)
    ]

    cursor.executemany("""
    INSERT INTO products
    (name,category, description, price, stock)
    VALUES (?,?,?,?,?)
    """, products)

conn.commit()
conn.close()

print("Database created.")

