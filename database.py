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
    size TEXT,
    color TEXT,
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
        ("Nike Hoodie", "M", "Black", 79.99, 10),
        ("Adidas Shirt", "L", "White", 34.99, 15),
        ("Puma Shorts", "S", "Blue", 29.99, 20)
    ]

    cursor.executemany("""
    INSERT INTO products
    (name,size,color,price,stock)
    VALUES (?,?,?,?,?)
    """, products)

conn.commit()
conn.close()

print("Database created.")

