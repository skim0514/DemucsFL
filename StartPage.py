from tkinter import *
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import SeparateAudio
import torchaudio
import os
import SeparationHelper
import SeparateAudio

LARGEFONT = ("Verdana", 35)
helper = SeparationHelper.SeparationHelper()

class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)



        # initializing frames to an empty array

        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Page1, Page2):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # label of frame Layout 2
        label = ttk.Label(self, text="Start Page", font=LARGEFONT)

        # putting the grid in its place by using
        # grid
        label.grid(row=0, column=1, padx=10, pady=10)

        button1 = ttk.Button(self, text="Separate Vocals and Instrumentals",
                             command=lambda: controller.show_frame(Page1))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

        ## button to show frame 2 with text layout2
        button2 = ttk.Button(self, text="Choose Instruments then Separate",
                             command=lambda: controller.show_frame(Page2))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)


class Page1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Separate to Instrumental + Vocals", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Back to Start Page",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place
        # by using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

        openFile = Button(self, text="Separate 1 File", command=helper.openFile)
        openFile.grid(row=2, column=1, padx=10, pady=10)
        openDirectory = Button(self, text="Separate Directory", command=helper.openDirectory)
        openDirectory.grid(row=3, column=1, padx=10, pady=10)


class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page 2", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 3 with text
        # layout3
        button2 = ttk.Button(self, text="Back to Start Page",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)

        self.var1 = tk.IntVar()
        self.var2 = tk.IntVar()
        self.var3 = tk.IntVar()
        self.var4 = tk.IntVar()
        c1 = tk.Checkbutton(self, text='Vocals', variable=self.var1, onvalue=1, offvalue=0)
        c1.grid(row=3, column=1, padx=10, pady=10)
        c2 = tk.Checkbutton(self, text='Drums', variable=self.var2, onvalue=1, offvalue=0)
        c2.grid(row=4, column=1, padx=10, pady=10)
        c3 = tk.Checkbutton(self, text='Bass', variable=self.var3, onvalue=1, offvalue=0)
        c3.grid(row=5, column=1, padx=10, pady=10)
        c4 = tk.Checkbutton(self, text='Other', variable=self.var4, onvalue=1, offvalue=0)
        c4.grid(row=6, column=1, padx=10, pady=10)

        openFile = Button(self, text="Separate 1 File", command=self.openFileSelection)
        openFile.grid(row=7, column=1, padx=10, pady=10)
        openDirectory = Button(self, text="Separate Directory", command=self.openDirectorySelection)
        openDirectory.grid(row=8, column=1, padx=10, pady=10)


    def openFileSelection(self):
        helper.selection = True
        if self.checkInstruments() == -1:
            return
        helper.openFile()

    def openDirectorySelection(self):
        helper.selection = True
        if self.checkInstruments() == -1:
            return
        helper.openDirectory()

    def checkInstruments(self):
        if not (self.var1.get() or self.var2.get() or self.var3.get() or self.var4.get()):
            messagebox.showerror("Error", "Select at least 1 instrument")
            return -1
        print(self.var1.get(), self.var2.get(), self.var3.get(), self.var4.get())
        if self.var1.get() == 1:
            helper.instruments[0] = True
        if self.var2.get() == 1:
            helper.instruments[1] = True
        if self.var3.get() == 1:
            helper.instruments[2] = True
        if self.var4.get() == 1:
            helper.instruments[3] = True



# Driver Code
app = tkinterApp()
app.mainloop()