import tkinter as tk
from tkinter import ttk
from WindowsFiles.Accounts import Accounts
from tkinter import messagebox
from tkcalendar import DateEntry
import MySQLdb as mdb
from datetime import date

class HostelAccount:
    global details,amount,c_i,db,treeview,incomelavel,costlavel,lastlavel,datepiker

    def Connection(self):
        try:
            HostelAccount.db = mdb.connect('localhost', 'root', '', 'hostel_managment')

        except mdb.Error as e:
            print('Not Connect')

    def FromSection(self):

        frame = tk.Frame(background='#6DC9F3', highlightbackground='#2C0036',highlightthicknes=3)
        # Find what
        tk.Label(frame, text='Details', font=("Bahnschrift", 14)).grid(column=0, row=0, sticky=tk.W,padx=10,pady=20)
        HostelAccount.details = tk.Entry(frame, width=30, font=("Bahnschrift", 15))
        HostelAccount.details.grid(column=0, row=1, padx=10, pady=2)

        # Replace with:
        tk.Label(frame, text="Amount", font=("Bahnschrift", 14)).grid(column=0, row=2, sticky=tk.W, padx=10,
                                                                           pady=20)
        HostelAccount.amount = tk.Entry(frame, width=30, font=("Bahnschrift", 15))
        HostelAccount.amount.grid(column=0, row=3, sticky=tk.W, padx=10, pady=2)

        # Replace with:
        tk.Label(frame, text='Status',font = ("Bahnschrift", 14)).grid(column=0, row=4, sticky=tk.W,padx=10,pady=20)
        HostelAccount.c_i = tk.StringVar()
        runningr = tk.Radiobutton(frame, bg='#6DC9F3', text="Cost", variable=HostelAccount.c_i, value="cost")
        runningr.select()
        runningr.grid(column=0, row=5, padx=10, pady=2, sticky=tk.W)
        passingr = tk.Radiobutton(frame, bg='#6DC9F3', text="Income", variable=HostelAccount.c_i, value="income")
        passingr.grid(column=0, row=5, padx=10, pady=2, sticky=tk.NS)

        tk.Button(frame, text='Submit', font = ("Bahnschrift", 14), command=lambda: self.AddDataToDatabase()).grid(column=0, row=8, sticky=tk.SE, padx=10, pady=20)


        return frame

    def TableSection(self):
        frame = tk.Frame(background='#6DC9F3', highlightbackground='#2C0036', highlightthicknes=3)

        # scrollbar
        game_scroll = ttk.Scrollbar(frame)
        game_scroll.pack(side='right', fill='y')

        game_scroll = ttk.Scrollbar(frame, orient='horizontal')
        game_scroll.pack(side='bottom', fill='x')

        my_game = ttk.Treeview(frame,height = 23, yscrollcommand=game_scroll.set, xscrollcommand=game_scroll.set)
        HostelAccount.treeview=my_game

        game_scroll.config(command=my_game.yview)
        game_scroll.config(command=my_game.xview)

        # define our column

        my_game['columns'] = ('id', 'details', 'date', 'amount', 'cost')

        # format our column
        my_game.column("#0", width=0, stretch='NO',anchor="center")
        my_game.column("id",  width=40,anchor="center")
        my_game.column("details",  width=200,anchor="center")
        my_game.column("date",  width=200,anchor="center")
        my_game.column("amount",  width=200,anchor="center")
        my_game.column("cost", width=200,anchor="center")

        # Create Headings
        my_game.heading("#0", text="")
        my_game.heading("id", text="Id")
        my_game.heading("details", text="Details")
        my_game.heading("date", text="Date")
        my_game.heading("amount", text="Amount")
        my_game.heading("cost", text="Cost")

        my_game.pack()

        return  frame

    def __init__(self):
        self.Connection()
        root = tk.Tk()
        root.title('Sohid Sab Uddin Hostel ___ Hostel Account')
        root.attributes('-fullscreen', True)
        root.configure(bg='#6DC9F3')
        root.iconphoto(False, tk.PhotoImage(file='../asset/icon.png'))

        # layout on the root window
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=4)

        tk.Button(
            root,
            text='Back To Accounts', font=("Bahnschrift", 14),
            command=lambda: [root.destroy(), self.Accounts()]
        ).grid(column=0, row=0,sticky=tk.NW,padx=40, pady=20)

        input_frame = self.FromSection()
        input_frame.grid(column=0, row=0,  sticky=tk.NW,padx=40,pady=80)

        button_frame = self.TableSection()
        button_frame.grid(column=1, row=0, sticky=tk.NW,pady=80)

        HostelAccount.datepiker = DateEntry(root, height=20, width=30, fg="white")
        HostelAccount.datepiker.grid(column=1, row=0, sticky=tk.NW, pady=20)

        tk.Button(
            root,
            text='Show Month', font=("Bahnschrift", 14),
            command=lambda: self.SurchMonth()
        ).grid(column=1, row=0, sticky=tk.NW, padx=250, pady=20)

        tk.Button(
            root,
            text='Show Date', font=("Bahnschrift", 14),
            command=lambda: self.SurchDate()
        ).grid(column=1, row=0, sticky=tk.NW, padx=400, pady=20)





        HostelAccount.incomelavel = tk.StringVar()
        tk.Label(root, font=("Bahnschrift", 14), textvariable=HostelAccount.incomelavel
                 ).grid(column=1, row=0, sticky=tk.NW,  pady=600)

        HostelAccount.costlavel = tk.StringVar()
        tk.Label(root, font=("Bahnschrift", 14), textvariable=HostelAccount.costlavel
                 ).grid(column=1, row=0, sticky=tk.NS, pady=600)

        HostelAccount.lastlavel = tk.StringVar()
        tk.Label(root, font=("Bahnschrift", 14), textvariable=HostelAccount.lastlavel
                 ).grid(column=1, row=0, sticky=tk.SE, padx=80, pady=600)

        self.FetchDataFromDatabase()

        root.mainloop()

    def AddDataToDatabase(self):
        a=HostelAccount.details.get()
        b=HostelAccount.amount.get()
        c=HostelAccount.c_i.get()
        d=date.today()
        if(len(a)!=0):
            if(len(b)!=0):
                if(c=='cost'):
                    co = HostelAccount.db.cursor()
                    k = co.execute("""INSERT INTO `hostel_managment`.`hostel_free`(`date`, `details`,`cost`)
                    VALUES (%s,%s,%s)""",(d,a,b,))

                    z = HostelAccount.db.cursor()
                    z.execute(
                        """INSERT INTO `hostel_managment`.`account`(`details`,`amount`,`date`,`status`) VALUES (%s,%s,%s,%s)""",
                        (a,b, d, 'Devit',))
                else:
                    co = HostelAccount.db.cursor()
                    k = co.execute("""INSERT INTO `hostel_managment`.`hostel_free`(`date`, `details`,`amount`)
                    VALUES (%s,%s,%s)""",(d,a,b,))

                    z = HostelAccount.db.cursor()
                    z.execute(
                        """INSERT INTO `hostel_managment`.`account`(`details`,`amount`,`date`,`status`) VALUES (%s,%s,%s,%s)""",
                        (a, b, d, 'Credit',))

                if(k):
                    pass
                HostelAccount.db.commit()
                self.FetchDataFromDatabase()
            else:
                tk.messagebox.showwarning('Sorry',
                                          'Please, Enter Amount',
                                          icon='warning')
        else:
            tk.messagebox.showwarning('Sorry',
                                      'Please, Enter Details',
                                      icon='warning')

    def FetchDataFromDatabase(self):
        HostelAccount.AllData=[]
        HostelAccount.TableData=[]
        r = HostelAccount.db.cursor()
        r.execute("""SELECT*FROM `hostel_managment`.`hostel_free`""")
        rows = r.fetchall()
        self.SetDataToTable(rows)

    def SetDataToTable(self,data):

        for row in HostelAccount.treeview.get_children():
            HostelAccount.treeview.delete(row)

        incomet=0
        costt=0
        for row in data:
            incomet+=row[4]
            costt+= row[5]
            HostelAccount.treeview.insert(parent='', index='end', iid=row[0], text='',
                                          values=(row[0], row[3], row[2], row[4], row[5]))

        lastamount=incomet-costt

        HostelAccount.incomelavel.set(f"Total Income: {incomet}")
        HostelAccount.costlavel.set(f"Total Cost: {costt}")
        HostelAccount.lastlavel.set(f"Last Amount: {lastamount}")

    def SurchDate(self):
        self.DateMealAddToTable(HostelAccount.datepiker.get_date())

    def SurchMonth(self):
        a=HostelAccount.datepiker.get_date()
        self.MonthMealAddToTable(str(a)[0:7])

    def DateMealAddToTable(self, date):

        for row in HostelAccount.treeview.get_children():
            HostelAccount.treeview.delete(row)

        r = HostelAccount.db.cursor()
        r.execute("""SELECT*FROM `hostel_managment`.`hostel_free` WHERE `date`=%s""",
                  (date,))
        rows = r.fetchall()
        self.SetDataToTable(rows)

    def MonthMealAddToTable(self,month):
        for row in HostelAccount.treeview.get_children():
            HostelAccount.treeview.delete(row)

        r = HostelAccount.db.cursor()
        sql=f"""
           SELECT `ID`,`student_ID`,`date`,`details`,SUM(`amount`) ,SUM(`cost`)FROM `hostel_managment`.`hostel_free` WHERE `date` LIKE '{month}%' GROUP BY `date`
            """
        r.execute(sql)
        rows = r.fetchall()
        self.SetDataToTable(rows)

    def Accounts(self):
            Accounts.AccDetails()
