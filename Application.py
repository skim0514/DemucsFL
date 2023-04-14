from tkinter import *
from tkinter  import filedialog

class Application(Frame):
    def say_hi(self):
        print("hi there, everyone!")

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})

        self.button = Button(text="Open", command=self.openFile)
        self.button.pack()

        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack({"side": "left"})

    def openFile(self):
        filepath = filedialog.askopenfilename(filetypes=[("Audio Types", ".mp3 .wav")])
        file = open(filepath, 'r')
        print(file.read())
        file.close()

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()



root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()