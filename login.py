import customtkinter as ctk
from tkinter import messagebox
from extensions import db
from model.user import User


class LoginFrame(ctk.CTkFrame):

    def __init__(self, master, on_login_success):
        super().__init__(master)

        self.on_login_success = on_login_success
        self.pack(expand=True)

        self.show_login_page()

    # ======================
    # Utility
    # ======================
    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    # ======================
    # Login Page
    # ======================
    def show_login_page(self):
        self.clear()

        # ====== Main Container (จัดให้อยู่กลางจอ) ======
        container = ctk.CTkFrame(self, width=350, corner_radius=15)
        container.pack(expand=True)

        # ====== Title ======
        ctk.CTkLabel(
            container,
            text="Welcome Back",
            font=("Arial", 24, "bold")
        ).pack(pady=(30, 5))

        ctk.CTkLabel(
            container,
            text="Login to your account",
            font=("Arial", 13),
            text_color="gray"
        ).pack(pady=(0, 20))

        # ====== Username ======
        self.username_entry = ctk.CTkEntry(
            container,
            placeholder_text="Username",
            width=250,
            height=35,
            corner_radius=10
        )
        self.username_entry.pack(pady=8)

        # ====== Password ======
        self.password_entry = ctk.CTkEntry(
            container,
            placeholder_text="Password",
            show="*",
            width=250,
            height=35,
            corner_radius=10
        )
        self.password_entry.pack(pady=8)

        # ====== Login Button ======
        ctk.CTkButton(
            container,
            text="Login",
            width=250,
            height=40,
            corner_radius=10,
            command=self.login
        ).pack(pady=(20, 10))

        # ====== Register Button ======
        ctk.CTkButton(
            container,
            text="Create Account",
            width=250,
            height=35,
            fg_color="gray",
            hover_color="#555555",
            corner_radius=10,
            command=self.show_register_page
        ).pack(pady=(0, 25))


    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "กรุณากรอกข้อมูลให้ครบ")
            return

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            messagebox.showinfo("Success", "Login สำเร็จ")
            self.on_login_success(user)
        else:
            messagebox.showerror("Error", "Username หรือ Password ไม่ถูกต้อง")

    # ======================
    # Register Page
    # ======================
    def show_register_page(self):
        self.clear()

        ctk.CTkLabel(self, text="Register", font=("Arial", 22)).pack(pady=20)

        self.first_name_entry = ctk.CTkEntry(self, placeholder_text="First Name")
        self.first_name_entry.pack(pady=5)

        self.last_name_entry = ctk.CTkEntry(self, placeholder_text="Last Name")
        self.last_name_entry.pack(pady=5)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=5)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=5)

        ctk.CTkButton(self, text="สมัครสมาชิก", command=self.register)\
            .pack(pady=10)

        ctk.CTkButton(self, text="กลับไป Login", fg_color="gray",
                      command=self.show_login_page)\
            .pack(pady=5)

    def register(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not first_name or not last_name or not username or not password:
            messagebox.showerror("Error", "กรุณากรอกข้อมูลให้ครบ")
            return

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            messagebox.showerror("Error", "Username นี้มีอยู่แล้ว")
            return

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            role=0   # customer เสมอ
        )

        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        messagebox.showinfo("Success", "สมัครสมาชิกสำเร็จ")

        # สมัครเสร็จ → กลับหน้า login
        self.show_login_page()
