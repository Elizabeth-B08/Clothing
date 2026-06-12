from PIL import Image, ImageTk

def show_product_details(self, event):

    selection = self.listbox.curselection()

    if not selection:
        return

    product_id = int(
        self.listbox.get(selection[0]).split("|")[0]
    )

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT name,
           description,
           color,
           image_path,
           price
    FROM products
    WHERE id=?
    """, (product_id,))

    row = cur.fetchone()

    conn.close()

    if row:

        self.desc_label.config(
            text=f"""
Name: {row[0]}

Color: {row[2]}

Price: ${row[4]:.2f}

Description:
{row[1]}
"""
        )

        try:

            img = Image.open(row[3])

            img = img.resize((200, 200))

            self.photo = ImageTk.PhotoImage(img)

            self.image_label.config(
                image=self.photo
            )

        except:
            self.image_label.config(
                image=""
            )