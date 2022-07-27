import tkinter as tk
from tkinter import ttk
from WindowsFiles.Accounts import Accounts
import MySQLdb as mdb
from datetime import date
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import io
from tkinter import messagebox

class MonthlyMealAcc:
    global db,amount, treeview, datepiker

    def Connection(self):
        try:
            MonthlyMealAcc.db = mdb.connect('localhost', 'root', '', 'hostel_managment')

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

        my_game = ttk.Treeview(frame, height=8, yscrollcommand=game_scroll.set, xscrollcommand=game_scroll.set)
        MonthlyMealAcc.treeview = my_game
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

        a = date.today()
        self.FetchDataFromDatabase(str(a)[0:7])

        my_game.pack()

        return  frame

    def __init__(self):
        self.Connection()
        root = tk.Tk()
        root.title('Sohid Sab Uddin Hostel ___ Monthly Meal Accounts')
        root.attributes('-fullscreen', True)
        root.iconphoto(False, tk.PhotoImage(file='../asset/icon.png'))
        root.configure(bg='#6DC9F3')

        # layout on the root window
        root.columnconfigure(0)

        input_frame = self.TableSection(root)
        input_frame.grid(column=0, row=0, sticky=tk.NW, padx=100, pady=80)

        MonthlyMealAcc.datepiker = DateEntry(root, height=20, width=30, fg="white")
        MonthlyMealAcc.datepiker.grid(column=0, row=0, sticky=tk.NW, padx=500, pady=20)

        tk.Button(
            root,
            text='Back To Accounts', font=("Bahnschrift", 14),
            command=lambda: [root.destroy(), self.Accounts()]
        ).grid(column=0, row=0, sticky=tk.NW, padx=40, pady=20)

        tk.Button(
            root,
            text='Show Month', font=("Bahnschrift", 14),
            command=lambda: self.SurchMonth()
        ).grid(column=0, row=0, sticky=tk.NW, padx=750, pady=20)

    def FetchDataFromDatabase(self,month):
        for row in MonthlyMealAcc.treeview.get_children():
            MonthlyMealAcc.treeview.delete(row)

        r = MonthlyMealAcc.db.cursor()
        sql=f"""
            SELECT * FROM `student_account` WHERE `date` LIKE '{month}%'
            """
        r.execute(sql)
        rows = r.fetchall()
        MonthlyMealAcc.treeview.imglist = []
        for row in rows:
            img = Image.open(io.BytesIO(row[3]))
            img_resized = img.resize((50, 50))
            img = ImageTk.PhotoImage(img_resized)

            MonthlyMealAcc.treeview.insert(parent='', index='end', iid=row[0], text=' ' + str(row[0]), image=img,
                                             values=(row[2], row[4], row[1], row[5], row[6], row[7], row[8]))
            MonthlyMealAcc.treeview.imglist.append(img)

    def SurchMonth(self):
        a=MonthlyMealAcc.datepiker.get_date()
        self.FetchDataFromDatabase(str(a)[0:7])


    def Accounts(self):
        Accounts.AccDetails()