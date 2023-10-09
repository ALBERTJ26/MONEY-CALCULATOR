from tkinter import *
from PIL import ImageTk, Image
import sqlite3
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import pandas as pd

w = Tk()
w.geometry('900x500')
w.configure(bg='#262626')  # 12c4c0')
w.resizable(0, 0)
w.title('Toggle Menu')

con = sqlite3.connect('calculation.db')
cursor = con.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS TECHNICAL_UNION (branch_name TEXT NOT NULL)''')

conn = sqlite3.connect('calculation.db')
cursor1 = conn.cursor()
cursor3 = conn.cursor()

cursor1.execute("SELECT name FROM sqlite_master WHERE type='table';")
table_names = [table[0] for table in cursor1.fetchall() if table[0] != 'sqlite_sequence']

sums_dict = {}
all_table_names = []
all_column_names = []

if table_names:
    table_names.pop(0)

for table_name in table_names:
    cursor1.execute(f"PRAGMA table_info({table_name})")
    column_info = cursor1.fetchall()
    column_names = [row[1] for row in column_info[1:]]
    all_table_names.append(table_name)
    all_column_names.extend(column_names)
    all_column_names = list(set(all_column_names))

    for column_name in column_names:
        query = f"SELECT SUM(\"{column_name}\") FROM {table_name};"
        cursor1.execute(query)
        sums = cursor1.fetchone()[0] or 0
        sums_dict[table_name, column_name] = sums

all_column_names.sort()

print("\nStored Sum Values (without the first table):\n")
for key, value in sums_dict.items():
    print(f"\n{key}: {value}")
    print("Values:", value)

print("\nTable Names:")
print(all_table_names)

print("\nColumn Names (Ascending Order):")
print(all_column_names)

for table in all_table_names:
    cursor1.execute(f'SELECT branch_name FROM TECHNICAL_UNION WHERE branch_name = ?;', (table,))
    existing_value = cursor1.fetchone()

    if existing_value is None:
        cursor1.execute(f'INSERT INTO TECHNICAL_UNION(branch_name) VALUES (?);', (table,))
        conn.commit()

for column in all_column_names:
    cursor1.execute(f"PRAGMA table_info(TECHNICAL_UNION);")
    existing_columns = [row[1] for row in cursor1.fetchall()]

    if column not in existing_columns:
        cursor1.execute(f"ALTER TABLE TECHNICAL_UNION ADD COLUMN '{column}' INTEGER")
        conn.commit()

for (table_name, column_name), value in sums_dict.items():
    cursor1.execute(f'SELECT branch_name FROM TECHNICAL_UNION WHERE branch_name = ?;', (table_name,))
    existing_value = cursor1.fetchone()

    if existing_value:
        cursor1.execute(f'UPDATE TECHNICAL_UNION SET "{column_name}" = ? WHERE branch_name = ?;', (value, table_name))
        conn.commit()

cursor.execute(f"PRAGMA table_info(TECHNICAL_UNION)")
column_info = cursor.fetchall()
column_names = [row[1] for row in column_info]

if column_names:
    column_names.pop(0)
print("\nColumn Names OF TECHNICAL_UNION:")

for column_name in column_names:
    cursor.execute(f"SELECT SUM(\"{column_name}\") FROM TECHNICAL_UNION;")
    total_sum = cursor.fetchone()[0] or 0
    y_total = total_sum
    year_total = f"{column_name}:{total_sum}"
    print(year_total)

total_sum = 0
for column_name in column_names:
    cursor1.execute(f"SELECT SUM(\"{column_name}\") FROM TECHNICAL_UNION;")
    column_total = cursor1.fetchone()[0] or 0
    total_sum =total_sum + column_total
print(f"Total sum of all columns: {total_sum}")
cursor1.close()

def default_home():
    f2 = Frame(w, width=900, height=455, bg='#262626')
    f2.place(x=0, y=45)
    l2 = Label(f2, text='Tech Union \n Calculator', fg='white', bg='#262626')
    l2.config(font=('Comic Sans MS', 60))
    l2.place(x=210, y=120 - 45)


def view():
    f1.destroy()
    f2 = Frame(w, width=900, height=455, bg='#262626')
    f2.place(x=0, y=45)

    cursor.execute("SELECT COUNT(name) FROM sqlite_master WHERE type='table';")
    num_tables = cursor.fetchone()[0]
    print("Number of tables in the database:", num_tables)

    Total = Label(f2, text='Total', fg='white', bg='#262626')
    Total.config(font=('Comic Sans MS', 20))
    Total.place(x=150, y=50 - 45)

    Total_num = Label(f2, text=f'- {total_sum} ₹ ', fg='white', bg='#262626')
    Total_num.config(font=('Comic Sans MS', 20))
    Total_num.place(x=250, y=50 - 45)

    for i, column_name in enumerate(all_column_names, start=1):
        Y_name = Label(f2, text=column_name, fg='white', bg='#262626')
        Y_name.config(font=('Comic Sans MS', 20))
        Y_name.place(x=150, y=(50 - 45) + (i * 60))

        cursor.execute(f"SELECT SUM(\"{column_name}\") FROM TECHNICAL_UNION;")
        y_total = cursor.fetchone()[0] or 0

        Y_total_label = Label(f2, text=f'- {y_total} ₹ ', fg='white', bg='#262626')
        Y_total_label.config(font=('Comic Sans MS', 20))
        Y_total_label.place(x=250, y=(50 - 45) + (i * 60))  # Adjust the x-coordinate as needed


def display():
    f1.destroy()
    f2 = Frame(w, width=900, height=455, bg='white')
    f2.place(x=0, y=45)

    def view_data():
        conn = sqlite3.connect('calculation.db')
        cursor = conn.cursor()
        branch_name = branch_disp.get()

        query = f"PRAGMA table_info({branch_name})"
        cursor.execute(query)
        field_names = [column[1] for column in cursor.fetchall()]

        data_query = f"SELECT * FROM {branch_name}"
        cursor.execute(data_query)
        data = cursor.fetchall()

        result_window = tk.Tk()
        result_window.title("Database Results")
        result_window.geometry("800x600")

        table_frame = tk.Frame(result_window)
        table_frame.pack(padx=10, pady=10)

        # Display field names
        row_index = 0
        for index, field in enumerate(field_names):
            label = tk.Label(table_frame, text=field, padx=10, pady=5, relief=tk.RIDGE, font=('Arial', 12, 'bold'))
            label.grid(row=row_index, column=index, sticky=tk.W + tk.E)

        # Display data
        for row_index, row in enumerate(data, start=1):
            for col_index, value in enumerate(row):
                label = tk.Label(table_frame, text=value, padx=10, pady=5, relief=tk.RIDGE, font=('Arial', 12))
                label.grid(row=row_index, column=col_index, sticky=tk.W + tk.E)

        # Calculate individual year totals
        year_totals = []
        for year in field_names[1:]:  # Skip the first column (name)
            cursor.execute(f"SELECT SUM(\"{year}\") FROM {branch_name};")
            year_total = cursor.fetchone()[0]
            if year_total is None:
                year_total = 0  # Replace None with 0
            year_totals.append(year_total)

        # Display individual year totals
        row_index = len(data) + 1
        for col_index, year_total in enumerate(year_totals, start=1):
            label = tk.Label(table_frame, text=f" {year_total} Rs", padx=10, pady=5, relief=tk.RIDGE,font=('Arial', 12, 'bold'))
            label.grid(row=row_index, column=col_index, sticky=tk.W + tk.E)

        # Calculate and display overall total
        overall_total = sum(year_totals)
        disp_total = tk.Label(table_frame, text=f"Overall Total: {overall_total} Rs", padx=10, pady=5, relief=tk.RIDGE,font=('Arial', 12, 'bold'))
        disp_total.grid(row=row_index + 1, columnspan=len(year_totals) + 1, sticky=tk.W + tk.E)
        result_window.mainloop()

    def view_overall():
        conn = sqlite3.connect('calculation.db')
        cursor = conn.cursor()

        query = "PRAGMA table_info(TECHNICAL_UNION)"
        cursor.execute(query)
        field_names = [column[1] for column in cursor.fetchall()]

        data_query = "SELECT * FROM TECHNICAL_UNION"
        cursor.execute(data_query)
        data = cursor.fetchall()

        result_window = tk.Tk()
        result_window.title("Database Results")
        result_window.geometry("800x600")  # Set the window dimensions

        table_frame = tk.Frame(result_window)
        table_frame.pack(padx=10, pady=10)

        # Display field names
        row_index = 0
        for index, field in enumerate(field_names):
            label = tk.Label(table_frame, text=field, padx=10, pady=5, relief=tk.RIDGE, font=('Arial', 12, 'bold'))
            label.grid(row=row_index, column=index, sticky=tk.W + tk.E)

        # Display data
        for row_index, row in enumerate(data, start=1):
            for col_index, value in enumerate(row):
                label = tk.Label(table_frame, text=value, padx=10, pady=5, relief=tk.RIDGE, font=('Arial', 12))
                label.grid(row=row_index, column=col_index, sticky=tk.W + tk.E)

        # Calculate individual year totals
        year_totals = []
        for year in field_names[1:]:  # Skip the first column (name)
            cursor.execute(f"SELECT SUM(\"{year}\") FROM TECHNICAL_UNION;")
            year_total = cursor.fetchone()[0]
            if year_total is None:
                year_total = 0  # Replace None with 0
            year_totals.append(year_total)

        # Display individual year totals
        row_index = len(data) + 1
        for col_index, year_total in enumerate(year_totals, start=1):
            label = tk.Label(table_frame, text=f" {year_total} Rs", padx=10, pady=5, relief=tk.RIDGE,
                             font=('Arial', 12, 'bold'))
            label.grid(row=row_index, column=col_index, sticky=tk.W + tk.E)

        # Calculate and display overall total
        overall_total = sum(year_totals)
        disp_total = tk.Label(table_frame, text=f"Overall Total: {overall_total} Rs", padx=10, pady=5, relief=tk.RIDGE,
                              font=('Arial', 12, 'bold'))
        disp_total.grid(row=row_index + 1, columnspan=len(year_totals) + 1, sticky=tk.W + tk.E)

        cursor.close()  # Close the cursor after all operations are done
        conn.close()  # Close the connection

        result_window.mainloop()

    def on_branch_select(event):
        global selected_branch
        selected_branch = branch_disp.get()
        print(f"Selected Branch: {selected_branch}")
        update_employee_combobox()

    def update_employee_combobox():
        cursor3 = con.cursor()
        cursor3.execute(f"PRAGMA table_info({selected_branch})")
        column_info = cursor3.fetchall()
        column_names = [row[1] for row in column_info]
        if column_names:
            column_names.pop(0)
        cursor3.close()

    def export():
        overall_data = sqlite3.connect('calculation.db')
        df = pd.read_sql_query(f"SELECT * from TECHNICAL_UNION", overall_data)
        df.to_excel(f"./Total.xlsx", index=False)
        overall_data.close()
        messagebox.showinfo("Exported", "Overall data exported to Excel successfully.")

    def export_data():
        b_name = branch_disp.get()
        branch_data = sqlite3.connect('calculation.db')
        df = pd.read_sql_query(f"SELECT * from {b_name}", branch_data)
        df.to_excel(f"./{b_name}.xlsx", index=False)
        branch_data.close()
        messagebox.showinfo("Exported", "Branch data exported to Excel successfully.")

    cursor.execute("SELECT branch_name FROM TECHNICAL_UNION")
    rows = cursor.fetchall()
    branch_names = [row[0] for row in rows]

    overall_disp = Button(f2, text="OVERALL", font=10, command=view_overall)
    overall_disp.place(x=250, y=100)

    exp = Button(f2, text='EXPORT', font=10, command=export)
    exp.place(x=400, y=100)

    select_branch = Label(f2, text="BY BRANCH", font=10)
    select_branch.place(x=250, y=180)

    branch_disp = ttk.Combobox(f2, values=branch_names, font=5, width=10)
    branch_disp.place(x=400, y=180)
    branch_disp.set(branch_names[0])
    branch_disp.bind("<<ComboboxSelected>>", on_branch_select)

    view_btn = Button(f2, text="VIEW", font=7, command=view_data)
    view_btn.place(x=550, y=180)

    exp_d = Button(f2, text='EXPORT DATA', font=10, command=export_data)
    exp_d.place(x=350, y=250)
    conn.close()


def branch():
    f1.destroy()
    f2 = Frame(w, width=900, height=455, bg='white')
    f2.place(x=0, y=45)

    def name_union():
        name = union_name.get()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {name} (employee_name TEXT NOT NULL)''')
        messagebox.showinfo('ADDED', f'{name} added')
        con.commit()

    def new_year():
        name = union_name.get()
        year = year_name.get()
        cursor.execute(f'''ALTER TABLE {name} ADD COLUMN '{year}' TEXT DEFAULT 'N/A' ;''')
        messagebox.showinfo('ADDED', f'{year} added')
        con.commit()

    box_name = Label(f2, text='ADD BRANCH', fg='black', bg='white')
    box_name.config(font=('Poppins', 15))
    box_name.place(x=350, y=80 - 45)

    u_name = Label(f2, text='BRANCH NAME', fg='black', bg='white')
    u_name.config(font=('Comic Sans MS', 10))
    u_name.place(x=290, y=150 - 45)

    union_name = Entry(f2,  fg='black', bg='white')
    union_name.config(font=('Comic Sans MS', 10))
    union_name.place(x=420, y=150 - 45)

    y_name = Label(f2, text='YEAR', fg='black', bg='white')
    y_name.config(font=('Comic Sans MS', 10))
    y_name.place(x=290, y=200 - 45)

    year_name = Entry(f2,  fg='black', bg='white')
    year_name.config(font=('Comic Sans MS', 10))
    year_name.place(x=420, y=200 - 45)

    add_branch = Button(f2, text='CREATE', command=name_union)
    add_branch.config(font=('Comic Sans MS', 10))
    add_branch.place(x=320, y=250 - 45)

    update_branch = Button(f2, text='UPDATE', command=new_year)
    update_branch.config(font=('Comic Sans MS', 10))
    update_branch.place(x=420, y=250 - 45)


