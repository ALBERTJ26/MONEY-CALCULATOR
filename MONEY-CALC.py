from tkinter import *
from PIL import ImageTk, Image
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


w = Tk()
w.geometry('900x500')
w.configure(bg='#262626')  # 12c4c0')
w.resizable(0,0)
w.title('Toggle Menu')

con = sqlite3.connect('calculation.db')
cursor = con.cursor()
cursor1 = con.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS TECHNICAL_UNION (branchname TEXT NOT NULL)''')


def default_home():
    f2 = Frame(w, width=1500, height=455, bg='#262626')
    f2.place(x=0, y=45)


def destroy_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    frame.destroy()


cursor.execute("SELECT SUM(\"2018\") FROM TECHNICAL_UNION;")
sum_2018 = cursor.fetchone()[0]or 0

cursor.execute("SELECT SUM(\"2019\") FROM TECHNICAL_UNION;")
sum_2019 = cursor.fetchone()[0] or 0

cursor.execute("SELECT SUM(\"2020\") FROM TECHNICAL_UNION;")
sum_2020 = cursor.fetchone()[0] or 0

cursor.execute("SELECT SUM(\"2021\") FROM TECHNICAL_UNION;")
sum_2021 = cursor.fetchone()[0] or 0

cursor.execute("SELECT SUM(\"2022\") FROM TECHNICAL_UNION;")
sum_2022 = cursor.fetchone()[0] or 0

def display_total():
    destroy_frame(f1)
    f2 = Frame(w, width=900, height=455, bg='white')
    f2.place(x=0, y=45)

    overall_total = Label(f2, text='OVERALL TOTAL',bg='white')
    overall_total.config(font=('Comic Sans MS', 15))
    overall_total.place(x=100,y=20)

##########################################
    tk18_total = Label(f2, text='2018 TOTAL',bg='white')
    tk18_total.config(font=('Comic Sans MS', 15))
    tk18_total.place(x=100, y=100)

    tk18_value = Label(f2, text=f'{sum_2018}  Rs', bg='white')
    tk18_value.config(font=('Comic Sans MS', 15))
    tk18_value.place(x=300, y=100)
###########################################
    tk19_total = Label(f2, text='2019 TOTAL', bg='white')
    tk19_total.config(font=('Comic Sans MS', 15))
    tk19_total.place(x=100, y=200)

    tk19_value = Label(f2, text=f'{sum_2019}  Rs', bg='white')
    tk19_value.config(font=('Comic Sans MS', 15))
    tk19_value.place(x=300, y=200)

###########################################
    tk20_total = Label(f2, text='2020 TOTAL', bg='white')
    tk20_total.config(font=('Comic Sans MS', 15))
    tk20_total.place(x=100, y=300)

    tk20_value = Label(f2, text=f'{sum_2020}  Rs', bg='white')
    tk20_value.config(font=('Comic Sans MS', 15))
    tk20_value.place(x=300, y=300)

##########################################
    tk21_total = Label(f2, text='2021 TOTAL', bg='white')
    tk21_total.config(font=('Comic Sans MS', 15))
    tk21_total.place(x=500, y=100)

    tk21_value = Label(f2, text=f'{sum_2021}  Rs', bg='white')
    tk21_value.config(font=('Comic Sans MS', 15))
    tk21_value.place(x=700, y=100)

#########################################
    tk22_total = Label(f2, text='2022 TOTAL', bg='white')
    tk22_total.config(font=('Comic Sans MS', 15))
    tk22_total.place(x=500, y=200)

    tk22_value = Label(f2, text=f'{sum_2022}  Rs', bg='white')
    tk22_value.config(font=('Comic Sans MS', 15))
    tk22_value.place(x=700, y=200)

#########################################

    overall = int(sum_2018)+int(sum_2019)+int(sum_2020)+int(sum_2021)+int(sum_2022)

    disp_total = Label(f2, text=overall, bg='white')
    disp_total.config(font=('Comic Sans MS', 15))
    disp_total.place(x=300,y=20)

    con.commit()


def view():
    destroy_frame(f1)
    f2 = Frame(w, width=1500, height=455, bg='white')
    f2.place(x=50, y=45)

    conn = sqlite3.connect('calculation.db')
    cursor = conn.cursor()

    query = "PRAGMA table_info(TECHNICAL_UNION)"
    cursor.execute(query)
    field_names = [column[1] for column in cursor.fetchall()]

    data_query = "SELECT * FROM TECHNICAL_UNION"
    cursor.execute(data_query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    result_window = tk.Tk()
    result_window.title("Database Results")

    tree = ttk.Treeview(result_window, columns=field_names, show='headings')

    for field in field_names:
        tree.heading(field, text=field)
        tree.column(field)

    for row in data:
        tree.insert("", "end", values=row)

    tree.pack()
    toggle_win()


def add_union():
    destroy_frame(f1)
    f2 = Frame(w, width=900, height=455, bg='white')
    f2.place(x=0, y=45)

    def name_union():
        name = union_name.get()
        cursor.execute(f'''INSERT INTO TECHNICAL_UNION (branchname) VALUES ('{name}');''')
        messagebox.showinfo('ADDED', f'{name} added')
        con.commit()

    box_name = Label(f2, text='ADD UNION', fg='black', bg='white')
    box_name.config(font=('Poppins', 15))
    box_name.place(x=350, y=80 - 45)

    u_name = Label(f2, text='BRANCH NAME', fg='black', bg='white')
    u_name.config(font=('Comic Sans MS', 10))
    u_name.place(x=290, y=150 - 45)

    union_name = Entry(f2,  fg='black', bg='white')
    union_name.config(font=('Comic Sans MS', 10))
    union_name.place(x=420, y=150 - 45)

    c_union = Button(f2, text='CREATE UNION', command=name_union)
    c_union.config(font=('Comic Sans MS', 10))
    c_union.place(x=390, y=200 - 45)

    toggle_win()


def add_year():
    destroy_frame(f1)
    f2 = Frame(w, width=900, height=455, bg='white')
    f2.place(x=0, y=45)

    def new_year():

        year = year_name.get()
        cursor.execute(f'''ALTER TABLE TECHNICAL_UNION ADD COLUMN '{year}' TEXT NOT NULL ;''')
        messagebox.showinfo('ADDED', f'{year} added')
        con.commit()

    box_name = Label(f2, text='ADD YEAR', fg='black', bg='white')
    box_name.config(font=('Poppins', 15))
    box_name.place(x=350, y=80 - 45)

    y_name = Label(f2, text='YEAR', fg='black', bg='white')
    y_name.config(font=('Comic Sans MS', 10))
    y_name.place(x=290, y=150 - 45)

    year_name = Entry(f2,  fg='black', bg='white')
    year_name.config(font=('Comic Sans MS', 10))
    year_name.place(x=420, y=150 - 45)

    c_year = Button(f2, text='CREATE YEAR', command=new_year)
    c_year.config(font=('Comic Sans MS', 10))
    c_year.place(x=390, y=200 - 45)

    toggle_win()


def add_amount():
    destroy_frame(f1)
    f2 = Frame(w, width=900, height=455, bg='white')
    f2.place(x=0, y=45)

    def create():
        c_year = s_year.get()
        c_union = union_name.get()
        c_amount = n_amount.get()
        cursor.execute(f'''UPDATE TECHNICAL_UNION SET "{c_year}" = {c_amount} WHERE branchname = '{c_union}' ;''')
        print(f"Updated value for {c_year}: {c_amount}")
        messagebox.showinfo('ADDED', f'{c_amount} added')
        con.commit()

    box_name = Label(f2, text='ADD AMOUNT', fg='black', bg='white')
    box_name.config(font=('Poppins', 15))
    box_name.place(x=350, y=80 - 45)

    u_name = Label(f2, text='UNION NAME', fg='black', bg='white')
    u_name.config(font=('Comic Sans MS', 10))
    u_name.place(x=290, y=150 - 45)

    union_name = Entry(f2,  fg='black', bg='white')
    union_name.config(font=('Comic Sans MS', 10))
    union_name.place(x=420, y=150 - 45)

    year = Label(f2, text='YEAR', fg='black', bg='white')
    year.config(font=('Comic Sans MS', 10))
    year.place(x=290, y=200 - 45)

    s_year = Entry(f2,  fg='black', bg='white')
    s_year.config(font=('Comic Sans MS', 10))
    s_year.place(x=420, y=200 - 45)

    e_amount = Label(f2, text='AMOUNT', fg='black', bg='white')
    e_amount.config(font=('Comic Sans MS', 10))
    e_amount.place(x=290, y=250 - 45)

    n_amount = Entry(f2,  fg='black', bg='white')
    n_amount.config(font=('Comic Sans MS', 10))
    n_amount.place(x=420, y=250 - 45)

    ch_union = Button(f2, text='CREATE', command=create)
    ch_union.config(font=('Comic Sans MS', 10))
    ch_union.place(x=310, y=300 - 45)



    toggle_win()


def update_amount():
    destroy_frame(f1)
    f2 = Frame(w, width=900, height=455, bg='white')
    f2.place(x=0, y=45)


    def add():
        c_year = s_year.get()
        c_union = union_name.get()
        up_amount = n_amount.get()

        cursor1.execute(f'''SELECT "{c_year}" FROM TECHNICAL_UNION WHERE branchname = '{c_union}';''')
        selected_value = cursor1.fetchone()
        print('value is:', selected_value)
        print("sum is", up_amount)

        if selected_value:
            selected_value = selected_value[0]  # Get the value from the tuple

            print('Value is:', selected_value)
            print('Sum is:', up_amount)

            sum_amount = selected_value + int(up_amount)
            print('Sum:', sum_amount)
            cursor.execute(f'''UPDATE TECHNICAL_UNION SET "{c_year}" = {sum_amount} WHERE branchname = '{c_union}' ;''')
            messagebox.showinfo('UPDATED', f'{up_amount} added')

        else:
            print('No value found for the given conditions')

        con.commit()

    box_name = Label(f2, text='UPDATE AMOUNT', fg='black', bg='white')
    box_name.config(font=('Poppins', 15))
    box_name.place(x=350, y=80 - 45)

    u_name = Label(f2, text='UNION NAME', fg='black', bg='white')
    u_name.config(font=('Comic Sans MS', 10))
    u_name.place(x=290, y=150 - 45)

    union_name = Entry(f2,  fg='black', bg='white')
    union_name.config(font=('Comic Sans MS', 10))
    union_name.place(x=420, y=150 - 45)

    year = Label(f2, text='YEAR', fg='black', bg='white')
    year.config(font=('Comic Sans MS', 10))
    year.place(x=290, y=200 - 45)

    s_year = Entry(f2,  fg='black', bg='white')
    s_year.config(font=('Comic Sans MS', 10))
    s_year.place(x=420, y=200 - 45)

    e_amount = Label(f2, text='ADD AMOUNT', fg='black', bg='white')
    e_amount.config(font=('Comic Sans MS', 10))
    e_amount.place(x=290, y=250 - 45)

    n_amount = Entry(f2,  fg='black', bg='white')
    n_amount.config(font=('Comic Sans MS', 10))
    n_amount.place(x=420, y=250 - 45)

    ch_union_add = Button(f2, text='UPDATE', command=add)
    ch_union_add.config(font=('Comic Sans MS', 10))
    ch_union_add.place(x=390, y=300 - 45)

    toggle_win()


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

        myButton1 = Button(f1, text=text,  width=42,  height=2,  fg='#262626',  border=0,  bg=fcolor,  activeforeground='#262626',  activebackground=bcolor,  command=cmd)
        myButton1.bind("<Enter>", on_entera)
        myButton1.bind("<Leave>", on_leavea)

        myButton1.place(x=x, y=y)

    bttn(0, 80, 'D I S P L A Y  D A T A', '#0f9d9a', '#12c4c0', display_total)
    bttn(0, 130, 'V I E W', '#0f9d9a', '#12c4c0', view)
    bttn(0, 180, 'A D D  B R A N C H', '#0f9d9a', '#12c4c0', add_union)
    bttn(0, 230, 'A D D  Y E A R', '#0f9d9a', '#12c4c0', add_year)
    bttn(0, 280, 'A D D  A M O U N T', '#0f9d9a', '#12c4c0', add_amount)
    bttn(0, 330, 'U P D A T E  A M O U N T', '#0f9d9a', '#12c4c0', update_amount)


    #
    def dele():
        f1.destroy()
        b2 = Button(w, image=img1, command=toggle_win, border=0, bg='#262626', activebackground='#262626')
        b2.place(x=5, y=8)

    global img2
    img2 = ImageTk.PhotoImage(Image.open("close.png"))

    Button(f1, image=img2, border=0, command=dele, bg='#12c4c0', activebackground='#12c4c0').place(x=5, y=10)


default_home()
img1 = ImageTk.PhotoImage(Image.open("open.png"))
global b2
b2 = Button(w, image=img1, command=toggle_win, border=0, bg='#262626', activebackground='#262626')
b2.place(x=5, y=8)
w.mainloop()