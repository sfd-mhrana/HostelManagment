import tkinter as tk
from tkinter import ttk
from WindowsFiles import Mainwindow
from WindowsFiles.Students import NewStudent
from PIL import Image, ImageTk
import MySQLdb as mdb
import io
from tkinter import messagebox

class RunningStudent():

    global bd,allData,showdata,treeviewgui

    def Connection(self):
        try:
            RunningStudent.db = mdb.connect('localhost', 'root', '', 'hostel_managment')
            #print('Connect')
        except mdb.Error as e:
            print('Not Connect')

    def TableSection(self,root):

        frame = tk.Frame(root, width=1200, height=680, relief="groove", highlightbackground='#2C0036', highlightthicknes=3)

        style = ttk.Style(frame)
        style.configure('Treeview', rowheight=90)

        # scrollbar
        game_scroll = ttk.Scrollbar(frame)
        game_scroll.pack(side='right', fill='y')

        game_scroll = ttk.Scrollbar(frame, orient='horizontal')
        game_scroll.pack(side='bottom', fill='x')

        my_game = ttk.Treeview(frame,height=6, yscrollcommand=game_scroll.set, xscrollcommand=game_scroll.set)

        RunningStudent.treeviewgui=my_game

        game_scroll.config(command=my_game.yview)
        game_scroll.config(command=my_game.xview)
        # define our column

        my_game['column'] = ('room_name', 'student_name','roll', 'mobile','family_phn')

        # format our column
        my_game.column("#0", width=200,anchor="center")
        my_game.column("room_name",anchor="center", width=220)
        my_game.column("student_name",anchor="center", width=220)
        my_game.column("roll",anchor="center", width=220)
        my_game.column("mobile",anchor="center", width=210)
        my_game.column("family_phn",anchor="center", width=210)

        # Create Headings
        my_game.heading("#0", text="IMG--ID")
        my_game.heading("room_name", text="Room Name")
        my_game.heading("student_name", text="Student Name")
        my_game.heading("roll", text="Roll")
        my_game.heading("mobile", text="Student Mobile")
        my_game.heading("family_phn", text="Family Mobile")

        self.FetchDataFromDatabase()

        my_game.pack()

        return  frame

    def __init__(self):
        self.Connection()
        root = tk.Tk()
        root.title('Sohid Sab Uddin Hostel ___ Running Students')
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


        var = tk.StringVar()
        var.trace("w", lambda name, index, mode, var=var: self.SurchingData(var))
        surching = tk.Entry(root, width=20, font=("Bahnschrift", 15), textvariable=var)
        surching.grid(column=0, row=0, sticky=tk.NW, padx=1080, pady=25)

        root.mainloop()

    def FetchDataFromDatabase(self):
        c = RunningStudent.db.cursor()
        c.execute("""SELECT * FROM `running_student` ORDER BY Room_Name ASC""")

        rows = c.fetchall()
        RunningStudent.allData = rows
        RunningStudent.showdata = RunningStudent.allData

        self.AddDatatoTable(RunningStudent.showdata)

    def SurchingData(self,var):
        NewArray=[]
        value=var.get()
        for data in RunningStudent.allData:
            if(value in str(data[5])):
                NewArray.append(data)

        self.AddDatatoTable(NewArray)

    def AddDatatoTable(self,data):
        for row in RunningStudent.treeviewgui.get_children():
            RunningStudent.treeviewgui.delete(row)

        RunningStudent.treeviewgui.imglist = []
        for row in data:
            img = Image.open(io.BytesIO(row[2]))
            img_resized = img.resize((80, 80))
            img = ImageTk.PhotoImage(img_resized)
            RunningStudent.treeviewgui.insert(parent='', index='end', iid=row[1], text=' ' + str(row[0]), image=img,
                           values=(row[7],row[3], row[5], row[4], row[6]))
            RunningStudent.treeviewgui.imglist.append(img)

    def Mainwindow(self):
            Mainwindow.Mainwindow()