def employee():
    f1.destroy()
    f2 = Frame(w, width=900, height=455, bg='white')
    f2.place(x=0, y=45)

    def add_emp():
        emp_name = e_name.get()
        branchs_name = branch_name.get()
        cursor.execute(f'''INSERT INTO {branchs_name} (employee_name) VALUES ('{emp_name}');''')
        messagebox.showinfo('ADDED', f'{emp_name} added')
        con.commit()

    def del_emp():
        emp_name = e_name.get()
        branchs_name = branch_name.get()
        cursor.execute(f'''DELETE FROM {branchs_name} WHERE employee_name='{emp_name}';''')
        messagebox.showinfo('DELETE', f'{emp_name} deleted')
        con.commit()

    box_name = Label(f2, text='ADD EMPLOYEE', fg='black', bg='white')
    box_name.config(font=('Poppins', 15))
    box_name.place(x=350, y=80 - 45)

    emplo_name = Label(f2, text='EMPLOYEE NAME', fg='black', bg='white')
    emplo_name.config(font=('Comic Sans MS', 10))
    emplo_name.place(x=290, y=200 - 45)

    e_name = Entry(f2,  fg='black', bg='white')
    e_name.config(font=('Comic Sans MS', 10))
    e_name.place(x=420, y=200 - 45)

    b_name = Label(f2, text='BRANCH NAME', fg='black', bg='white')
    b_name.config(font=('Comic Sans MS', 10))
    b_name.place(x=290, y=150 - 45)

    branch_name = Entry(f2,  fg='black', bg='white')
    branch_name.config(font=('Comic Sans MS', 10))
    branch_name.place(x=420, y=150 - 45)

    add_employee = Button(f2, text='ADD', command=add_emp)
    add_employee.config(font=('Comic Sans MS', 10))
    add_employee.place(x=400, y=250 - 45)

    del_employee = Button(f2, text='DELETE', command=del_emp)
    del_employee.config(font=('Comic Sans MS', 10))
    del_employee.place(x=500, y=250 - 45)


