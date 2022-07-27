import tkinter as tk
from tkinter import ttk
from WindowsFiles.Accounts import Accounts
import MySQLdb as mdb
from datetime import date
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import io
from tkinter import messagebox

class MealAccount:

    global db
    global room_name, room_withId, student_name, student_withId, room_combo, student_combo, selected_room_id, selected_student_id, r_or_p
    global amount,treeview,datepiker

    def Connection(self):
        try:
            MealAccount.db = mdb.connect('localhost', 'root', '', 'hostel_managment')

        except mdb.Error as e:
            print('Not Connect')

    def FromSection(self):

        frame = tk.Frame(background='#6DC9F3', highlightbackground='#2C0036',highlightthicknes=3)

        # Find what
        tk.Label(frame, text='Select Room Name' ,font = ("Bahnschrift", 14)).grid(column=0, row=0, sticky=tk.W,padx=10,pady=20)
        selected_month = tk.StringVar()
        MealAccount.room_combo = ttk.Combobox(frame, textvariable=selected_month, width=28, font=("Bahnschrift", 15))
        MealAccount.room_combo.bind('<<ComboboxSelected>>', self.RoomSelect)
        MealAccount.room_combo['state'] = 'readonly'
        MealAccount.room_combo.grid(column=0, row=1, padx=10, pady=2)


        # Replace with:
        tk.Label(frame, text="Select Student",font = ("Bahnschrift", 14)).grid(column=0, row=2, sticky=tk.W,padx=10,pady=20)
        select_student = tk.StringVar()
        MealAccount.student_combo = ttk.Combobox(frame, textvariable=select_student, width=28, font=("Bahnschrift", 15))
        MealAccount.student_combo.bind('<<ComboboxSelected>>', self.StudentSelect)
        MealAccount.student_combo['state'] = 'readonly'
        MealAccount.student_combo.grid(column=0, row=3,sticky=tk.W, padx=10, pady=2)

        # Find what
        tk.Label(frame, text='Amount', font=("Bahnschrift", 14)).grid(column=0, row=4, sticky=tk.W, padx=10, pady=20)
        MealAccount.amount= tk.Entry(frame, width=30, font=("Bahnschrift", 15))
        MealAccount.amount.grid(column=0, row=5, padx=10, pady=2)

        # Replace with:
        tk.Label(frame, text='Status',font = ("Bahnschrift", 14)).grid(column=0, row=6, sticky=tk.W,padx=10,pady=20)
        MealAccount.r_or_p = tk.StringVar()
        runningr = tk.Radiobutton(frame, bg='#6DC9F3', text="Devit", variable=MealAccount.r_or_p, value="Devit")
        runningr.grid(column=0, row=7, padx=10, pady=2, sticky=tk.W)
        passingr = tk.Radiobutton(frame, bg='#6DC9F3', text="Credit", variable=MealAccount.r_or_p, value="Credit")
        passingr.grid(column=0, row=7, padx=10, pady=2, sticky=tk.NS)
        passingr.select()

        tk.Button(frame, text='Submit', font = ("Bahnschrift", 14), command=lambda: self.GetSelectedData()).grid(column=0, row=9, sticky=tk.SE, padx=10, pady=20)


        return frame

    def TableSection(self):
        frame = tk.Frame(background='#6DC9F3', highlightbackground='#2C0036', highlightthicknes=3)
        style = ttk.Style(frame)
        style.configure('Treeview', rowheight=70)
        # scrollbar
        game_scroll = ttk.Scrollbar(frame)
        game_scroll.pack(side='right', fill='y')

        game_scroll = ttk.Scrollbar(frame, orient='horizontal')
        game_scroll.pack(side='bottom', fill='x')

        my_game = ttk.Treeview(frame,height = 8, yscrollcommand=game_scroll.set, xscrollcommand=game_scroll.set)

        MealAccount.treeview=my_game

        game_scroll.config(command=my_game.yview)
        game_scroll.config(command=my_game.xview)

        # define our column

        my_game['columns'] = ('room_name', 'student_name', 'amount','date', 'status')

        # format our column
        my_game.column("#0", width=100,anchor="center")
        my_game.column("room_name",  width=100,anchor="center")
        my_game.column("student_name",  width=200,anchor="center")
        my_game.column("amount",  width=150,anchor="center")
        my_game.column("date",  width=150,anchor="center")
        my_game.column("status", width=100,anchor="center")

        # Create Headings
        my_game.heading("#0", text="IMG--ID")
        my_game.heading("room_name", text="Room Name")
        my_game.heading("student_name", text="Student Name")
        my_game.heading("amount", text="Amount")
        my_game.heading("date", text="Date")
        my_game.heading("status", text="Status")

        self.DateMealAddToTable(date.today())

        my_game.pack()

        return  frame

    def __init__(self):
        self.Connection()

        root = tk.Tk()
        root.title('Sohid Sab Uddin Hostel ___ Meal Account')
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

        MealAccount.datepiker = DateEntry(root, height=20, width=30, fg="white")
        MealAccount.datepiker.grid(column=1, row=0, sticky=tk.NW, pady=20)

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

        self.FetchRunnigStudent()

        MealAccount.selected_room_id = None
        MealAccount.selected_student_id = None

        root.mainloop()

    def FetchRunnigStudent(self):
        MealAccount.room_name = []
        MealAccount.room_withId = {}
        r = MealAccount.db.cursor()
        r.execute("""SELECT * FROM `running_student` GROUP BY room_ID ORDER BY Room_Name ASC""")
        rows = r.fetchall()
        for row in rows:
            MealAccount.room_name.append(row[7])
            MealAccount.room_withId[row[7]] = row[0]


        MealAccount.room_combo['values'] = MealAccount.room_name

    def RoomSelect(self,event):
        MealAccount.selected_room_id= MealAccount.room_withId[MealAccount.room_combo.get()]
        MealAccount.student_name = []
        MealAccount.student_withId = {}

        MealAccount.student_combo.set('')
        r = MealAccount.db.cursor()
        r.execute("""SELECT * FROM `running_student` WHERE room_ID=%s""",(MealAccount.selected_room_id,))
        rows = r.fetchall()
        for row in rows:
            MealAccount.student_name.append(row[3])
            MealAccount.student_withId[row[3]] = row[1]

        MealAccount.student_combo['values']=MealAccount.student_name

    def StudentSelect(self,event):
        MealAccount.selected_student_id= MealAccount.student_withId[MealAccount.student_combo.get()]

    def GetSelectedData(self):
        if MealAccount.selected_room_id is None:
            tk.messagebox.showwarning('Sorry',
                                      'Please, Select Room Frist',
                                      icon='warning')
        else:
            if MealAccount.selected_student_id is None:
                tk.messagebox.showwarning('Sorry',
                                          'Please, Select Student',
                                          icon='warning')
            else:
                if len(MealAccount.amount.get())==0:
                    tk.messagebox.showwarning('Sorry',
                                              'Please, Entry Amount',
                                              icon='warning')
                else:
                    room_id = MealAccount.selected_room_id
                    st_id = MealAccount.selected_student_id
                    amount=MealAccount.amount.get()
                    status = MealAccount.r_or_p.get()
                    today = date.today()
                    a=self.AddDataToDataBase(room_id,st_id,today,amount,status)
                    if(a):
                        self.DateMealAddToTable(date.today())

    def AddDataToDataBase(self,r,s,d,a,st):
        z=str(d)[0:7]
        k=MealAccount.db.cursor()
        k.execute(f"""SELECT*FROM `hostel_managment`.`hostel_free` WHERE`student_ID`='{s}' AND `date` LIKE '{z}%'""")
        rows = k.fetchall()
        if len(rows)==0:
            k = MealAccount.db.cursor()
            k.execute(f"""SELECT*FROM `hostel_managment`.`set_value`WHERE`date` LIKE '{z}%'""")
            collection = k.fetchall()
            if(len(collection)!=0):
                col=collection[0][2]
                a=int(a)-int(col)
                co=MealAccount.db.cursor()
                k=co.execute("""INSERT INTO `hostel_managment`.`hostel_free` (`student_ID`,`date`,`details`,`amount`)
                            VALUES (%s,%s,%s,%s)""",(s,d,'Student Hostel Free',col))
                if(k):
                    p = MealAccount.db.cursor()
                    p.execute(
                        """INSERT INTO `hostel_managment`.`account`(`details`,`amount`,`date`,`status`) VALUES (%s,%s,%s,%s)""",
                        (str(s) + "/Student Hostel Free", col, d, 'Credit',))

                    if a<0:
                        a=-a
                        st='Devit'

                    c = MealAccount.db.cursor()
                    b = c.execute("""INSERT INTO `hostel_managment`.`meal_free`(`room_id`,`student_ID`,`date`,`amount`,`status`)
                                                VALUES (%s,%s,%s,%s,%s)""", (r, s, d, a, st,))
                    if (b):
                        k = MealAccount.db.cursor()
                        k.execute(
                                """INSERT INTO `hostel_managment`.`account`(`details`,`amount`,`date`,`status`) VALUES (%s,%s,%s,%s)""",
                                (str(s) + "/Meal Payment", a, d, st,))
                        self.ClearField()
                        MealAccount.db.commit()
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                tk.messagebox.showwarning('Sorry',
                                          'Please, Set Hostel Meal And Collection Ret For This Month',
                                          icon='warning')
        else:
            c = MealAccount.db.cursor()
            b = c.execute("""INSERT INTO `hostel_managment`.`meal_free`(`room_id`,`student_ID`,`date`,`amount`,`status`)
                            VALUES (%s,%s,%s,%s,%s)""", (r,s, d, a, st,))
            if(b):
                k=MealAccount.db.cursor()
                k.execute("""INSERT INTO `hostel_managment`.`account`(`details`,`amount`,`date`,`status`) VALUES (%s,%s,%s,%s)""",
                          (str(s)+"/Meal Payment",a,d,st,))
                self.ClearField()
                MealAccount.db.commit()
                return True
            else:
                return False

    def ClearField(self):
        MealAccount.selected_room_id = None
        MealAccount.selected_student_id = None
        MealAccount.room_combo.set('')
        MealAccount.student_combo.set('')
        MealAccount.amount.delete(0, 'end')
        MealAccount.room_combo.focus()

    def SurchDate(self):
        self.DateMealAddToTable(MealAccount.datepiker.get_date())

    def SurchMonth(self):
        a=MealAccount.datepiker.get_date()
        self.MonthMealAddToTable(str(a)[0:7])

    def DateMealAddToTable(self, date):

        for row in MealAccount.treeview.get_children():
            MealAccount.treeview.delete(row)

        r = MealAccount.db.cursor()
        r.execute("""SELECT ID,room_id,student_ID,`date`,SUM(amount) AS amount,`status`,student_name,IMG,Room_Name
                            FROM `meal_free_view` WHERE `date`=%s GROUP BY student_ID,`status`""",
                  (date,))
        rows = r.fetchall()
        MealAccount.treeview.imglist = []
        for row in rows:
            img = Image.open(io.BytesIO(row[7]))
            img_resized = img.resize((50, 50))
            img = ImageTk.PhotoImage(img_resized)

            MealAccount.treeview.insert(parent='', index='end', iid=row[0], text=' ' + str(row[0]), image=img,
                                             values=(row[8], row[6], row[4], row[3], row[5]))
            MealAccount.treeview.imglist.append(img)

    def MonthMealAddToTable(self,month):
        count=0
        for row in MealAccount.treeview.get_children():
            MealAccount.treeview.delete(row)

        r = MealAccount.db.cursor()
        sql=f"""
           SELECT * FROM `monthly_meal_amount_view` WHERE `date`LIKE '{month}%'
            """
        r.execute(sql)
        rows = r.fetchall()
        MealAccount.treeview.imglist = []
        for row in rows:
            count +=1
            img = Image.open(io.BytesIO(row[5]))
            img_resized = img.resize((50, 50))
            img = ImageTk.PhotoImage(img_resized)
            if(row[3]<0):
                status='Devit'
            else:
                status='Credit'
            MealAccount.treeview.insert(parent='', index='end', iid=count, text=' ' + str(row[0]), image=img,
                                        values=(row[6], row[4], row[3], row[2], status
                                                ))
            MealAccount.treeview.imglist.append(img)

    def Accounts(self):
        Accounts.AccDetails()
