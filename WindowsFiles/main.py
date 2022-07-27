from tkinter import *
from time import sleep
import Mainwindow

class PlassScreen:
    def __init__(self):

        self.root=Tk()
        self.root.config(bg="black")
        self.root.title('Sohid Sab Uddin Hostel')
        self.root.attributes('-fullscreen', True)


        Label(self.root,text="Loading....", font="Bahnschrift 15"
              ,bg="black",fg="#FFBD09").place(x=490,y=320)


        for i in range(20):
            Label(self.root,bg="#1F2732",width=2,height=1).place(x=(i+22)*22,y=350)



        self.root.update()
        self.play_animation()

        self.root.mainloop()


    def play_animation(self):
            for i in range(20):
                for j in range(20):
                    Label(self.root,bg="#FFBD09",width=2,height=1).place(x=(j+22)*22,y=350)
                    sleep(0.01)
                    self.root.update_idletasks()
                    Label(self.root, bg="#1F2732", width=2, height=1).place(x=(j + 22) * 22, y=350)
            else:
                Mainwindow.Mainwindow()
                exit(0)


if __name__=="__main__":
    PlassScreen()