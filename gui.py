import customtkinter as ctk
from customtkinter import CTkInputDialog
from tkinter import messagebox

from app import create_app
from extensions import db
from model.product import Product
from model.order import Order
from model.order_item import OrderItem

from login import LoginFrame


# ---------- Flask ----------
app = create_app()
app.app_context().push()

# ---------- GUI ----------
ctk.set_appearance_mode("dark")

window = ctk.CTk()
window.geometry("900x700")
window.title("Mini POS System")

window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(0, weight=1)

current_user = None

# ---------- Frames ----------
sidebar = ctk.CTkFrame(window, width=200)
content_frame = ctk.CTkFrame(window)


# ---------- Utility ----------
def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()


# ---------- Main POS UI ----------
def build_sidebar():
    for widget in sidebar.winfo_children():
        widget.destroy()

    sidebar.grid(row=0, column=0, sticky="ns")

    ctk.CTkLabel(
        sidebar,
        text=f"👤 {current_user.first_name} {current_user.last_name}",
        font=("Arial", 16)
    ).pack(pady=20)

    ctk.CTkButton(
        sidebar,
        text="📦 รายการสินค้า",
        command=show_products
    ).pack(pady=10, padx=10, fill="x")

    ctk.CTkButton(
        sidebar,
        text="🧾 คำสั่งซื้อ",
        command=show_orders
    ).pack(pady=10, padx=10, fill="x")

    if current_user.is_admin():
        ctk.CTkButton(
            sidebar,
            text="➕ เพิ่มสินค้าใหม่",
            command=add_product
        ).pack(pady=10, padx=10, fill="x")

    ctk.CTkButton(
        sidebar,
        text="🚪 Logout",
        fg_color="red",
        command=logout
    ).pack(pady=40, padx=10, fill="x")


def build_content():
    content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)


def build_main_ui():
    build_sidebar()
    build_content()
    show_products()




# ---------- Login Success ----------
def on_login_success(user):
    global current_user
    current_user = user

    login_frame.destroy()
    build_main_ui()



# ---------- Logout ----------
def logout():
    global current_user
    current_user = None

    sidebar.grid_remove()
    content_frame.grid_remove()

    show_login()




# ---------- Show Login ----------
def show_login():
    global login_frame
    login_frame = LoginFrame(window, on_login_success)


# ----------Add Products ----------
def add_product():

    top = ctk.CTkToplevel(window)
    top.title("เพิ่มสินค้า")
    top.geometry("300x300")

    ctk.CTkLabel(top, text="ชื่อสินค้า").pack(pady=5)
    name_entry = ctk.CTkEntry(top)
    name_entry.pack(pady=5)

    ctk.CTkLabel(top, text="ราคาสินค้า").pack(pady=5)
    price_entry = ctk.CTkEntry(top)
    price_entry.pack(pady=5)

    ctk.CTkLabel(top, text="จำนวนสินค้าเริ่มต้น").pack(pady=5)
    stock_entry = ctk.CTkEntry(top)
    stock_entry.pack(pady=5)

    def save_product():
        name = name_entry.get()
        price_str = price_entry.get()
        stock_str = stock_entry.get()

        if not name or not price_str or not stock_str:
            messagebox.showerror("Error", "กรุณากรอกข้อมูลให้ครบ")
            return

        try:
            price = float(price_str)
            stock = int(stock_str)

            new_product = Product(
                name=name,
                price=price,
                stock=stock
            )

            db.session.add(new_product)
            db.session.commit()

            messagebox.showinfo("สำเร็จ", "เพิ่มสินค้าเรียบร้อย")
            top.destroy()
            show_products()

        except ValueError:
            messagebox.showerror("Error", "กรุณาใส่ตัวเลขให้ถูกต้อง")

    ctk.CTkButton(top, text="บันทึก", command=save_product)\
        .pack(pady=20)


# ---------- Products ----------
def show_products():
    clear_content()

    products = Product.query.all()

    for p in products:
        row = ctk.CTkFrame(content_frame)
        row.pack(fill="x", pady=5, padx=5)

        ctk.CTkLabel(
            row,
            text=f"{p.name} | ราคา: {p.price} | คงเหลือ: {p.stock}",
            width=300,
            anchor="w"
        ).pack(side="left", padx=10)

        # =========================
        # ปุ่มซื้อ (ทุก role เห็น)
        # =========================
        def buy(product=p):
            dialog = CTkInputDialog(
                text=f"ใส่จำนวนที่ต้องการซื้อ (คงเหลือ {product.stock})",
                title="ซื้อสินค้า"
            )

            qty_str = dialog.get_input()

            if qty_str is None:
                return

            try:
                qty = int(qty_str)

                if qty <= 0:
                    messagebox.showerror("Error", "จำนวนต้องมากกว่า 0")
                    return

                if product.stock >= qty:

                    order = Order(
                        total_price=product.price * qty,
                        user_id=current_user.id
                    )
                    db.session.add(order)
                    db.session.flush()

                    order_item = OrderItem(
                        order_id=order.id,
                        product_id=product.id,
                        quantity=qty,
                        price=product.price
                    )
                    db.session.add(order_item)

                    product.stock -= qty

                    db.session.commit()

                    messagebox.showinfo("สำเร็จ", "สร้างคำสั่งซื้อแล้ว")
                    show_products()

                else:
                    messagebox.showerror("Error", "สินค้าไม่พอ")

            except ValueError:
                messagebox.showerror("Error", "กรุณาใส่ตัวเลข")

        ctk.CTkButton(
            row,
            text="ซื้อ",
            command=buy
        ).pack(side="left", padx=10)

        # ==================================
        # ปุ่มเพิ่มสต๊อก (Admin เท่านั้น)
        # ==================================
        if current_user.is_admin():

            def add_stock(product=p):
                dialog = CTkInputDialog(
                    text=f"เพิ่มจำนวนสินค้า (ปัจจุบัน {product.stock})",
                    title="เพิ่มสต๊อก"
                )

                qty_str = dialog.get_input()

                if qty_str is None:
                    return

                try:
                    qty = int(qty_str)

                    if qty <= 0:
                        messagebox.showerror("Error", "จำนวนต้องมากกว่า 0")
                        return

                    product.stock += qty
                    db.session.commit()

                    messagebox.showinfo("สำเร็จ", "เพิ่มสต๊อกเรียบร้อย")
                    show_products()

                except ValueError:
                    messagebox.showerror("Error", "กรุณาใส่ตัวเลข")

            ctk.CTkButton(
                row,
                text="➕ เพิ่มสต๊อก",
                fg_color="orange",
                command=add_stock
            ).pack(side="left", padx=5)



# ---------- Orders ----------
def show_orders():
    clear_content()

    if current_user.is_admin():
        orders = Order.query.order_by(Order.id.desc()).all()
    else:
        orders = Order.query.filter_by(user_id=current_user.id)\
                            .order_by(Order.id.desc()).all()

    for order in orders:

        # แปลงเวลาให้อ่านง่าย
        local_time = order.created_at.astimezone()
        formatted_time = local_time.strftime("%d/%m/%Y %H:%M")

        frame = ctk.CTkFrame(content_frame)
        frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            frame,
            text=f"Order #{order.id} | "
                 f"{order.user.first_name} {order.user.last_name} | "
                 f"{formatted_time} | "
                 f"รวม: {order.total_price}",
            font=("Arial", 14)
        ).pack(side="left", padx=10)




# ---------- Start App ----------
show_login()
window.mainloop()
