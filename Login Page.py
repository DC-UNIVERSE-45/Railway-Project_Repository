#                                        LOGIN PAGE

import os
import re
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector as sq
from PIL import Image, ImageTk, ImageFilter, ImageEnhance

# ---------------- DB CONFIG ----------------
DB_CONFIG = dict(
    host="localhost",
    user="root",
    password="Debjit@08#2025",
    database="Railway_Reservation_System"
)

def get_db_connection():
    return sq.connect(**DB_CONFIG)

# ---------------- PASSWORD VALIDATION ----------------
def is_strong_password(password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(pattern, password)

# ---------------- BACKGROUND IMAGE ----------------
def create_background_image(filename="image.png"):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        script_dir = os.getcwd()

    image_path = os.path.join(script_dir, filename)

    if not os.path.isfile(image_path):
        root.configure(bg="#f0f0f0")
        return

    try:
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        img = Image.open(image_path).resize((w, h), Image.LANCZOS)
        img_blurred = img.filter(ImageFilter.GaussianBlur(radius=5))
        enhancer = ImageEnhance.Brightness(img_blurred)
        img_final = enhancer.enhance(0.8)

        bg_img = ImageTk.PhotoImage(img_final)
        bg_label = tk.Label(root, image=bg_img)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        root._bg_img = bg_img
    except Exception as ex:
        root.configure(bg="#f0f0f0")
        messagebox.showerror("Background error", str(ex))

# ---------------- LOGIN FUNCTION ----------------
def login():
    uid = entry_uid.get().strip()
    password = entry_password.get().strip()

    if not uid or not password:
        messagebox.showerror("Input Error", "UID and Password are required.")
        return

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT UID FROM users WHERE UID = %s AND password = %s",
                    (uid, password))
        result = cur.fetchone()

        if result:
            messagebox.showinfo("✅ Success", f"Welcome! Logged in with UID: {uid}")
            root.destroy()
        else:
            messagebox.showerror("❌ Login Failed", "Invalid UID or password.")
            entry_password.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if conn:
            conn.close()

# ---------------- REGISTER FUNCTION ----------------
def register():
    name = entry_reg_name.get().strip()
    age = entry_reg_age.get().strip()
    dob = entry_reg_dob.get().strip()
    gender = gender_var.get()
    state = entry_reg_state.get().strip()
    password = entry_reg_password.get().strip()

    if not all([name, age, dob, gender, state, password]):
        messagebox.showerror("Input Error", "All fields are required.")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Input Error", "Age must be a number.")
        return

    if not is_strong_password(password):
        messagebox.showerror("Password Error",
                             "Password must be at least 8 characters long and include:\n"
                             "- One uppercase letter\n- One lowercase letter\n"
                             "- One number\n- One special character (@$!%*?&)")
        return

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (name, age, dob, gender, state, password)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, age, dob, gender, state, password))
        conn.commit()

        cur.execute("SELECT LAST_INSERT_ID()")
        uid = cur.fetchone()[0]

        messagebox.showinfo("🎉 Registration Successful",
                            f"Welcome {name}!\n\nYour UID is: {uid}\n(Use this UID to login)")
        clear_register_fields()
        show_login_frame()
    except Exception as e:
        if conn:
            conn.rollback()
        messagebox.showerror("Database Error", str(e))
    finally:
        if conn:
            conn.close()

def clear_register_fields():
    entry_reg_name.delete(0, tk.END)
    entry_reg_age.delete(0, tk.END)
    entry_reg_dob.delete(0, tk.END)
    entry_reg_state.delete(0, tk.END)
    entry_reg_password.delete(0, tk.END)
    gender_var.set("Male")

# ---------------- UI TOGGLE ----------------
def show_login_frame():
    register_frame.pack_forget()
    login_frame.pack(fill="both", expand=True)
    entry_uid.focus()
    title_label.config(text="🔐 User Login")

def show_register_frame():
    login_frame.pack_forget()
    register_frame.pack(fill="both", expand=True)
    entry_reg_name.focus()
    title_label.config(text="✍️ User Registration")

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Railway Management - Login/Register")
root.state("zoomed")

