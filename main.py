import tkinter as tk
from tkinter import *
from tkinter import messagebox
import sqlite3
import hashlib


# Password Hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Database Connection
def connect_db():
    return sqlite3.connect("database.db")


# Main Class
class StyleHub:

    def __init__(self, root):
        self.root = root
        self.root.title("StyleHub")

        self.user_id = None
        self.cart = []
        self.wishlist = []

        self.login_screen()

    def login_screen(self):
        self.clear_screen()

        Label(
            self.root,
            text="StyleHub Login",
            font=("Arial", 20)
        ).pack()

        self.username_entry = Entry(self.root)
        self.username_entry.pack()

        self.password_entry = Entry(
            self.root,
            show="*"
        )
        self.password_entry.pack()

        Button(
            self.root,
            text="Login",
            command=self.login
        ).pack()

        Button(
            self.root,
            text="Register",
            command=self.register_screen
        ).pack()

    def register_screen(self):
        ...

    def register(self):
        ...

    def login(self):
        ...

    def products_screen(self):
        ...

    def add_to_cart(self, product):
        ...

    def view_cart(self):
        ...

    def add_to_wishlist(self, item):
        ...

    def checkout(self):
        ...

    def chatbot(self):
        ...

    def admin_dashboard(self):
        ...

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# Register Screen
def register_screen(self):
    self.clear_screen()

    Label(
        self.root,
        text="Register",
        font=("Arial", 20)
    ).pack()

    self.reg_user = Entry(self.root)
    self.reg_user.pack()

    self.reg_pass = Entry(
        self.root,
        show="*"
    )
    self.reg_pass.pack()

    Button(
        self.root,
        text="Create Account",
        command=self.register
    ).pack()


# Register Function
def register(self):
    username = self.reg_user.get()
    password = hash_password(
        self.reg_pass.get()
    )

    conn = connect_db()
    cursor = conn.cursor()

    try:

        cursor.execute("""
        INSERT INTO users
        (username,password)
        VALUES (?,?)
        """, (username, password))

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Account Created"
        )

        self.login_screen()

    except:
        messagebox.showerror(
            "Error",
            "Username Exists"
        )

    conn.close()


# Login Function
def login(self):
    username = self.username_entry.get()
    password = hash_password(
        self.password_entry.get()
    )

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM users
    WHERE username=? AND password=?
    """, (username, password))

    user = cursor.fetchone()

    conn.close()

    if user:

        self.user_id = user[0]

        self.products_screen()

    else:

        messagebox.showerror(
            "Error",
            "Invalid Login"
        )


# Product Catalog
def products_screen(self):
    self.clear_screen()

    Label(
        self.root,
        text="Products",
        font=("Arial", 20)
    ).pack()

    search = Entry(self.root)
    search.pack()

    listbox = Listbox(
        self.root,
        width=60
    )

    listbox.pack()

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM products"
    )

    products = cursor.fetchall()

    for p in products:
        listbox.insert(
            END,
            f"{p[0]} | {p[1]} | ${p[4]}"
        )

    conn.close()


# Shopping Cart



def add_to_cart(self, product):
    self.cart.append(product)

    messagebox.showinfo(
        "Cart",
        "Item Added"
    )



def view_cart(self):
    cart_window = Toplevel()

    cart_window.title("Cart")

    total = 0

    for item in self.cart:
        Label(
            cart_window,
            text=item
        ).pack()

        total += float(
            item.split("$")[1]
        )

    Label(
        cart_window,
        text=f"Total: ${total}"
    ).pack()



def add_to_wishlist(self, item):
    self.wishlist.append(item)

    messagebox.showinfo(
        "Wishlist",
        "Added"
    )


def checkout(self):
    total = 0

    for item in self.cart:
        total += float(
            item.split("$")[1]
        )

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO orders
    (user_id,total)
    VALUES (?,?)
    """, (self.user_id, total))

    conn.commit()
    conn.close()

    self.cart.clear()

    messagebox.showinfo(
        "Order",
        "Order Placed"
    )


# Chatbot
def chatbot(self):
    bot = Toplevel()

    bot.title("Chatbot")

    entry = Entry(bot, width=40)
    entry.pack()

    output = Label(bot, text="")
    output.pack()

    def respond():

        msg = entry.get().lower()

        if "return" in msg:

            response = \
                "Returns accepted within 30 days."

        elif "shipping" in msg:

            response = \
                "Shipping takes 3-5 days."

        elif "size" in msg:

            response = \
                "Sizes range from S to XL."

        else:

            response = \
                "Please contact support."

        output.config(text=response)

    Button(
        bot,
        text="Ask",
        command=respond
    ).pack()



def admin_dashboard(self):
    admin = Toplevel()

    admin.title("Admin")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM products"
    )

    products = cursor.fetchall()

    for p in products:
        Label(
            admin,
            text=f"{p[1]} Stock:{p[5]}"
        ).pack()

    conn.close()



def clear_screen(self):
    for widget in self.root.winfo_children():
        widget.destroy()


root = Tk()

root.geometry("800x600")

app = StyleHub(root)

root.mainloop()
