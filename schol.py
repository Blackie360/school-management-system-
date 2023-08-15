import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
from PIL import Image, ImageTk

# Create the database
db_file = "student_management.db"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Students (
        student_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        photo_path TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Courses (
        course_id TEXT PRIMARY KEY,
        title TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Enrollment (
        student_id TEXT,
        course_id TEXT,
        FOREIGN KEY (student_id) REFERENCES Students (student_id),
        FOREIGN KEY (course_id) REFERENCES Courses (course_id)
    )
''')

conn.commit()
conn.close()

class Student:
    def __init__(self, student_id, name, age, photo_path=''):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.photo_path = photo_path

class Course:
    def __init__(self, course_id, title):
        self.course_id = course_id
        self.title = title

class StudentManagementSystem:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = sqlite3.connect(self.db_file)

    def add_student(self, student):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Students VALUES (?, ?, ?, ?)",
                       (student.student_id, student.name, student.age, student.photo_path))
        self.connection.commit()

    # Add other methods as needed

# GUI Functions
def add_student():
    student_id = student_id_entry.get()
    name = name_entry.get()
    age = age_entry.get()

    if student_id and name and age:
        student_data['student_id'] = student_id
        student_data['name'] = name
        student_data['age'] = age
        messagebox.showinfo("Success", "Student information added.")
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

def browse_photo():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif")])
    if file_path:
        photo = Image.open(file_path)
        photo = photo.resize((100, 100), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(photo)
        photo_label.config(image=photo)
        photo_label.image = photo
        photo_path.set(file_path)
        student_data['photo_path'] = file_path

def save_student():
    if 'student_id' in student_data and 'name' in student_data and 'age' in student_data:
        student = Student(
            student_data['student_id'],
            student_data['name'],
            student_data['age'],
            student_data.get('photo_path', '')
        )
        system.add_student(student)
        messagebox.showinfo("Success", f"Student {student_data['name']} added successfully.")
        student_id_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        photo_label.config(image="")
        photo_path.set("")
        student_data.clear()
    else:
        messagebox.showerror("Error", "Please add student information and photo.")

def enroll_student():
    # Implement this function to enroll a student in a course
    pass

def show_student_info():
    # Implement this function to display student information
    pass

# Create the main GUI window
root = tk.Tk()
root.title("Student Management System")
root.configure(bg="#674ea7")

# Create frames
add_student_frame = tk.Frame(root, bg="#674ea7")
add_student_frame.pack(padx=10, pady=10, anchor="w")

enroll_student_frame = tk.Frame(root, bg="#674ea7")
enroll_student_frame.pack(padx=10, pady=10, anchor="w")

show_student_frame = tk.Frame(root, bg="#674ea7")
show_student_frame.pack(padx=10, pady=10, anchor="w")

# Create input fields and labels for adding students
student_id_label = tk.Label(add_student_frame, text="Student ID:", bg="#674ea7", fg="white")
student_id_label.grid(row=0, column=0, padx=5, pady=5)
student_id_entry = tk.Entry(add_student_frame)
student_id_entry.grid(row=0, column=1, padx=5, pady=5)

name_label = tk.Label(add_student_frame, text="Name:", bg="#674ea7", fg="white")
name_label.grid(row=1, column=0, padx=5, pady=5)
name_entry = tk.Entry(add_student_frame)
name_entry.grid(row=1, column=1, padx=5, pady=5)

age_label = tk.Label(add_student_frame, text="Age:", bg="#674ea7", fg="white")
age_label.grid(row=2, column=0, padx=5, pady=5)
age_entry = tk.Entry(add_student_frame)
age_entry.grid(row=2, column=1, padx=5, pady=5)

add_button = tk.Button(add_student_frame, text="Add Student", command=add_student, bg="#0074D9", fg="white")
add_button.grid(row=3, columnspan=2, padx=5, pady=10)

# Create input fields and labels for enrolling students
course_id_label = tk.Label(enroll_student_frame, text="Course ID:", bg="#674ea7", fg="white")
course_id_label.grid(row=0, column=0, padx=5, pady=5)
course_id_entry = tk.Entry(enroll_student_frame)
course_id_entry.grid(row=0, column=1, padx=5, pady=5)

enroll_button = tk.Button(enroll_student_frame, text="Enroll Student", command=enroll_student, bg="#0074D9", fg="white")
enroll_button.grid(row=1, columnspan=2, padx=5, pady=10)

# Create input fields and labels for showing student info
student_id_label_show = tk.Label(show_student_frame, text="Student ID:", bg="#674ea7", fg="white")
student_id_label_show.grid(row=0, column=0, padx=5, pady=5)
student_id_entry_show = tk.Entry(show_student_frame)
student_id_entry_show.grid(row=0, column=1, padx=5, pady=5)

show_info_button = tk.Button(show_student_frame, text="Show Info", command=show_student_info, bg="#0074D9", fg="white")
show_info_button.grid(row=1, columnspan=2, padx=5, pady=10)

# Photo handling
photo_label = tk.Label(root, text="Passport Photo", bg="#674ea7", fg="white")
photo_label.pack(padx=10, pady=10)

photo_path = tk.StringVar()
browse_button = tk.Button(root, text="Browse Photo", command=browse_photo, bg="#0074D9", fg="white")
browse_button.pack(padx=10, pady=10)

save_button = tk.Button(root, text="Save Student", command=save_student, bg="#2ECC40", fg="white")
save_button.pack(padx=10, pady=10)

# Create the student management system with the database file
system = StudentManagementSystem(db_file)
student_data = {}  # To store temporary student data

# Start the GUI main loop
root.mainloop()
