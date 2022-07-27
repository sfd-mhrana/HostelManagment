import tkinter as tk
from tkinter import messagebox
from WindowsFiles.Students import StudentDetails
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import MySQLdb as mdb
from datetime import date

class NewStudent:
    global imglabel ,db
    global student_name,father_name,mother_name,department,shift,group,session,mbl,p_mbl,address,rool,img,img_name,status,root

    def Connection(self):
        try:
            NewStudent.db = mdb.connect('localhost', 'root', '', 'hostel_managment')

        except mdb.Error as e:
            print('Not Connect')

    def StudentFrom(self,root):
        frame = tk.Frame(background='#6DC9F3', highlightbackground='#2C0036', highlightthicknes=3)

        # Find what
        tk.Label(frame, text='Student Name',bg='#6DC9F3', font=("Bahnschrift", 14)).grid(column=0, row=0, sticky=tk.W, padx=43, pady=10)
        NewStudent.student_name = tk.Entry(frame, width=30, font=("Bahnschrift", 15))
        NewStudent.student_name.grid(column=0, row=1, padx=43, pady=10)

        tk.Label(frame, text='Father Name',bg='#6DC9F3', font=("Bahnschrift", 14)).grid(column=1, row=0, sticky=tk.W, padx=43, pady=10)
        NewStudent.father_name = tk.Entry(frame, width=30, font=("Bahnschrift", 15))
        NewStudent.father_name.grid(column=1, row=1, padx=43, pady=10)

        tk.Label(frame, text='Mother Name',bg='#6DC9F3', font=("Bahnschrift", 14)).grid(column=2, row=0, sticky=tk.W, padx=43, pady=10)
        NewStudent.mother_name = tk.Entry(frame, width=30, font=("Bahnschrift", 15))
        NewStudent.mother_name.grid(column=2, row=1, padx=43, pady=10)

        department = ('CMT', 'AIDT', 'PT', 'CT', 'ET', 'MT')
        NewStudent.department = tk.StringVar()
        tk.Label(frame, text='Department',bg='#6DC9F3', font=("Bahnschrift", 14)).grid(column=0, row=2, sticky=tk.W, padx=43,pady=10)
        month_cb = ttk.Combobox(frame, textvariable=NewStudent.department,width=28, font=("Bahnschrift", 15))
        month_cb['values'] = department
        month_cb['state'] = 'readonly'
        month_cb.grid(column=0, row=3, padx=43, pady=10)


        tk.Label(frame, text='Shift',bg='#6DC9F3', font=("Bahnschrift", 14)).grid(column=1, row=2, sticky=tk.W, padx=43,pady=10)
        NewStudent.shift =tk.StringVar()
        shifta = tk.Radiobutton(frame, bg='#6DC9F3',text="1'st", variable=NewStudent.shift, value="1")
        shifta.select()
        shifta.grid(column=1, row=3, padx=43, pady=10, sticky=tk.W)
        shiftb = tk.Radiobutton(frame,bg='#6DC9F3', text="2'nd", variable=NewStudent.shift,value="2")
        shiftb.grid(column=1, row=3, padx=43, pady=10, sticky=tk.NS)


        tk.Label(frame, text='Group',bg='#6DC9F3', font=("Bahnschrift", 14)).grid(column=2, row=2, sticky=tk.W, padx=43, pady=10)
        NewStudent.group = tk.StringVar()
        groupa = tk.Radiobutton(frame, bg='#6DC9F3', text="A", variable=NewStudent.group, value="A")
        groupa.select()
        groupa.grid(column=2, row=3, padx=43, pady=10, sticky=tk.W)
        groupb = tk.Radiobutton(frame, bg='#6DC9F3', text="B", variable=NewStudent.group, value="B")
        groupb.grid(column=2, row=3, padx=43, pady=10, sticky=tk.NS)

        now = date.today().year
        sessingItem=[]
        for x in range(now-9 ,now+1):
            sessingItem.append(str(x) +'-'+str(x+1)[-2:])

        NewStudent.session = tk.StringVar()
        tk.Label(frame, text='Session', bg='#6DC9F3', font=("Bahnschrift", 14)).grid(column=0, row=4, sticky=tk.W, padx=43,pady=10)
        sessiongui = ttk.Combobox(frame, textvariable=NewStudent.session, width=28, font=("Bahnschrift", 15))
        sessiongui['values'] = sessingItem
        sessiongui['state'] = 'readonly'
        sessiongui.grid(column=0, row=5, padx=43, pady=10)

        tk.Label(frame, text='Mobile', bg='#6DC9F3',font=("Bahnschrift", 14)).grid(column=1, row=4, sticky=tk.W, padx=43,pady=10)
        NewStudent.mbl = tk.Entry(frame, width=30, font=("Bahnschrift", 15))
        NewStudent.mbl.grid(column=1, row=5, padx=43, pady=10)

        tk.Label(frame, text='Family Phone',bg='#6DC9F3', font=("Bahnschrift", 14)).grid(column=2, row=4, sticky=tk.W, padx=43,pady=10)
        NewStudent.p_mbl = tk.Entry(frame, width=30, font=("Bahnschrift", 15))
        NewStudent.p_mbl.grid(column=2, row=5, padx=43, pady=10)


        tk.Label(frame, text='Address', bg='#6DC9F3', font=("Bahnschrift", 14)).grid(column=0, row=6, sticky=tk.W, padx=43, pady=10)
        NewStudent.address = tk.Entry(frame, width=30, font=("Bahnschrift", 15))
        NewStudent.address.grid(column=0, row=7, padx=43, pady=10)

        tk.Label(frame, text='Roll', bg='#6DC9F3', font=("Bahnschrift", 14)).grid(column=1, row=6, sticky=tk.W,padx=43, pady=10)
        NewStudent.rool = tk.Entry(frame, width=30, font=("Bahnschrift", 15))
        NewStudent.rool.grid(column=1, row=7, padx=43, pady=10)

        status = ['Running', 'Passing']
        NewStudent.status = tk.StringVar()
        tk.Label(frame, text='Status', bg='#6DC9F3', font=("Bahnschrift", 14)).grid(column=2, row=6, sticky=tk.W,
                                                                                        padx=43, pady=10)
        statusgui = ttk.Combobox(frame, textvariable=NewStudent.status, width=28, font=("Bahnschrift", 15))
        statusgui['values'] = status
        statusgui['state'] = 'readonly'
        statusgui.grid(column=2, row=7, padx=43, pady=10)

        tk.Button(frame, text='Choose..', font=("Bahnschrift", 14), command=lambda: self.upload_file(root)).grid(column=0, row=10,
                                                                                                       sticky=tk.NW,
                                                                                                       padx=40, pady=50)
        NewStudent.imglabel=tk.Label(frame,bg='#6DC9F3')
        NewStudent.imglabel.grid(column=0, row=10,
                                                                                                       sticky=tk.SE,
                                                                                                       padx=40, pady=50)
        tk.Button(frame, text='Submit', font=("Bahnschrift", 14), command=lambda: self.AddData()).grid(column=2, row=10,
                                                                                                       sticky=tk.SE,
                                                                                                       padx=40, pady=50)

        return frame

    def __init__(self):
        self.Connection()
        root = tk.Tk()
        root.title('Sohid Sab Uddin Hostel ___ New Student')
        root.attributes('-fullscreen', True)
        root.configure(bg='#6DC9F3')
        root.iconphoto(False, tk.PhotoImage(file='../asset/icon.png'))

        NewStudent.root=root
        # layout on the root window
        root.columnconfigure(0)

        input_frame = self.StudentFrom(root)
        input_frame.grid(column=0, row=0, sticky=tk.NW, padx=40, pady=80)
        tk.Button(
            root,
            text='Student Details', font=("Bahnschrift", 14),
            command=lambda: [root.destroy(), self.StudetnDetails()]
        ).grid(column=0, row=0, sticky=tk.NW, padx=40, pady=20)

        NewStudent.img_name=None
        root.mainloop()

    def StudetnDetails(self):
        StudentDetails.StudentDetails()

    def upload_file(self,root):
        f_types = [('Jpg Files', '*.jpg')]
        NewStudent.img_name = filedialog.askopenfilename(filetypes=f_types)
        NewStudent.img = Image.open(NewStudent.img_name)
        img_resized = NewStudent.img.resize((100, 100))  # new width & height
        NewStudent.img = ImageTk.PhotoImage(img_resized)
        NewStudent.imglabel.config(image=NewStudent.img)

    def AddData(self):
        student_name=NewStudent.student_name.get()
        father_name=NewStudent.father_name.get()
        mother_name=NewStudent.mother_name.get()
        department=NewStudent.department.get()
        shift=NewStudent.shift.get()
        group=NewStudent.group.get()
        session=NewStudent.session.get()
        mbl=NewStudent.mbl.get()
        p_mbl=NewStudent.p_mbl.get()
        address=NewStudent.address.get()
        rool=NewStudent.rool.get()
        status=NewStudent.status.get()

        if len(student_name)==0:
            tk.messagebox.showwarning('Sorry',
                                      'Please, Entry Student Name',
                                      icon='warning')
        elif len(father_name)==0:
            tk.messagebox.showwarning('Sorry',
                                      'Please, Entry Father Name',
                                      icon='warning')
        elif len(mother_name)==0:
            tk.messagebox.showwarning('Sorry',
                                      'Please, Entry Mother Name',
                                      icon='warning')
        elif len(department)==0:
            tk.messagebox.showwarning('Sorry',
                                      'Please, Select Department',
                                      icon='warning')
        elif len(session)==0:
            tk.messagebox.showwarning('Sorry',
                                      'Please, Select Session',
                                      icon='warning')
        elif len(mbl)==0:
            tk.messagebox.showwarning('Sorry',
                                      'Please, Entry Student Mobile',
                                      icon='warning')
        elif len(p_mbl)==0:
            tk.messagebox.showwarning('Sorry',
                                      'Please, Entry Family Mobile',
                                      icon='warning')
        elif len(address)==0:
            tk.messagebox.showwarning('Sorry',
                                      'Please, Entry Home Address',
                                      icon='warning')
        elif len(rool)==0:
            tk.messagebox.showwarning('Sorry',
                                      'Please, Entry Roll No',
                                      icon='warning')
        elif len(status)==0:
            tk.messagebox.showwarning('Sorry',
                                      'Please, Select Status',
                                      icon='warning')
        elif NewStudent.img_name is None:
            tk.messagebox.showwarning('Sorry',
                                      'Please, Select a Image',
                                      icon='warning')
        else:
            binary_file = self.convertToBinaryData(NewStudent.img_name)
            today = date.today()

            d = NewStudent.db.cursor()
            d.execute(
                """SELECT COUNT(*) `rows` FROM `hostel_managment`.`student_details` WHERE  `roll`=%s""",
                (rool,))

            rows = d.fetchall()
            if rows[0][0] == 0:
                c = NewStudent.db.cursor()
                a=c.execute("""INSERT INTO `hostel_managment`.`student_details`
                (`student_name`,`father_name`,`mother_name`,`deparment`,`shift`,`group`,`roll`,`sessition`,`mobile`,`family_PHN`,`address`,`IMG`,`status`,`date`)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                          (student_name,father_name,mother_name,department,shift,group,rool,session,mbl,p_mbl,address,binary_file,status,today)
                )

                if(a):
                    NewStudent.db.commit()
                    messagebox.showinfo('Success', 'Data Added')
                    NewStudent.root.destroy()
                    StudentDetails.StudentDetails()
                else:
                    pass
            else:
                tk.messagebox.showwarning('Sorry',
                                          'This Roll Already Add. Please Check',
                                          icon='warning')

    def convertToBinaryData(self,filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData

