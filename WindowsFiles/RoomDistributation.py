import tkinter as tk
from tkinter import ttk
import WindowsFiles.Mainwindow as Mainwindow
import MySQLdb as mdb
from datetime import date
from PIL import Image, ImageTk
import io
from tkinter import messagebox

class RoomDistributation:

    global db,room_name,room_withId,student_name,student_withId
    global room_combo,student_combo,selected_room_id,selected_student_id,r_or_p,alldata,table_data
    global treeview

    def Connection(self):
        try:
            RoomDistributation.db = mdb.connect('localhost', 'root', '', 'hostel_managment')

        except mdb.Error as e:
            print('Not Connect')

    def FromSection(self):

        frame = tk.Frame(background='#6DC9F3', highlightbackground='#2C0036',highlightthicknes=3)

        # Find what
        tk.Label(frame, text='Select Room Name' ,font = ("Bahnschrift", 14)).grid(column=0, row=0, sticky=tk.W,padx=10,pady=20)
        RoomDistributation.room_combo = ttk.Combobox(frame, width=28, font=("Bahnschrift", 15))
        RoomDistributation.room_combo['state'] = 'readonly'
        RoomDistributation.room_combo.bind('<<ComboboxSelected>>', self.RoomSelect)
        RoomDistributation.room_combo.grid(column=0, row=1, padx=10, pady=2)


        # Replace with:
        tk.Label(frame, text="Select Student",font = ("Bahnschrift", 14)).grid(column=0, row=2, sticky=tk.W,padx=10,pady=20)
        RoomDistributation.student_combo = ttk.Combobox(frame, width=28, font=("Bahnschrift", 15))
        RoomDistributation.student_combo['state'] = 'readonly'
        RoomDistributation.student_combo.bind('<<ComboboxSelected>>', self.StudentSelect)
        RoomDistributation.student_combo.grid(column=0, row=3,sticky=tk.W, padx=10, pady=2)

        # Replace with:
        tk.Label(frame, text='Status',font = ("Bahnschrift", 14)).grid(column=0, row=4, sticky=tk.W,padx=10,pady=20)
        RoomDistributation.r_or_p =  tk.StringVar()
        runningr = tk.Radiobutton(frame, bg='#6DC9F3', text="Running", variable=RoomDistributation.r_or_p, value="Running")
        runningr.select()
        runningr.grid(column=0, row=5, padx=10, pady=2, sticky=tk.W)
        passingr = tk.Radiobutton(frame, bg='#6DC9F3', text="Passing", variable=RoomDistributation.r_or_p, value="Passing")
        passingr.grid(column=0, row=5, padx=10, pady=2, sticky=tk.NS)

        self.getData()


        tk.Button(frame, text='Submit', font = ("Bahnschrift", 14), command=lambda: self.AddDataToDatabase()).grid(column=0, row=8, sticky=tk.SE, padx=10, pady=20)


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
        RoomDistributation.treeview = my_game

        game_scroll.config(command=my_game.yview)
        game_scroll.config(command=my_game.xview)

        # define our column

        my_game['columns'] = ('room_name', 'student_id', 'student_name', 'status', 'date')

        # format our column
        my_game.column("#0", width=100, anchor="center")
        my_game.column("room_name",  width=200,anchor="center")
        my_game.column("student_id",  width=90,anchor="center")
        my_game.column("student_name",  width=200,anchor="center")
        my_game.column("status", width=100,anchor="center")
        my_game.column("date",  width=150,anchor="center")

        # Create Headings
        my_game.heading("#0", text="IMG--ID")
        my_game.heading("room_name", text="Room Name")
        my_game.heading("student_id", text="Student Roll")
        my_game.heading("student_name", text="Student Name")
        my_game.heading("status", text="Status")
        my_game.heading("date", text="Date")

        # add data
        self.FetchTableData()

        my_game.pack()

        return  frame

    def __init__(self):
        self.Connection()
        root = tk.Tk()
        root.title('Sohid Sab Uddin Hostel ___ Room Distributation')
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
        ).grid(column=0, row=0,sticky=tk.NW,padx=40, pady=20)

        input_frame = self.FromSection()
        input_frame.grid(column=0, row=0,  sticky=tk.NW,padx=40,pady=80)

        button_frame = self.TableSection()
        button_frame.grid(column=1, row=0, sticky=tk.NW,pady=80)

        var = tk.StringVar()
        var.trace("w", lambda name, index, mode, var=var: self.SurchingStudentData(var))
        surching = tk.Entry(root, width=20, font=("Bahnschrift", 15), textvariable=var)
        surching.grid(column=1, row=0, sticky=tk.NE, padx=60, pady=20)

        s_room = tk.StringVar()
        s_room.trace("w", lambda name, index, mode, var=s_room: self.SurchingRoomData(s_room))
        surching = tk.Entry(root, width=20, font=("Bahnschrift", 15), textvariable=s_room)
        surching.grid(column=1, row=0, sticky=tk.NE, padx=350, pady=20)

        RoomDistributation.treeview.bind("<Double-1>", self.OnDoubleClick)

        RoomDistributation.selected_room_id=None
        RoomDistributation.selected_student_id=None

        root.mainloop()

    def SurchingStudentData(self, var):
        NewArray = []
        value=var.get()
        for data in RoomDistributation.alldata:
            if (value in str(data[5])):
                NewArray.append(data)
        self.AddDatatoTable(NewArray)

    def SurchingRoomData(self, var):
        NewArray = []
        value=var.get()
        for data in RoomDistributation.alldata:
            if (value in str(data[7])):
                NewArray.append(data)
        self.AddDatatoTable(NewArray)

    def FetchTableData(self):
        c = RoomDistributation.db.cursor()
        c.execute("""SELECT * FROM `distributation_s_r_details` ORDER BY d_id DESC""")

        rows = c.fetchall()
        RoomDistributation.alldata = rows
        RoomDistributation.table_data = RoomDistributation.alldata
        self.AddDatatoTable(RoomDistributation.table_data)

    def OnDoubleClick(self, event):
        item = RoomDistributation.treeview.selection()[0]
        values = RoomDistributation.treeview.item(item, "values")
        id = RoomDistributation.treeview.item(item, "text")
        if values[3]=='Running':
            MsgBox = tk.messagebox.askquestion('Status Chaning', 'Do You Want to Change Present Status?',
                                               icon='warning')
            if MsgBox == 'yes':
                c = RoomDistributation.db.cursor()
                c.execute("""UPDATE `hostel_managment`.`room_distributation`SET`status` = 'Passing'WHERE `ID` = %s""",
                              (id,)
                          )
                RoomDistributation.db.commit()
                self.FetchTableData()

        else:
            tk.messagebox.showwarning('Sorry', 'You Can not Change Passing Status. If You Need To Running It Please, Add New One',
                                               icon='warning')

    def getData(self):
        RoomDistributation.room_name=[]
        RoomDistributation.room_withId={}
        RoomDistributation.student_name=[]
        RoomDistributation.student_withId= {}

        r = RoomDistributation.db.cursor()
        r.execute("""SELECT * FROM `null_set_rooms`""")
        rooms = r.fetchall()
        for room in rooms:
            RoomDistributation.room_name.append(room[1])
            RoomDistributation.room_withId[room[1]]=room[0]

        s = RoomDistributation.db.cursor()
        s.execute("""SELECT * FROM `student_without_room`""")
        students = s.fetchall()
        for student in students:
            RoomDistributation.student_name.append(student[1])
            RoomDistributation.student_withId[student[1]] = student[0]

        RoomDistributation.room_combo['values'] = RoomDistributation.room_name
        RoomDistributation.student_combo['values'] = RoomDistributation.student_name

    def RoomSelect(self,event):
        RoomDistributation.selected_room_id= RoomDistributation.room_withId[RoomDistributation.room_combo.get()]

    def StudentSelect(self,event):
        RoomDistributation.selected_student_id= RoomDistributation.student_withId[RoomDistributation.student_combo.get()]

    def AddDataToDatabase(self):
        if RoomDistributation.selected_room_id is None:
            tk.messagebox.showwarning('Sorry',
                                      'Please, Select Room Frist',
                                      icon='warning')
        else:
            if RoomDistributation.selected_student_id is None:
                tk.messagebox.showwarning('Sorry',
                                          'Please, Select Student',
                                          icon='warning')
            else:
                room_id=RoomDistributation.selected_room_id
                st_id=RoomDistributation.selected_student_id
                status=RoomDistributation.r_or_p.get()

                today = date.today()
                d = RoomDistributation.db.cursor()
                d.execute(
                    """SELECT COUNT(*) AS `rows` FROM `hostel_managment`.`room_distributation` WHERE `status`='Running' AND `student_ID`=%s""",
                    (st_id,))

                rows = d.fetchall()
                if rows[0][0] == 0:
                    c = RoomDistributation.db.cursor()
                    a=c.execute("""INSERT INTO `hostel_managment`.`room_distributation`(`student_ID`,`room_ID`, `status`,`date`)
                        VALUES (%s,%s,%s,%s)""", (st_id, room_id, status,today, )
                              )
                    if(a):
                        self.getData()
                        self.FetchTableData()
                        self.ClearField()
                        RoomDistributation.db.commit()
                else:
                    tk.messagebox.showwarning('Sorry',
                                              'This Student Already Running in Another Room.',
                                              icon='warning')

    def AddDatatoTable(self,data):
        for row in RoomDistributation.treeview.get_children():
            RoomDistributation.treeview.delete(row)

        RoomDistributation.treeview.imglist = []
        for row in data:
            img = Image.open(io.BytesIO(row[6]))
            img_resized = img.resize((50, 50))
            img = ImageTk.PhotoImage(img_resized)

            RoomDistributation.treeview.insert(parent='', index='end', iid=row[0], text=' ' + str(row[0]), image=img,
                                              values=(row[7], row[5], row[4], row[8], row[3]))
            RoomDistributation.treeview.imglist.append(img)

    def ClearField(self):
        RoomDistributation.selected_room_id =None
        RoomDistributation.selected_student_id=None
        RoomDistributation.room_combo.set('')
        RoomDistributation.student_combo.set('')
        RoomDistributation.room_combo.focus()

    def Mainwindow(self):
            Mainwindow.Mainwindow()