create_background_image("image.png")

main_frame = tk.Frame(root, bg="#FFFFFF", relief="raised", bd=3)
main_frame.place(relx=0.5, rely=0.5, relwidth=0.4, relheight=0.6, anchor=tk.CENTER)

title_label = tk.Label(main_frame, text="🔐 User Login",
                       font=("Helvetica", 22, "bold"),
                       bg="#FFFFFF", fg="#222")
title_label.pack(pady=20)

# ---------------- LOGIN FRAME ----------------
login_frame = tk.Frame(main_frame, bg="#FFFFFF")
tk.Label(login_frame, text="UID", font=("Helvetica", 12), bg="#FFFFFF").pack(pady=5)
entry_uid = ttk.Entry(login_frame, width=30, font=("Helvetica", 12))
entry_uid.pack()

tk.Label(login_frame, text="Password", font=("Helvetica", 12), bg="#FFFFFF").pack(pady=5)
entry_password = ttk.Entry(login_frame, width=30, font=("Helvetica", 12), show="*")
entry_password.pack()

style = ttk.Style()
style.theme_use("clam")
style.configure("Custom.TButton", font=("Helvetica", 12, "bold"),
                foreground="white", background="#007BFF")
style.map("Custom.TButton", background=[("active", "#0056b3")])

ttk.Button(login_frame, text="Login", command=login,
           style="Custom.TButton").pack(pady=15, ipadx=20)

tk.Label(login_frame, text="Don't have an account?", bg="#FFFFFF").pack()
register_link = tk.Label(login_frame, text="Register Here", fg="#007BFF",
                         cursor="hand2", bg="#FFFFFF", font=("Helvetica", 10, "underline"))
register_link.pack()
register_link.bind("<Button-1>", lambda e: show_register_frame())
login_frame.pack(fill="both", expand=True)

# ---------------- REGISTER FRAME ----------------
register_frame = tk.Frame(main_frame, bg="#FFFFFF")

tk.Label(register_frame, text="Name", bg="#FFFFFF").pack(pady=5)
entry_reg_name = ttk.Entry(register_frame, width=30, font=("Helvetica", 12))
entry_reg_name.pack()

tk.Label(register_frame, text="Age", bg="#FFFFFF").pack(pady=5)
entry_reg_age = ttk.Entry(register_frame, width=30, font=("Helvetica", 12))
entry_reg_age.pack()

tk.Label(register_frame, text="Date of Birth (YYYY-MM-DD)", bg="#FFFFFF").pack(pady=5)
entry_reg_dob = ttk.Entry(register_frame, width=30, font=("Helvetica", 12))
entry_reg_dob.pack()

tk.Label(register_frame, text="Gender", bg="#FFFFFF").pack(pady=5)
gender_var = tk.StringVar(value="Male")
gender_menu = ttk.Combobox(register_frame, textvariable=gender_var,
                           values=["Male", "Female", "Other"],
                           state="readonly", width=28)
gender_menu.pack()

tk.Label(register_frame, text="State", bg="#FFFFFF").pack(pady=5)
entry_reg_state = ttk.Entry(register_frame, width=30, font=("Helvetica", 12))
entry_reg_state.pack()

tk.Label(register_frame, text="Password", bg="#FFFFFF").pack(pady=5)
entry_reg_password = ttk.Entry(register_frame, width=30, font=("Helvetica", 12), show="*")
entry_reg_password.pack()

ttk.Button(register_frame, text="Register", command=register,
           style="Custom.TButton").pack(pady=15, ipadx=20)

tk.Label(register_frame, text="Already have an account?", bg="#FFFFFF").pack()
login_link = tk.Label(register_frame, text="Login Here", fg="#007BFF",
                      cursor="hand2", bg="#FFFFFF", font=("Helvetica", 10, "underline"))
login_link.pack()
login_link.bind("<Button-1>", lambda e: show_login_frame())

root.mainloop()
