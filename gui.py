import customtkinter as ctk
from tkinter import messagebox

from app import create_app
from extensions import db
from model.product import Product
from model.order import Order
from model.order_item import OrderItem
from datetime import datetime, timezone
# ---------- Flask ----------
app = create_app()
app.app_context().push()

# ---------- GUI ----------
ctk.set_appearance_mode("dark")

window = ctk.CTk()
window.geometry("900x500")
window.title("Mini POS System")

# Layout แบ่ง 2 คอลัมน์
window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(0, weight=1)

# ---------- Sidebar ----------
sidebar = ctk.CTkFrame(window, width=200)
sidebar.grid(row=0, column=0, sticky="ns")

ctk.CTkLabel(sidebar, text="เมนู", font=("Arial", 18)).pack(pady=20)

# ---------- Content Area ----------
content_frame = ctk.CTkFrame(window)
content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)


# ---------- Functions ----------
def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()


def show_products():
    clear_content()

    products = Product.query.all()

    for p in products:
        row = ctk.CTkFrame(content_frame)
        row.pack(fill="x", pady=5, padx=5)

        # แสดงข้อมูลสินค้า
        ctk.CTkLabel(
            row,
            text=f"{p.name} | ราคา: {p.price} | คงเหลือ: {p.stock}",
            width=300,
            anchor="w"
        ).pack(side="left", padx=10)

        # ช่องใส่จำนวน
        qty_entry = ctk.CTkEntry(row, width=40)
        qty_entry.pack(side="left", padx=65)
        qty_entry.insert(0, "0")

        # ปุ่มซื้อ
        def buy(product=p, entry=qty_entry):
            try:
                qty = int(entry.get())

                if qty <= 0:
                    messagebox.showerror("Error", "จำนวนต้องมากกว่า 0")
                    return

                if product.stock >= qty:

                    # 1️⃣ สร้าง Order
                    order = Order(
                        total_price=product.price * qty
                    )
                    db.session.add(order)
                    db.session.flush()  # เพื่อให้ได้ order.id

                    # 2️⃣ สร้าง OrderItem
                    order_item = OrderItem(
                        order_id=order.id,
                        product_id=product.id,
                        quantity=qty,
                        price=product.price
                    )
                    db.session.add(order_item)

                    # 3️⃣ ลด stock
                    product.stock -= qty

                    db.session.commit()

                    messagebox.showinfo("สำเร็จ", "สร้างคำสั่งซื้อแล้ว")
                    show_products()

                else:
                    messagebox.showerror("Error", "สินค้าไม่พอ")

            except ValueError:
                messagebox.showerror("Error", "กรุณาใส่ตัวเลข")


        ctk.CTkButton(row, text="ซื้อ", command=buy).pack(side="left", padx=5)



def show_orders():
    clear_content()

    orders = Order.query.order_by(Order.id.desc()).all()

    for order in orders:
        frame = ctk.CTkFrame(content_frame)
        frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            frame,
            text=f"Order #{order.id} | รวม: {order.total_price}",
            font=("Arial", 14)
        ).pack(side="left", padx=10)

# ---------- Sidebar Buttons ----------
ctk.CTkButton(sidebar, text="📦 รายการสินค้า", command=show_products).pack(pady=10, padx=10, fill="x")
ctk.CTkButton(sidebar, text="🧾 คำสั่งซื้อ", command=show_orders).pack(pady=10, padx=10, fill="x")

# เริ่มต้นให้แสดงสินค้า
show_products()

window.mainloop()
