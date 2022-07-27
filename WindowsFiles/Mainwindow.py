import tkinter as tk
import WindowsFiles.RoomDetails as RoomDetails
import WindowsFiles.Students.StudentDetails as StudentDetails
import WindowsFiles.RoomDistributation as RoomDistributation
import WindowsFiles.RunningStudents  as RunningStudents
import WindowsFiles.Accounts.Accounts  as Accounts
from WindowsFiles.MealSheet.MeelSheet import MeelSheetDetails
import MySQLdb as mdb

class Mainwindow():
    global db

    def Connection(self):
        try:
            Mainwindow.db = mdb.connect('Localhost', 'root', '', 'hostel_managment')
            c=Mainwindow.db.cursor()
            c.execute("""SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''))""")
            Mainwindow.db.commit()
        except mdb.Error as e:
            print(e)

    def __init__(self):
        self.Connection()
        root = tk.Tk()
        root.title('Sohid Sab Uddin Hostel')
        #root.resizable(False, False)
        root.attributes('-fullscreen', True)
        root.configure(bg='#6DC9F3')
        root.iconphoto(False, tk.PhotoImage(file='../asset/icon.png'))

        tk.Button(
            root,
            text='Room Details', width=20, height=2, font = ("Bahnschrift", 14),
            command=lambda:[root.destroy(),self.RoomDetails()]
        ).place(x=250, y=180)

        tk.Button(
            root,
            text='Room Distributation', width=20, height=2, font=("Bahnschrift", 14),
            command=lambda:  [root.destroy(),self.RoomDistributation()]
        ).place(x=550, y=180)

        tk.Button(
            root,
            text='Student Details', width=20, height=2, font=("Bahnschrift", 14),
            command=lambda: [root.destroy(),self.StudentDetails()]
        ).place(x=850, y=180)

        tk.Button(
            root,
            text='MeetSheet', width=20, height=2, font=("Bahnschrift", 14),
            command=lambda: [root.destroy(),self.MeelSheet()]
        ).place(x=400, y=320)

        tk.Button(
            root,
            text='Accounts', width=20, height=2, font=("Bahnschrift", 14),
            command=lambda:[root.destroy(),self.Accounts()]
        ).place(x=720, y=320)

        tk.Button(
            root,
            text='See Running Student', width=20, height=2, font=("Bahnschrift", 14),
            command=lambda: [root.destroy(), self.RunningStudent()]
        ).place(x=560, y=450)
        root.mainloop()

    def RoomDetails(self):
        RoomDetails.RoomDetails()

    def StudentDetails(self):
        StudentDetails.StudentDetails()

    def RoomDistributation(self):
        RoomDistributation.RoomDistributation()

    def MeelSheet(self):
        MeelSheetDetails()

    def Accounts(self):
        Accounts.AccDetails()

    def RunningStudent(self):
        RunningStudents.RunningStudent()

if __name__=="__main__":
        Mainwindow()