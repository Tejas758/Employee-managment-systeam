import mysql.connector
from tkinter import *
from tkinter import messagebox 
from tkinter import ttk
from PIL import ImageTk, Image

conn = mysql.connector.connect(host='localhost', user='root', password='Y1012Jqkhkp', database='pythondb1')

def create_emptable(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS employee
                      (id INT AUTO_INCREMENT PRIMARY KEY,
                       name VARCHAR(255) NOT NULL UNIQUE,
                       age INT,
                       department VARCHAR(255),
                       salary INT)''')

def add_employee(name, age, department, salary):
    cursor = conn.cursor()
    query = "INSERT INTO employee (name, age, department, salary) VALUES (%s, %s, %s, %s)"
    values = (name, age, department, salary)
    cursor.execute(query, values)
    conn.commit()
    messagebox.showinfo("Success", "Employee added successfully!")
    # status_label.config(text="Employee added successfully!", fg="green")

def view_employee_details():
    details_window = Toplevel(root)
    details_window.title("Employee Details")
    details_window.geometry("600x400")

    emp_table = ttk.Treeview(details_window)
    emp_table['columns'] = ('ID', 'Name', 'Age', 'Department', 'Salary')

    emp_table.heading('ID', text='ID')
    emp_table.heading('Name', text='Name')
    emp_table.heading('Age', text='Age')
    emp_table.heading('Department', text='Department')
    emp_table.heading('Salary', text='Salary')

    emp_table.column('#0', stretch=NO, minwidth=0, width=0)
    emp_table.column('ID', stretch=NO, minwidth=0, width=70)
    emp_table.column('Name', stretch=NO, minwidth=0, width=150)
    emp_table.column('Age', stretch=NO, minwidth=0, width=70)
    emp_table.column('Department', stretch=NO, minwidth=0, width=150)
    emp_table.column('Salary', stretch=NO, minwidth=0, width=100)

    emp_table.grid(row=0, column=0, sticky='nsew')

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employee")
    employees = cursor.fetchall()

    for employee in employees:
        emp_table.insert('', 'end', values=employee)

def create_employee():
    
    name = name_entry.get()
    age = age_entry.get()
    department = dep_entry.get()
    salary = sal_entry.get()

    try:
        age = int(age)
        salary = int(salary)

        if age < 18 or age > 60:
            raise ValueError("Age must be between 18 and 60.")
        

        add_employee(name, age, department, salary)

        name_entry.delete(0, END)
        age_entry.delete(0, END)
        dep_entry.delete(0, END)
        sal_entry.delete(0, END)

        view_employee_details()

    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", "An error occurred: " + str(e))


    name_entry.delete(0, END)
    age_entry.delete(0, END)
    dep_entry.delete(0, END)
    sal_entry.delete(0, END)

    

create_emptable(conn)

root = Tk()
root.title("Employee Management System")
root.geometry("800x600")

bg_image = Image.open("emp.jpg")
bg_image = bg_image.resize((800, 600), Image.ANTIALIAS)
background = ImageTk.PhotoImage(bg_image)

bg_label = Label(root, image=background)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

header_label = ttk.Label(root, text="Employee Management System", style='TLabel.Large.TLabel')
header_label.config(font=("Helvetica", 24), foreground="black")
header_label.grid(row=0, column=0, columnspan=2, pady=20)

name_label = ttk.Label(root, text="Name", style='TLabel')
name_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
name_entry = ttk.Entry(root, width=30)
name_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

age_label = ttk.Label(root, text="Age", style='TLabel')
age_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')
age_entry = ttk.Entry(root, width=30)
age_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

dep_label = ttk.Label(root, text="Department", style='TLabel')
dep_label.grid(row=3, column=0, padx=10, pady=10, sticky='e')
dep_entry = ttk.Entry(root, width=30)
dep_entry.grid(row=3, column=1, padx=10, pady=10, sticky='w')

sal_label = ttk.Label(root, text=("Salary"), style='TLabel')
sal_label.grid(row=4, column=0, padx=10, pady=10, sticky='e')
sal_entry = ttk.Entry(root, width=30)
sal_entry.grid(row=4, column=1, padx=10, pady=10, sticky='w')

create_button = ttk.Button(root, text="Add Employee", style='TButton', command=create_employee)
create_button.grid(row=5, column=0, padx=10, pady=10)

view_button = ttk.Button(root, text="View Employee Details", style='TButton', command=view_employee_details)
view_button.grid(row=5, column=1, padx=10, pady=10)

# status_label = ttk.Label(root, text="", style='TLabel')
#  status_label.grid(row=6, column=0, columnspan=2)

root.mainloop()

conn.close()
