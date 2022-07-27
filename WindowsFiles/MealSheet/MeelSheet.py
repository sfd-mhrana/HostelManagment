import tkinter as tk
from tkinter import ttk
from WindowsFiles import Mainwindow
from tkinter import messagebox
from tkcalendar import DateEntry
import MySQLdb as mdb
from datetime import date
from PIL import Image, ImageTk
import io
from tkinter import messagebox

class MeelSheetDetails():

    global mealEdit,totalmealLabel
    global db,treeview,datepiker
    global room_name,room_withId,student_name,student_withId,room_combo,student_combo,selected_room_id,selected_student_id,r_or_p

    def Connection(self):
        try:
            MeelSheetDetails.db = mdb.connect('localhost', 'root', '', 'hostel_managment')

        except mdb.Error as e:
            print('Not Connect')

    def FromSection(self):
        frame = tk.Frame(background='#6DC9F3', highlightbackground='#2C0036', highlightthicknes=3)

        # Find what
        tk.Label(frame, text='Select Room Name', font=("Bahnschrift", 14)).grid(column=0, row=0, sticky=tk.W, padx=10,
                                                                                pady=20)
        selected_month = tk.StringVar()
        MeelSheetDetails.room_combo = ttk.Combobox(frame, textvariable=selected_month, width=28, font=("Bahnschrift", 15))
        MeelSheetDetails.room_combo['state'] = 'readonly'
        MeelSheetDetails.room_combo.bind('<<ComboboxSelected>>', self.RoomSelect)
        MeelSheetDetails.room_combo.grid(column=0, row=1, padx=10, pady=2)

        # Replace with:
        tk.Label(frame, text="Select Student", font=("Bahnschrift", 14)).grid(column=0, row=2, sticky=tk.W, padx=10,
                                                                              pady=20)
        select_student = tk.StringVar()
        MeelSheetDetails.student_combo = ttk.Combobox(frame, textvariable=select_student, width=28, font=("Bahnschrift", 15))
        MeelSheetDetails.student_combo['state'] = 'readonly'
        MeelSheetDetails.student_combo.bind('<<ComboboxSelected>>', self.StudentSelect)
        MeelSheetDetails.student_combo.grid(column=0, row=3, sticky=tk.W, padx=10, pady=2)

        # Replace with:
        tk.Label(frame, text='Meal Status', font=("Bahnschrift", 14)).grid(column=0, row=4, sticky=tk.W, padx=10, pady=20)
        MeelSheetDetails.r_or_p = tk.StringVar()
        runningr = tk.Radiobutton(frame, bg='#6DC9F3', text="Running", variable=MeelSheetDetails.r_or_p, value="Running")
        runningr.select()
        runningr.grid(column=0, row=5, padx=10, pady=2, sticky=tk.W)
        passingr = tk.Radiobutton(frame, bg='#6DC9F3', text="Passing", variable=MeelSheetDetails.r_or_p, value="Passing")
        passingr.grid(column=0, row=5, padx=10, pady=2, sticky=tk.NS)

        tk.Button(frame, text='Submit', font=("Bahnschrift", 14), command=lambda: self.GetSelectedData()).grid(column=0, row=8,
                                                                                                       sticky=tk.SE,
                                                                                                       padx=10, pady=20)
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

        my_game = ttk.Treeview(frame, height=7, yscrollcommand=game_scroll.set, xscrollcommand=game_scroll.set)

        my_game.pack()

        game_scroll.config(command=my_game.yview)
        game_scroll.config(command=my_game.xview)

        # define our column

        my_game['columns'] = ('room_name', 'student_id', 'student_name', 'status', 'date')

        # format our column
        my_game.column("#0", width=100, anchor="center")
        my_game.column("room_name", width=200, anchor="center")
        my_game.column("student_id", width=50, anchor="center")
        my_game.column("student_name", width=200, anchor="center")
        my_game.column("status", width=100, anchor="center")
        my_game.column("date", width=200, anchor="center")

        # Create Headings
        my_game.heading("#0", text="IMG--Room ID")
        my_game.heading("room_name", text="Room Name")
        my_game.heading("student_id", text="Student ID")
        my_game.heading("student_name", text="Student Name")
        my_game.heading("status", text="Meal")
        my_game.heading("date", text="Date")

        MeelSheetDetails.treeview = my_game

        self.DateMealAddToTable(date.today())

        my_game.pack()

        return frame

    def __init__(self):
        self.Connection()

        root = tk.Tk()
        root.title('Sohid Sab Uddin Hostel ___ Meal Sheet')
        root.attributes('-fullscreen', True)
        root.configure(bg='#6DC9F3')
        root.iconphoto(False, tk.PhotoImage(file='../asset/icon.png'))

        # layout on the root window
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=4)

        tk.Button(
            root,
            text='Back To Home', font=("Bahnschrift", 14),
            command=lambda: [root.destroy(), self.Mainwindow()]
        ).grid(column=0, row=0, sticky=tk.NW, padx=40, pady=20)

        tk.Button(
            root,
            text='Add Meal', font=("Bahnschrift", 14),
            command=lambda: self.AutoMealAdd(root)
        ).grid(column=0, row=0, sticky=tk.NW, padx=40, pady=110)

        input_frame = self.FromSection()
        input_frame.grid(column=0, row=0, sticky=tk.NW, padx=40, pady=180)

        MeelSheetDetails.datepiker = DateEntry(root,height=20,width=30, fg="white")
        MeelSheetDetails.datepiker.grid(column=1, row=0, sticky=tk.NW, pady=20)

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

        MeelSheetDetails.totalmealLabel= tk.StringVar()
        tk.Label(root, text='', font=("Bahnschrift", 14),textvariable=MeelSheetDetails.totalmealLabel
                                                  ).grid(column=1, row=0, sticky=tk.E,  padx=80,  pady=650)

        button_frame = self.TableSection()
        button_frame.grid(column=1, row=0, sticky=tk.NW, pady=80)


        self.FetchRunnigStudent()

        MeelSheetDetails.treeview.bind("<Double-1>", self.OnDoubleClick)

        MeelSheetDetails.selected_room_id = None
        MeelSheetDetails.selected_student_id = None

        root.mainloop()

    def AutoMealAdd(self,root):
        today = date.today()
        length=len(MeelSheetDetails.room_name)
        for i in range(0,length):
            roomid=MeelSheetDetails.room_withId[MeelSheetDetails.room_name[i]]
            studentname = []
            studentnameid = {}
            r = MeelSheetDetails.db.cursor()
            r.execute("""SELECT * FROM `running_student` WHERE room_ID=%s""",
                      (roomid,))
            rows = r.fetchall()
            for row in rows:
                studentname.append(row[3])
                studentnameid[row[3]] = row[1]

            student = len(studentname)
            for j in range(0, student):
                MsgBox = messagebox.askyesnocancel('Do You Want To Add Meal?',
                                                   'Room Name : ' + MeelSheetDetails.room_name[i] + '\nStudent Name : ' + studentname[j],
                                                   icon='warning')
                if MsgBox:
                    a=self.AddDataToDataBase(MeelSheetDetails.room_withId[MeelSheetDetails.room_name[i]],
                                           studentnameid[studentname[j]],today,'Running')
                    if(a):
                        pass
                elif MsgBox is None:
                    messagebox.showinfo('Warning', 'You Cancel Auto Add Mean',icon='warning')
                else:
                    a = self.AddDataToDataBase(MeelSheetDetails.room_withId[MeelSheetDetails.room_name[i]],
                                               studentnameid[studentname[j]], today, 'Passing')
                    if (a):
                        pass

    def FetchRunnigStudent(self):
        MeelSheetDetails.room_name = []
        MeelSheetDetails.room_withId = {}
        r = MeelSheetDetails.db.cursor()
        r.execute("""SELECT * FROM `running_student` GROUP BY room_ID ORDER BY Room_Name ASC""")
        rows = r.fetchall()
        for row in rows:
            MeelSheetDetails.room_name.append(row[7])
            MeelSheetDetails.room_withId[row[7]] = row[0]


        MeelSheetDetails.room_combo['values'] = MeelSheetDetails.room_name

    def RoomSelect(self,event):
        MeelSheetDetails.selected_room_id= MeelSheetDetails.room_withId[MeelSheetDetails.room_combo.get()]
        MeelSheetDetails.student_name = []
        MeelSheetDetails.student_withId = {}

        MeelSheetDetails.student_combo.set('')
        r = MeelSheetDetails.db.cursor()
        r.execute("""SELECT * FROM `running_student` WHERE room_ID=%s""",(MeelSheetDetails.selected_room_id,))
        rows = r.fetchall()
        for row in rows:
            MeelSheetDetails.student_name.append(row[3])
            MeelSheetDetails.student_withId[row[3]] = row[1]

        MeelSheetDetails.student_combo['values']=MeelSheetDetails.student_name

    def StudentSelect(self,event):
        MeelSheetDetails.selected_student_id= MeelSheetDetails.student_withId[MeelSheetDetails.student_combo.get()]

    def GetSelectedData(self):
        if MeelSheetDetails.selected_room_id is None:
            tk.messagebox.showwarning('Sorry',
                                      'Please, Select Room Frist',
                                      icon='warning')
        else:
            if MeelSheetDetails.selected_student_id is None:
                tk.messagebox.showwarning('Sorry',
                                          'Please, Select Student',
                                          icon='warning')
            else:
                room_id = MeelSheetDetails.selected_room_id
                st_id = MeelSheetDetails.selected_student_id
                status = MeelSheetDetails.r_or_p.get()
                today = date.today()
                a=self.AddDataToDataBase(room_id,st_id,today,status)
                if(a):
                    pass

    def AddDataToDataBase(self,r,s,d,st):
        k = MeelSheetDetails.db.cursor()
        k.execute(
            """SELECT COUNT(*) AS row_no FROM `hostel_managment`.`meal_sheet` WHERE `room_ID`=%s AND `student_ID`=%s AND `date`=%s""",
            (r, s, d,))
        rows = k.fetchall()
        if rows[0][0] == 0:
            c = MeelSheetDetails.db.cursor()
            a = c.execute("""INSERT INTO `hostel_managment`.`meal_sheet`(`room_ID`,`student_ID`,`date`,`A_P`)
                                                        VALUES (%s,%s,%s,%s)""", (r, s, d, st,))
            if (a):
                self.DateMealAddToTable(date.today())
                self.ClearField()
                MeelSheetDetails.db.commit()
                return True
            else:
                return False
        else:
            tk.messagebox.showwarning('Sorry',
                                      'This Student Meal Add for ' + str(d) + ' Date',
                                      icon='warning')
            return False

    def ClearField(self):
        MeelSheetDetails.selected_room_id = None
        MeelSheetDetails.selected_student_id = None
        MeelSheetDetails.room_combo.set('')
        MeelSheetDetails.student_combo.set('')

    def SurchDate(self):
        self.DateMealAddToTable(MeelSheetDetails.datepiker.get_date())

    def SurchMonth(self):
        a=MeelSheetDetails.datepiker.get_date()
        self.MonthMealAddToTable(str(a)[0:7])

    def DateMealAddToTable(self,date):
        totalmeal=0;
        MeelSheetDetails.mealEdit='Date'
        for row in MeelSheetDetails.treeview.get_children():
            MeelSheetDetails.treeview.delete(row)

        r = MeelSheetDetails.db.cursor()
        r.execute("""SELECT * FROM `meal_sheet_view` WHERE `date`=%s ORDER BY Room_Name ASC""",
                  (date,))
        rows = r.fetchall()
        MeelSheetDetails.treeview.imglist = []
        for row in rows:
            img = Image.open(io.BytesIO(row[6]))
            img_resized = img.resize((50, 50))
            img = ImageTk.PhotoImage(img_resized)
            if row[3]=='Running':
                    totalmeal+=1
            MeelSheetDetails.treeview.insert(parent='', index='end', iid=row[0], text=' ' + str(row[1]), image=img,
                                               values=(row[7], row[2], row[5], row[3], row[4]))
            MeelSheetDetails.treeview.imglist.append(img)


        MeelSheetDetails.totalmealLabel.set(f"Total Meal: {totalmeal}")

    def MonthMealAddToTable(self,month):
        totalmeal=0
        MeelSheetDetails.mealEdit = 'Month'
        for row in MeelSheetDetails.treeview.get_children():
            MeelSheetDetails.treeview.delete(row)

        r = MeelSheetDetails.db.cursor()
        sql=f"""
            SELECT meal_id,room_ID,student_ID,A_P,`date`,student_name,IMG,Room_Name,COUNT(*) AS meal FROM `meal_sheet_view`WHERE A_P='Running' AND`date` LIKE '{month}%' 
            GROUP BY room_ID,student_ID ORDER BY Room_Name ASC
            """
        r.execute(sql)
        rows = r.fetchall()
        MeelSheetDetails.treeview.imglist = []
        for row in rows:
            img = Image.open(io.BytesIO(row[6]))
            img_resized = img.resize((50, 50))
            img = ImageTk.PhotoImage(img_resized)
            totalmeal+=row[8]
            MeelSheetDetails.treeview.insert(parent='', index='end', iid=row[0], text=' ' + str(row[1]), image=img,
                                             values=(row[7], row[2], row[5], row[8], row[4]))
            MeelSheetDetails.treeview.imglist.append(img)
        MeelSheetDetails.totalmealLabel.set(f"Total Meal: {totalmeal}")

    def OnDoubleClick(self, event):
        if MeelSheetDetails.mealEdit=='Date':
            item = MeelSheetDetails.treeview.selection()[0]
            values = MeelSheetDetails.treeview.item(item, "values")
            id = MeelSheetDetails.treeview.item(item, "text")
            if values[4]==str(date.today()):
                if values[3] == 'Running':
                    MsgBox = tk.messagebox.askquestion('Status Chaning', 'Do You Want to Change Present Status?',
                                                       icon='warning')
                    if MsgBox == 'yes':
                        c = MeelSheetDetails.db.cursor()
                        c.execute(
                            """UPDATE `hostel_managment`.`meal_sheet`SET `A_P` = 'Passing' WHERE `ID` = %s""",
                            (item,)
                            )
                        self.DateMealAddToTable(date.today())
                        MeelSheetDetails.db.commit()

                else:
                    MsgBox = tk.messagebox.askquestion('Status Chaning', 'Do You Want to Change Present Status?',
                                                       icon='warning')
                    if MsgBox == 'yes':
                        c = MeelSheetDetails.db.cursor()
                        c.execute(
                            """UPDATE `hostel_managment`.`meal_sheet`SET `A_P` = 'Running' WHERE `ID` = %s""",
                            (item,)
                        )
                        self.DateMealAddToTable(date.today())
                        MeelSheetDetails.db.commit()
            else:
                tk.messagebox.showwarning('Sorry',
                                          'You Can not Change Passing Status. Because This Meal Already Count',
                                          icon='warning')
        else:
            tk.messagebox.showwarning('Sorry',
                                      'You Can Edit Day Table Meal, Please, Select Date',
                                      icon='warning')

    def Mainwindow(self):
            Mainwindow.Mainwindow()


