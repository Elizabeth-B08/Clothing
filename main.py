import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# -------------------------
# Theme Colors
# -------------------------
BG = "#121212"
CARD = "#1E1E1E"
ACCENT = "#4F46E5"


# -------------------------
# Database
# -------------------------
def connect_db():
    return sqlite3.connect("database.db")


def init_db():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
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

    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total REAL
    )
    """)

    # Add sample products if table is empty
    cur.execute("SELECT COUNT(*) FROM products")

    if cur.fetchone()[0] == 0:
        cur.executemany("""
        INSERT INTO products
        (name, category, description, price, stock)
        VALUES (?, ?, ?, ?, ?)
        """, [
            ("Classic T-Shirt", "Shirts", "Soft cotton shirt", 19.99, 50),
            ("Premium Hoodie", "Outerwear", "Warm fleece hoodie", 49.99, 25),
            ("Slim Jeans", "Pants", "Stretch denim jeans", 59.99, 30),
            ("Running Shoes", "Shoes", "Lightweight sneakers", 79.99, 20),
            ("Baseball Cap", "Accessories", "Adjustable cap", 14.99, 40)
        ])

    conn.commit()
    conn.close()


# -------------------------
# Main App
# -------------------------
class StyleHub:

    def __init__(self, root):
        self.root = root

        self.root.title("Forever 21")
        self.root.geometry("1000x700")
        self.root.configure(bg=BG)

        self.cart = []

        self.setup_styles()
        self.products_screen()

    # -------------------------
    # Styling
    # -------------------------
    def setup_styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except:
            pass

        style.configure(
            "Header.TLabel",
            font=("Segoe UI", 24, "bold")
        )

        style.configure(
            "TButton",
            font=("Segoe UI", 11, "bold"),
            padding=10
        )

        style.configure(
            "TLabel",
            font=("Segoe UI", 11)
        )

    # -------------------------
    # Utilities
    # -------------------------
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # -------------------------
    # Products Screen
    # -------------------------
    def products_screen(self):

        self.clear_screen()

        header = tk.Frame(
            self.root,
            bg=BG
        )

        header.pack(fill="x", pady=15)

        ttk.Label(
            header,
            text="🛍 Forever 21 Store",
            style="Header.TLabel"
        ).pack()

        self.cart_label = ttk.Label(
            header,
            text="Cart: 0 items"
        )

        self.cart_label.pack(pady=5)

        ttk.Button(
            header,
            text="View Cart",
            command=self.view_cart
        ).pack()

        self.listbox = tk.Listbox(
            self.root,
            bg=CARD,
            fg="white",
            font=("Segoe UI", 11),
            width=80,
            height=20,
            selectbackground=ACCENT,
            relief="flat"
        )

        self.listbox.pack(pady=20)

        self.load_products()

        ttk.Button(
            self.root,
            text="Add Selected To Cart",
            command=self.add_selected_product
        ).pack()

    # -------------------------
    # Load Products
    # -------------------------
    def load_products(self):

        self.listbox.delete(0, tk.END)

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, name, price FROM products"
        )

        rows = cur.fetchall()

        conn.close()

        for row in rows:
            self.listbox.insert(
                tk.END,
                f"{row[0]} | {row[1]} | ${row[2]:.2f}"
            )

    # -------------------------
    # Add To Cart
    # -------------------------
    def add_selected_product(self):

        selection = self.listbox.curselection()

        if not selection:
            messagebox.showwarning(
                "Selection Required",
                "Please select a product."
            )
            return

        item = self.listbox.get(selection[0])

        self.cart.append(item)

        self.cart_label.config(
            text=f"Cart: {len(self.cart)} items"
        )

        messagebox.showinfo(
            "Added",
            "Product added to cart."
        )

    # -------------------------
    # View Cart
    # -------------------------
    def view_cart(self):

        win = tk.Toplevel(self.root)

        win.title("Shopping Cart")
        win.geometry("500x500")
        win.configure(bg=BG)

        ttk.Label(
            win,
            text="Your Cart",
            style="Header.TLabel"
        ).pack(pady=15)

        total = 0

        for item in self.cart:

            ttk.Label(
                win,
                text=item
            ).pack(pady=3)

            try:
                total += float(
                    item.split("$")[-1]
                )
            except:
                pass

        ttk.Label(
            win,
            text=f"Total: ${total:.2f}",
            style="Header.TLabel"
        ).pack(pady=20)

        ttk.Button(
            win,
            text="Checkout",
            command=lambda: self.checkout(win)
        ).pack(pady=10)

    # -------------------------
    # Checkout
    # -------------------------
    def checkout(self, cart_window):

        if not self.cart:

            messagebox.showwarning(
                "Empty Cart",
                "Your cart is empty."
            )

            return

        total = 0

        for item in self.cart:

            try:
                total += float(
                    item.split("$")[-1]
                )
            except:
                pass

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO orders (total) VALUES (?)",
            (total,)
        )

        conn.commit()
        conn.close()

        self.cart.clear()

        self.cart_label.config(
            text="Cart: 0 items"
        )

        messagebox.showinfo(
            "Order Complete",
            f"Thank you for your purchase!\n\nTotal: ${total:.2f}"
        )

        cart_window.destroy()


# -------------------------
# Run App
# -------------------------
if __name__ == "__main__":

    init_db()

    root = tk.Tk()

    app = StyleHub(root)

    root.mainloop()