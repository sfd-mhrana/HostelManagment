import tkinter as tk
from tkinter import ttk
from WindowsFiles import Mainwindow
from WindowsFiles.Students import NewStudent
from PIL import Image, ImageTk
import MySQLdb as mdb
import io
from tkinter import messagebox

class StudentDetails():

    global bd,allData,showdata,treeviewgui

    def Connection(self):
        try:
            StudentDetails.db = mdb.connect('localhost', 'root', '', 'hostel_managment')
            #print('Connect')
        except mdb.Error as e:
            print('Not Connect')

    def TableSection(self,root):

        frame = tk.Frame(root, width=1200, height=680, relief="groove", highlightbackground='#2C0036', highlightthicknes=3)

        style = ttk.Style(frame)
        style.configure('Treeview', rowheight=70)

        # scrollbar
        game_scroll = ttk.Scrollbar(frame)
        game_scroll.pack(side='right', fill='y')

        game_scroll = ttk.Scrollbar(frame, orient='horizontal')
        game_scroll.pack(side='bottom', fill='x')

        my_game = ttk.Treeview(frame,height=8, yscrollcommand=game_scroll.set, xscrollcommand=game_scroll.set)

        StudentDetails.treeviewgui=my_game

        game_scroll.config(command=my_game.yview)
        game_scroll.config(command=my_game.xview)
        # define our column

        my_game['column'] = ('student_name', 'father_name', 'mother_name', 'deparment', 'shift'
                            ,'group', 'roll', 'session', 'mobile', 'family_phn', 'p_address','status')

        # format our column
        my_game.column("#0", width=100,anchor="center")
        my_game.column("student_name",anchor="center", width=120)
        my_game.column("father_name",anchor="center", width=120)
        my_game.column("mother_name",anchor="center", width=120)
        my_game.column("deparment",anchor="center", width=100)
        my_game.column("shift",anchor="center", width=40)
        my_game.column("group",anchor="center", width=40)
        my_game.column("roll",anchor="center", width=100)
        my_game.column("session",anchor="center", width=80)
        my_game.column("mobile",anchor="center", width=100)
        my_game.column("family_phn",anchor="center", width=100)
        my_game.column("p_address",anchor="center", width=200)
        my_game.column("status",anchor="center", width=60)

        # Create Headings
        my_game.heading("#0", text="IMG--ID")
        my_game.heading("student_name", text="Student Name")
        my_game.heading("father_name", text="Father Name")
        my_game.heading("mother_name", text="Mother Name")
        my_game.heading("deparment", text="Deparment" )
        my_game.heading("shift", text="Shift")
        my_game.heading("group", text="Group")
        my_game.heading("roll", text="Roll")
        my_game.heading("session", text="Session")
        my_game.heading("mobile", text="Mobile")
        my_game.heading("family_phn", text="Family PHN" )
        my_game.heading("p_address", text="P_Address")
        my_game.heading("status", text="Status")

        self.FetchDataFromDatabase()

        my_game.pack()

        return  frame

    def __init__(self):
        self.Connection()
        root = tk.Tk()
        root.title('Sohid Sab Uddin Hostel ___ Student Details')
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
            text='Add New Student', font=("Bahnschrift", 14),
            command=lambda: [root.destroy(), self.NewStudent()]
        ).grid(column=0, row=0, sticky=tk.NW, padx=200, pady=20)


        var = tk.StringVar()
        var.trace("w", lambda name, index, mode, var=var: self.SurchingData(var))
        surching = tk.Entry(root, width=20, font=("Bahnschrift", 15), textvariable=var)
        surching.grid(column=0, row=0, sticky=tk.NW, padx=1080, pady=25)


        StudentDetails.treeviewgui.bind("<Double-1>", self.OnDoubleClick)

        root.mainloop()

    def FetchDataFromDatabase(self):
        c = StudentDetails.db.cursor()
        c.execute("""SELECT*FROM `hostel_managment`.`student_details` ORDER BY `ID` DESC""")

        rows = c.fetchall()
        StudentDetails.allData = rows
        StudentDetails.showdata = StudentDetails.allData

        self.AddDatatoTable(StudentDetails.showdata)

    def OnDoubleClick(self, event):
        MsgBox = tk.messagebox.askquestion('Status Chaning', 'Do You Want to Change Present Status?',
                                           icon='warning')
        if MsgBox == 'yes':
            item = StudentDetails.treeviewgui.selection()[0]
            values=StudentDetails.treeviewgui.item(item, "values")
            id=StudentDetails.treeviewgui.item(item, "text")
            print(id)
            c = StudentDetails.db.cursor()
            if(values[11]=='Running'):
                c = StudentDetails.db.cursor()
                c.execute(
                    """SELECT COUNT(*) FROM `hostel_managment`.`room_distributation` WHERE `status`='Running' AND `student_ID`=%s""",
                    (id,))

                rows = c.fetchall()
                if rows[0][0] == 0:
                    d = StudentDetails.db.cursor()
                    d.execute(
                        """UPDATE `hostel_managment`.`student_details` SET   `status` = 'Passing' WHERE `ID` = %s """,
                        (id,)
                        )
                    StudentDetails.db.commit()
                else:
                    tk.messagebox.showwarning('Sorry',
                                              'Frist Pass This Student From Room',
                                              icon='warning')


            else:
                c.execute("""UPDATE `hostel_managment`.`student_details` SET   `status` = 'Running' WHERE `ID` = %s """,
                          (id,))
                StudentDetails.db.commit()

            self.FetchDataFromDatabase()

    def SurchingData(self,var):
        NewArray=[]
        value=var.get()
        for data in StudentDetails.allData:
            if(value in str(data[7])):
                NewArray.append(data)

        self.AddDatatoTable(NewArray)

    def AddDatatoTable(self,data):
        for row in StudentDetails.treeviewgui.get_children():
            StudentDetails.treeviewgui.delete(row)

        StudentDetails.treeviewgui.imglist = []
        for row in data:
            img = Image.open(io.BytesIO(row[12]))
            img_resized = img.resize((50, 50))
            img = ImageTk.PhotoImage(img_resized)
            StudentDetails.treeviewgui.insert(parent='', index='end', iid=row[0], text=' ' + str(row[0]), image=img,
                           values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]
                                   , row[9], row[10], row[11], row[13]))
            StudentDetails.treeviewgui.imglist.append(img)

    def Mainwindow(self):
            Mainwindow.Mainwindow()

    def NewStudent(self):
            NewStudent.NewStudent()