def amount():
    f1.destroy()
    f2 = Frame(w, width=900, height=455, bg='white')
    f2.place(x=0, y=45)

    def on_branch_select(event):
        global selected_branch
        selected_branch = combo.get()
        print(f"Selected Branch: {selected_branch}")
        update_employee_combobox()

    def on_employee_select(event):
        global selected_employee
        selected_employee = combo1.get()
        print(f"Selected Employee: {selected_employee}")

    def on_year_select(event):
        global selected_year
        selected_year = combo2.get()
        print(f"Selected Year: {selected_year}")

    def update_employee_combobox():
        cursor1.execute(f"PRAGMA table_info({selected_branch})")
        column_info = cursor1.fetchall()
        column_names = [row[1] for row in column_info]
        if column_names:
            column_names.pop(0)

        cursor2.execute(f"SELECT employee_name FROM {selected_branch}")
        rows = cursor2.fetchall()
        employee_names = [row[0] for row in rows]

        combo1['values'] = employee_names
        combo1.set(employee_names[0])

        combo2['values'] = column_names
        combo2.set(column_names[0])

    def add_amount():
        con1 = sqlite3.connect('calculation.db')
        cursors = con1.cursor()
        c_year = selected_year
        branch_name = selected_branch
        em_name = selected_employee
        amount_to_add = amount_add.get()
        cursors.execute(f'''UPDATE {branch_name} SET "{c_year}" = {amount_to_add} WHERE employee_name = '{em_name}' ;''')
        print(f"Updated value for {c_year}: {amount_to_add}")
        messagebox.showinfo('ADDED', f'{amount_to_add} added')
        con1.commit()
        con1.close()

    cons = sqlite3.connect('calculation.db')
    cursor = cons.cursor()
    cursor1 = cons.cursor()
    cursor2 = cons.cursor()

    cursor.execute("SELECT branch_name FROM TECHNICAL_UNION")
    rows = cursor.fetchall()
    branch_names = [row[0] for row in rows]

    box_name = Label(f2, text='ADD AMOUNT', fg='black', bg='white')
    box_name.config(font=('Poppins', 15))
    box_name.place(x=350, y=80 - 45)

    u_name = Label(f2, text='BRANCH NAME', fg='black', bg='white')
    u_name.config(font=('Comic Sans MS', 10))
    u_name.place(x=290, y=150 - 45)

    combo = ttk.Combobox(f2, values=branch_names)
    combo.place(x=420 ,y=150 - 45)
    combo.set(branch_names[0])
    combo.bind("<<ComboboxSelected>>", on_branch_select)

    e_name = Label(f2, text='EMPLOYEE NAME', fg='black', bg='white')
    e_name.config(font=('Comic Sans MS', 10))
    e_name.place(x=290, y=200 - 45)

    combo1 = ttk.Combobox(f2)
    combo1.place(x=420, y=200 - 45)
    combo1.bind("<<ComboboxSelected>>", on_employee_select)

    y_name = Label(f2, text='YEAR', fg='black', bg='white')
    y_name.config(font=('Comic Sans MS', 10))
    y_name.place(x=290, y=250 - 45)

    combo2 = ttk.Combobox(f2)
    combo2.place(x=420, y=250 - 45)
    combo2.bind("<<ComboboxSelected>>", on_year_select)

    money = Label(f2, text='AMOUNT', fg='black', bg='white')
    money.config(font=('Comic Sans MS', 10))
    money.place(x=290, y=300 - 45)

    amount_add = Entry(f2,  fg='black', bg='white')
    amount_add.config(font=('Comic Sans MS', 10))
    amount_add.place(x=420, y=300 - 45)

    add_branch = Button(f2, text='ADD', command=add_amount)
    add_branch.config(font=('Comic Sans MS', 10))
    add_branch.place(x=400, y=350 - 45)

