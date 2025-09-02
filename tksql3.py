import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk


def createdb():
    conn = sqlite3.connect("student_data.db")
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        roll_no TEXT,
        age INTEGER
    )''')
    conn.commit()
    conn.close()


def addstu():
    name = entry_name.get()
    roll_no = entry_roll.get()
    age = entry_age.get()

    if name == "" or roll_no == "" or age == "":
        messagebox.showerror("Input Error", "All fields are required.")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Input Error", "Age must be a number.")
        return

    conn = sqlite3.connect("student_data.db")
    c = conn.cursor()
    c.execute("INSERT INTO students (name, roll_no, age) VALUES (?, ?, ?)", (name, roll_no, age))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Student added successfully!")

    clear_fields()
    viewstu()


def viewstu(search_query=""):
    conn = sqlite3.connect("student_data.db")
    c = conn.cursor()
    if search_query:
        c.execute("SELECT * FROM students WHERE name LIKE ? OR roll_no LIKE ?",
                  (f"%{search_query}%", f"%{search_query}%"))
    else:
        c.execute("SELECT * FROM students")
    students = c.fetchall()
    conn.close()

    listbox_students.delete(*listbox_students.get_children())
    for index, student in enumerate(students):
        tag = "even" if index % 2 == 0 else "odd"
        listbox_students.insert("", tk.END, values=(student[0], student[1], student[2], student[3]), tags=(tag,))

    status_var.set(f"Total Students: {len(students)}")


def deletestu():
    selected_item = listbox_students.selection()
    if not selected_item:
        messagebox.showerror("Selection Error", "Please select a student to delete.")
        return

    student_id = listbox_students.item(selected_item[0])["values"][0]
    confirm = messagebox.askyesno("Delete Student", f"Are you sure you want to delete student ID {student_id}?")
    if not confirm:
        return

    conn = sqlite3.connect("student_data.db")
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", f"Student ID {student_id} deleted successfully!")

    clear_fields()
    viewstu()


def updatestu():
    selected_item = listbox_students.selection()
    if not selected_item:
        messagebox.showerror("Selection Error", "Please select a student to update.")
        return

    student_id = listbox_students.item(selected_item[0])["values"][0]
    new_name = entry_name.get()
    new_roll_no = entry_roll.get()
    new_age = entry_age.get()

    if new_name == "" or new_roll_no == "" or new_age == "":
        messagebox.showerror("Input Error", "All fields are required.")
        return

    try:
        new_age = int(new_age)
    except ValueError:
        messagebox.showerror("Input Error", "Age must be a number.")
        return

    conn = sqlite3.connect("student_data.db")
    c = conn.cursor()
    c.execute("UPDATE students SET name = ?, roll_no = ?, age = ? WHERE id = ?",
              (new_name, new_roll_no, new_age, student_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Student updated successfully!")

    clear_fields()
    viewstu()


def clear_fields():
    entry_name.delete(0, tk.END)
    entry_roll.delete(0, tk.END)
    entry_age.delete(0, tk.END)


def search_students():
    query = entry_search.get()
    viewstu(query)


def on_select(event):
    selected_item = listbox_students.selection()
    if not selected_item:
        return
    values = listbox_students.item(selected_item[0])["values"]

    entry_name.delete(0, tk.END)
    entry_name.insert(0, values[1])
    entry_roll.delete(0, tk.END)
    entry_roll.insert(0, values[2])
    entry_age.delete(0, tk.END)
    entry_age.insert(0, values[3])


# ---------------- GUI ----------------
root = tk.Tk()
root.title("🎓 Student Data Management")
root.geometry("600x500")
root.config(bg="#e3f2fd")

# Title
title_frame = tk.Frame(root, bg="#1565c0", pady=10)
title_frame.pack(fill="x")
title_label = tk.Label(title_frame, text="Student Data Management System",
                       font=("Arial", 18, "bold"), bg="#1565c0", fg="white")
title_label.pack()

# Input Frame
frame_inputs = tk.LabelFrame(root, text="Enter Student Details", padx=10, pady=10, bg="#e3f2fd", fg="#0d47a1")
frame_inputs.pack(pady=10, padx=10, fill="x")

tk.Label(frame_inputs, text="Name:", bg="#e3f2fd").grid(row=0, column=0, sticky="w")
entry_name = tk.Entry(frame_inputs)
entry_name.grid(row=0, column=1, padx=5)

tk.Label(frame_inputs, text="Roll No:", bg="#e3f2fd").grid(row=1, column=0, sticky="w")
entry_roll = tk.Entry(frame_inputs)
entry_roll.grid(row=1, column=1, padx=5)

tk.Label(frame_inputs, text="Age:", bg="#e3f2fd").grid(row=2, column=0, sticky="w")
entry_age = tk.Entry(frame_inputs)
entry_age.grid(row=2, column=1, padx=5)

# Buttons
button_frame = tk.Frame(frame_inputs, bg="#e3f2fd")
button_frame.grid(row=3, column=0, columnspan=2, pady=10)

style = {"width": 12, "padx": 5, "pady": 5}
tk.Button(button_frame, text="Add", command=addstu, bg="#43a047", fg="white", **style).grid(row=0, column=0)
tk.Button(button_frame, text="Update", command=updatestu, bg="#1e88e5", fg="white", **style).grid(row=0, column=1)
tk.Button(button_frame, text="Delete", command=deletestu, bg="#e53935", fg="white", **style).grid(row=0, column=2)
tk.Button(button_frame, text="Clear", command=clear_fields, bg="#8e24aa", fg="white", **style).grid(row=0, column=3)

# Search
frame_search = tk.Frame(root, padx=10, pady=5, bg="#e3f2fd")
frame_search.pack(fill="x")
tk.Label(frame_search, text="🔍 Search:", bg="#e3f2fd").pack(side="left")
entry_search = tk.Entry(frame_search)
entry_search.pack(side="left", padx=5)
tk.Button(frame_search, text="Go", command=search_students, bg="#fb8c00", fg="white").pack(side="left")

# Table
frame_list = tk.Frame(root, padx=10, pady=10)
frame_list.pack(fill="both", expand=True)

columns = ("ID", "Name", "Roll No", "Age")
listbox_students = ttk.Treeview(frame_list, columns=columns, show="headings", height=12)
for col in columns:
    listbox_students.heading(col, text=col)
    listbox_students.column(col, width=100)

listbox_students.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(frame_list, orient="vertical", command=listbox_students.yview)
listbox_students.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

listbox_students.tag_configure("even", background="#f1f8e9")
listbox_students.tag_configure("odd", background="#e3f2fd")

listbox_students.bind("<<TreeviewSelect>>", on_select)

# Status bar
status_var = tk.StringVar()
status_bar = tk.Label(root, textvariable=status_var, anchor="w", bg="#1565c0", fg="white")
status_bar.pack(side="bottom", fill="x")

# Init
createdb()
viewstu()

root.mainloop()
