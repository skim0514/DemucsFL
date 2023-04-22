from tkinter import *
from tkinter  import filedialog
import SeparateAudio
import torchaudio
import os


class Application(Frame):
    def say_hi(self):
        print("hi there, everyone!")

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})

        self.openFile = Button(text="Separate 1 File", command=self.openFile)
        self.openFile.pack()

        self.openDirectory = Button(text="Separate Directory", command=self.openDirectory)
        self.openDirectory.pack()

        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack({"side": "left"})

    def openFile(self):
        filepath = filedialog.askopenfilename(filetypes=[("Audio Types", ".mp3 .wav")])


        # file = open(filepath, 'rb')

        pathObject = os.path.abspath(filepath)
        print(pathObject)
        head, tail = os.path.split(pathObject)

        print(tail)

        if "mp3" in tail:
            waveform, sample_rate = torchaudio.load(filepath, format="mp3")
        else:
            waveform, sample_rate = torchaudio.load(filepath)

        self.separate(filepath, sample_rate, tail, waveform)

    def separate(self, filepath, sample_rate, tail, waveform):
        separation = SeparateAudio.SeparateAudio(waveform, sample_rate)
        audios = separation.runSeparation()
        print("separation")
        # Vocals Audio
        vocals = audios["vocals"]
        # torchaudio.save(filepath + )
        # Instrumental Audio
        instrumental = audios["other"] + audios["drums"] + audios["bass"]
        dir = os.path.splitext(filepath)[0]
        if not os.path.exists(dir):
            os.mkdir(dir)
        else:
            dir = self.check_file(dir)
            os.mkdir(dir)
        torchaudio.save(os.path.join(dir, "vocals" + tail), vocals, sample_rate)
        torchaudio.save(os.path.join(dir, "instr" + tail), instrumental, sample_rate)

    def check_file(self, filePath):
        if os.path.exists(filePath):
            numb = 1
            while True:
                newPath = "{0}_{2}{1}".format(*os.path.splitext(filePath) + (numb,))
                if os.path.exists(newPath):
                    numb += 1
                else:
                    return newPath
        return filePath

    def openDirectory(self):
        filepath = filedialog.askdirectory()

        for file in os.listdir(filepath):
            filename = os.fsdecode(file)
            print(filename)
            if filename.endswith(".mp3") or filename.endswith(".wav"):
                filefull = os.path.join(filepath, filename)
                if filename.endswith("mp3"):
                    waveform, sample_rate = torchaudio.load(filefull)
                else:
                    waveform, sample_rate = torchaudio.load(filefull)
                self.separate(filefull, sample_rate, filename, waveform)
            else:
                continue


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()



root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()