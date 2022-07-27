import tkinter as tk
from tkinter import ttk
from WindowsFiles.Accounts import Accounts
import MySQLdb as mdb
from datetime import date
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import io

class Student_Account:
    global db,amount, treeview, datepiker,totalamount,st_roll

    def Connection(self):
        try:
            Student_Account.db = mdb.connect('localhost', 'root', '', 'hostel_managment')

        except mdb.Error as e:
            print('Not Connect')

    def TableSection(self,root):

        frame = tk.Frame(root, width=1200, height=680, relief="groove", highlightbackground='#2C0036', highlightthicknes=3)
        style = ttk.Style(frame)
        style.configure('Treeview', rowheight=70)

        game_scroll = ttk.Scrollbar(frame)
        game_scroll.pack(side='right', fill='y')

        game_scroll = ttk.Scrollbar(frame, orient='horizontal')
        game_scroll.pack(side='bottom', fill='x')

        my_game = ttk.Treeview(frame, height=7, yscrollcommand=game_scroll.set, xscrollcommand=game_scroll.set)
        Student_Account.treeview = my_game
        # define our column

        my_game['columns'] = ('student_name', 'room_name','date', 'meal', 'meal_cost','meal_pay','last_cost')

        # format our column
        my_game.column("#0", width=100,anchor="center")
        my_game.column("student_name",anchor="center", width=150)
        my_game.column("room_name",anchor="center", width=150)
        my_game.column("date",anchor="center", width=150)
        my_game.column("meal",anchor="center", width=100)
        my_game.column("meal_cost",anchor="center", width=150)
        my_game.column("meal_pay",anchor="center", width=150)
        my_game.column("last_cost",anchor="center", width=150)

        # Create Headings
        my_game.heading("#0", text="IMG--ST_ID")
        my_game.heading("student_name", text="Student Name")
        my_game.heading("room_name", text="Room Name" )
        my_game.heading("date", text="Date")
        my_game.heading("meal", text="Meal")
        my_game.heading("meal_cost", text="Meal Cost")
        my_game.heading("meal_pay", text="Meal Pay")
        my_game.heading("last_cost", text="Last Cost")


        my_game.pack()

        return  frame

    def __init__(self):
        self.Connection()
        root = tk.Tk()
        root.title('Sohid Sab Uddin Hostel ___ Student Meal Accounts')
        root.attributes('-fullscreen', True)
        root.iconphoto(False, tk.PhotoImage(file='../asset/icon.png'))
        root.configure(bg='#6DC9F3')

        # layout on the root window
        root.columnconfigure(0)

        input_frame = self.TableSection(root)
        input_frame.grid(column=0, row=0, sticky=tk.NW, padx=100, pady=80)

        Student_Account.st_roll = tk.Entry(root, width=30, font=("Bahnschrift", 15))
        Student_Account.st_roll.grid(column=0, row=0, sticky=tk.NW, padx=400, pady=20)

        tk.Button(
            root,
            text='Back To Accounts', font=("Bahnschrift", 14),
            command=lambda: [root.destroy(), self.Accounts()]
        ).grid(column=0, row=0, sticky=tk.NW, padx=40, pady=20)

        Student_Account.totalamount = tk.StringVar()
        tk.Label(root, font=("Bahnschrift", 14), textvariable=Student_Account.totalamount
                 ).grid(column=0, row=0, sticky=tk.NW, padx=1000, pady=640)

        tk.Button(
            root,
            text='Show Student Acc', font=("Bahnschrift", 14),
            command=lambda: self.SurchForStudent()
        ).grid(column=0, row=0, sticky=tk.NW, padx=750, pady=20)

    def FetchDataFromDatabase(self,s):
        list_of_months = {'1': 'January', '2': 'February', '3': 'March',
                          '4': 'April', '5': 'May', '6': 'June', '7': 'July',
                          '8': 'August', '9': 'September', '10': 'October',
                          '11': 'November', '12': 'December'}
        total=0
        for row in Student_Account.treeview.get_children():
            Student_Account.treeview.delete(row)

        r = Student_Account.db.cursor()
        sql=f"""
            SELECT * FROM `student_account` WHERE student_id='{s}'
            """
        r.execute(sql)
        rows = r.fetchall()
        Student_Account.treeview.imglist = []
        for row in rows:
            img = Image.open(io.BytesIO(row[3]))
            img_resized = img.resize((50, 50))
            img = ImageTk.PhotoImage(img_resized)
            total+=row[8]
            Student_Account.treeview.insert(parent='', index='end', iid=row[0], text=' ' + str(row[0]), image=img,
                                             values=(row[2], row[4],
                                                     list_of_months[str(row[1])[5:7]] +'-'+str(row[1])[0:4]
                                                     , row[5], row[6], row[7], row[8]))
            Student_Account.treeview.imglist.append(img)

        Student_Account.totalamount.set(f"Last Total Amount : {total}")

    def SurchForStudent(self):
        a=Student_Account.st_roll.get()
        if len(a)!=0:
            r = Student_Account.db.cursor()
            sql = f"""SELECT*FROM `hostel_managment`.`student_details` WHERE `roll`='{a}'"""
            r.execute(sql)
            rows = r.fetchall()
            if len(rows)==0:
                for row in Student_Account.treeview.get_children():
                    Student_Account.treeview.delete(row)
                tk.messagebox.showwarning('Sorry',
                                          'No Student Found in This Roll',
                                          icon='warning')
            else:
                self.FetchDataFromDatabase(rows[0][0])
        else:
            tk.messagebox.showwarning('Sorry',
                                      'Please, Fell Roll Section',
                                      icon='warning')

    def Accounts(self):
        Accounts.AccDetails()