def toggle_win():
    global f1
    f1 = Frame(w, width=300, height=500, bg='#12c4c0')
    f1.place(x=0, y=0)

    # buttons
    def bttn(x, y, text, bcolor, fcolor, cmd):
        def on_entera(e):
            myButton1['background'] = bcolor  # ffcc66
            myButton1['foreground'] = '#262626'  # 000d33

        def on_leavea(e):
            myButton1['background'] = fcolor
            myButton1['foreground'] = '#262626'

        myButton1 = Button(f1, text=text,width=42,height=2,fg='#262626',border=0,bg=fcolor,activeforeground='#262626',activebackground=bcolor,command=cmd)
        myButton1.bind("<Enter>", on_entera)
        myButton1.bind("<Leave>", on_leavea)

        myButton1.place(x=x, y=y)

    bttn(0, 80, 'V I E W', '#0f9d9a', '#12c4c0', view)
    bttn(0, 130, 'D I S P L A Y', '#0f9d9a', '#12c4c0', display)
    bttn(0, 180, 'B R A N C H', '#0f9d9a', '#12c4c0', branch)
    bttn(0, 230, 'E M P L O Y E E', '#0f9d9a', '#12c4c0', employee)
    bttn(0, 280, 'A M O U N T', '#0f9d9a', '#12c4c0', amount)

    def dele():
        f1.destroy()
        b2 = Button(w, image=img1,command=toggle_win,border=0,bg='#262626',activebackground='#262626')
        b2.place(x=5, y=8)

    global img2
    img2 = ImageTk.PhotoImage(Image.open("close.png"))
    Button(f1,image=img2,border=0,command=dele,bg='#12c4c0',activebackground='#12c4c0').place(x=5, y=10)

default_home()
img1 = ImageTk.PhotoImage(Image.open("open.png"))
global b2
b2 = Button(w, image=img1,command=toggle_win,border=0,bg='#262626',activebackground='#262626')
b2.place(x=5, y=8)
w.mainloop()