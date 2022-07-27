import tkinter as tk
from tkinter import ttk
import WindowsFiles.Mainwindow as Mainwindow
import MySQLdb as mdb
from datetime import date

class RoomDetails:

    global room_name,member_no,details,status
    global db,mytreeview,alldata,table_data

    def Connection(self):
        try:
            RoomDetails.db = mdb.connect('localhost', 'root', '', 'hostel_managment')

        except mdb.Error as e:
            print('Not Connect')

    def FromSection(self):

        frame = tk.Frame(background='#6DC9F3', highlightbackground='#2C0036',highlightthicknes=3)

        # Find what
        tk.Label(frame, text='Room Name' ,font = ("Bahnschrift", 14)).grid(column=0, row=0, sticky=tk.W,padx=10,pady=20)
        RoomDetails.room_name = tk.Entry(frame, width=30,font = ("Bahnschrift",15))
        RoomDetails.room_name.grid(column=0, row=1,padx=10,pady=2)

        # Replace with:
        tk.Label(frame, text="Member's NO",font = ("Bahnschrift", 14)).grid(column=0, row=2, sticky=tk.W,padx=10,pady=20)
        RoomDetails.member_no = tk.Entry(frame, width=30,font = ("Bahnschrift",15))
        RoomDetails.member_no.grid(column=0, row=3, sticky=tk.W,padx=10,pady=2)

        # Replace with:
        tk.Label(frame, text='Details',font = ("Bahnschrift", 14)).grid(column=0, row=4, sticky=tk.W,padx=10,pady=20)
        RoomDetails.details = tk.Entry(frame, width=30,font = ("Bahnschrift",15))
        RoomDetails.details.grid(column=0, row=5, sticky=tk.W,padx=10,pady=2)

        # Replace with:
        status = ('Running', 'Passing')
        tk.Label(frame, text='Status :',font = ("Bahnschrift", 14)).grid(column=0, row=6, sticky=tk.W,padx=10,pady=20)
        RoomDetails.status = tk.StringVar()
        month_cb = ttk.Combobox(frame, textvariable=RoomDetails.status, width=28, font=("Bahnschrift", 15))
        month_cb['values'] = status
        month_cb['state'] = 'readonly'
        month_cb.grid(column=0, row=7, sticky=tk.W,padx=10,pady=2)

        tk.Button(frame, text='Submit', font = ("Bahnschrift", 14), command=lambda: self.AddData()).grid(column=0, row=8, sticky=tk.SE, padx=10, pady=20)


        return frame

    def TableSection(self):
        frame = tk.Frame(background='#6DC9F3', highlightbackground='#2C0036', highlightthicknes=3)

        # scrollbar
        game_scroll = ttk.Scrollbar(frame)
        game_scroll.pack(side='right', fill='y')

        game_scroll = ttk.Scrollbar(frame, orient='horizontal')
        game_scroll.pack(side='bottom', fill='x')

        RoomDetails.mytreeview=ttk.Treeview(frame,height = 28, yscrollcommand=game_scroll.set, xscrollcommand=game_scroll.set)

        my_game = RoomDetails.mytreeview

        game_scroll.config(command=my_game.yview)
        game_scroll.config(command=my_game.xview)

        # define our column

        my_game['columns'] = ('room_id', 'room_name', 'member_no', 'details', 'status')

        # format our column
        my_game.column("#0", width=0, stretch='NO',anchor="center")
        my_game.column("room_id",  width=40,anchor="center")
        my_game.column("room_name",  width=200,anchor="center")
        my_game.column("member_no",  width=200,anchor="center")
        my_game.column("details", width=200,anchor="center")
        my_game.column("status",  width=200,anchor="center")

        # Create Headings
        my_game.heading("#0", text="")
        my_game.heading("room_id", text="Id")
        my_game.heading("room_name", text="Room Name")
        my_game.heading("member_no", text="Member No")
        my_game.heading("details", text="Details")
        my_game.heading("status", text="Status")

        self.FetchData()

        my_game.pack()
        return  frame

    def FetchData(self):

        c = RoomDetails.db.cursor()
        c.execute("""SELECT*FROM `hostel_managment`.`room_details`""")

        rows = c.fetchall()
        RoomDetails.alldata=rows
        RoomDetails.table_data=RoomDetails.alldata

        self.AddDataToTable(RoomDetails.table_data)

    def AddDataToTable(self,data):
        for row in RoomDetails.mytreeview.get_children():
            RoomDetails.mytreeview.delete(row)

        for row in data:
            RoomDetails.mytreeview.insert(parent='', index='end', iid=row[0], text='',
                           values=(row[0], row[1], row[2], row[3], row[5]))

    def __init__(self):

        self.Connection()

        root = tk.Tk()
        root.title('Sohid Sab Uddin Hostel ___ Room Details')
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
        var.trace("w", lambda name, index, mode, var=var: self.SurchingData(var))
        surching = tk.Entry(root, width=20, font=("Bahnschrift", 15), textvariable=var)
        surching.grid(column=1, row=0,sticky=tk.NE,padx=60, pady=20)

        RoomDetails.mytreeview.bind("<Double-1>", self.OnDoubleClick)

        root.mainloop()

    def SurchingData(self, var):
        NewArray = []
        value=var.get()
        for data in RoomDetails.alldata:
            if (value in str(data[1])):
                NewArray.append(data)
        self.AddDataToTable(NewArray)

    def OnDoubleClick(self, event):
        item = RoomDetails.mytreeview.selection()[0]
        values = RoomDetails.mytreeview.item(item, "values")
        if values[4]=='Running':
            MsgBox = tk.messagebox.askquestion('Status Chaning', 'Do You Want to Change Present Status?',
                                               icon='warning')
            if MsgBox == 'yes':
                c = RoomDetails.db.cursor()
                c.execute("""SELECT COUNT(*) FROM `hostel_managment`.`room_distributation` WHERE `status`='Running' AND `room_ID`=%s""",
                          (item,))

                rows = c.fetchall()
                if rows[0][0]==0:
                    d = RoomDetails.db.cursor()
                    d.execute(
                        """UPDATE `hostel_managment`.`room_details` SET `Status` = 'Passing' WHERE `ID`= %s""",
                        (item,)
                        )
                    RoomDetails.db.commit()
                else:
                    tk.messagebox.showwarning('Sorry',
                                              'Frist Pass All Student From This Room',
                                              icon='warning')
        else:
            MsgBox = tk.messagebox.askquestion('Status Chaning', 'Do You Want to Change Present Status?',
                                               icon='warning')
            if MsgBox == 'yes':
                d = RoomDetails.db.cursor()
                d.execute(
                    """UPDATE `hostel_managment`.`room_details` SET `Status` = 'Running' WHERE `ID`= %s""",
                    (item,)
                )
                RoomDetails.db.commit()

        self.FetchData()

    def AddData(self):
        room_name=RoomDetails.room_name.get()
        member_no=RoomDetails.member_no.get()
        details=RoomDetails.details.get()
        status=RoomDetails.status.get()
        today = date.today()

        if(len(room_name)==0):
            tk.messagebox.showwarning('Sorry',
                                      'Please, Entry Room Name',
                                      icon='warning')
        elif(len(member_no)==0):
            tk.messagebox.showwarning('Sorry',
                                      'Please, Entry Member No',
                                      icon='warning')
        elif(len(details)==0):
            tk.messagebox.showwarning('Sorry',
                                      'Please, Entry Room Details',
                                      icon='warning')
        elif(len(status)==0):
            tk.messagebox.showwarning('Sorry',
                                      'Please, Select Status',
                                      icon='warning')
        else:
            d = RoomDetails.db.cursor()
            d.execute(
                """SELECT COUNT(*) AS find_room FROM `hostel_managment`.`room_details` WHERE `Room_Name`=%s""",
                (room_name,))

            rows = d.fetchall()
            if rows[0][0] == 0:
                c=RoomDetails.db.cursor()
                c.execute("""INSERT INTO `hostel_managment`.`room_details`
                                (`Room_Name`,`Student_No`,`Details`,`Date`,`Status`)
                                VALUES (%s,%s,%s,%s,%s)""",(room_name, member_no, details, today, status,)
                                     )
                RoomDetails.db.commit()
                self.ClearField()
            else:
                tk.messagebox.showwarning('Sorry',
                                          'This Room Name Already Have, Please Add New Name',
                                          icon='warning')
            self.FetchData()

    def ClearField(self):
        RoomDetails.room_name.delete(0, 'end')
        RoomDetails.details.delete(0, 'end')
        RoomDetails.member_no.delete(0, 'end')
        RoomDetails.status.set('')

    def Mainwindow(self):
            Mainwindow()


