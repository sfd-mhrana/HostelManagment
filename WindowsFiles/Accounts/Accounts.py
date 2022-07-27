import tkinter as tk
from tkinter import ttk
import WindowsFiles.Mainwindow as Mainwindow
from WindowsFiles.Accounts import MealAccount
from WindowsFiles.Accounts import HostelAccount
from WindowsFiles.Accounts import MonthlyMealAcc
from WindowsFiles.Accounts import Student_Account
import MySQLdb as mdb

class AccDetails:

    global db,treeview,incomelavel,costlavel,lastlavel

    def Connection(self):
        try:
            AccDetails.db = mdb.connect('localhost', 'root', '', 'hostel_managment')

        except mdb.Error as e:
            print('Not Connect')

    def TableSection(self,root):

        frame = tk.Frame(root, width=1200, height=680, relief="groove", highlightbackground='#2C0036', highlightthicknes=3)

        my_game = ttk.Treeview(frame, height=23)
        AccDetails.treeview=my_game
        # scrollbar
        game_scroll = ttk.Scrollbar(frame, orient='horizontal')
        game_scroll.config(command=my_game.xview)

        my_game.configure(xscrollcommand=game_scroll.set)

        # define our column

        my_game['columns'] = ('id','details','date', 'amount', 'status')

        # format our column
        my_game.column("#0", width=0, stretch='NO',anchor="center")
        my_game.column("id",anchor="center", width=50)
        my_game.column("details",anchor="center", width=500)
        my_game.column("date",anchor="center", width=150)
        my_game.column("amount",anchor="center", width=300)
        my_game.column("status",anchor="center", width=200)

        # Create Headings
        my_game.heading("#0", text="")
        my_game.heading("id", text="ID")
        my_game.heading("details", text="Details")
        my_game.heading("date", text="Date" )
        my_game.heading("amount", text="Amount")
        my_game.heading("status", text="Status")


        my_game.pack()

        return  frame

    def __init__(self):
        self.Connection()
        root = tk.Tk()
        root.title('Sohid Sab Uddin Hostel ___ Accounts')
        root.attributes('-fullscreen', True)
        root.configure(bg='#6DC9F3')
        root.iconphoto(False, tk.PhotoImage(file='../asset/icon.png'))

        # layout on the root window
        root.columnconfigure(0)

        input_frame = self.TableSection(root)
        input_frame.grid(column=0, row=0,  sticky=tk.NW, padx=40, pady=80)

        tk.Button(
            root,
            text='Back To Home', font=("Bahnschrift", 14),
            command=lambda: [root.destroy(), self.Mainwindow()]
        ).grid(column=0, row=0, sticky=tk.NW, padx=40, pady=20)

        tk.Button(
            root,
            text='Hostel Amount', font=("Bahnschrift", 14),
            command=lambda: [root.destroy(), self.HostelAccount()]
        ).grid(column=0, row=0, sticky=tk.NW, padx=200, pady=20)

        tk.Button(
            root,
            text='Meal Amount', font=("Bahnschrift", 14),
            command=lambda: [root.destroy(), self.MealAccount()]
        ).grid(column=0, row=0, sticky=tk.NW, padx=370, pady=20)

        tk.Button(
            root,
            text='Monthly Meal Account', font=("Bahnschrift", 14),
            command=lambda: [root.destroy(), self.MonthlyMealAcc()]
        ).grid(column=0, row=0, sticky=tk.NW, padx=530, pady=20)

        tk.Button(
            root,
            text='Student Meal Account', font=("Bahnschrift", 14),
            command=lambda: [root.destroy(), self.StudentMealAcc()]
        ).grid(column=0, row=0, sticky=tk.NW, padx=760, pady=20)

        # replacement2 = tk.Entry(root, width=20, font=("Bahnschrift", 15))
        # replacement2.grid(column=0, row=0, sticky=tk.NW, padx=1080, pady=25)

        HostelAccount.incomelavel = tk.StringVar()
        tk.Label(root, font=("Bahnschrift", 14), textvariable=HostelAccount.incomelavel
                 ).grid(column=0, row=0, sticky=tk.NW, padx=100, pady=600)

        HostelAccount.costlavel = tk.StringVar()
        tk.Label(root, font=("Bahnschrift", 14), textvariable=HostelAccount.costlavel
                 ).grid(column=0, row=0, sticky=tk.NW, padx=400, pady=600)

        HostelAccount.lastlavel = tk.StringVar()
        tk.Label(root, font=("Bahnschrift", 14), textvariable=HostelAccount.lastlavel
                 ).grid(column=0, row=0, sticky=tk.NW, padx=800, pady=600)

        self.FetchAndSetData()
        root.mainloop()

    def FetchAndSetData(self):
        incomet=0
        costt=0
        r = AccDetails.db.cursor()
        r.execute("""SELECT * FROM `account` ORDER BY `date` ASC""")
        rows = r.fetchall()
        for row in rows:
            if row[4]=='Credit':
                incomet+=row[2]
            else:
                costt+= row[2]
            AccDetails.treeview.insert(parent='', index='end', iid=row[0], text='',
                                          values=(row[0],row[1], row[3], row[2], row[4]))

        lastamount = incomet - costt

        HostelAccount.incomelavel.set(f"Total Income: {incomet}")
        HostelAccount.costlavel.set(f"Total Cost: {costt}")
        HostelAccount.lastlavel.set(f"Last Amount: {lastamount}")

    def Mainwindow(self):
            Mainwindow.Mainwindow()

    def MealAccount(self):
            MealAccount.MealAccount()

    def HostelAccount(self):
            HostelAccount.HostelAccount()

    def MonthlyMealAcc(self):
        MonthlyMealAcc.MonthlyMealAcc()

    def StudentMealAcc(self):
        Student_Account.Student_Account()