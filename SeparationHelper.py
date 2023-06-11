from tkinter import *
from tkinter  import filedialog, messagebox
import SeparateAudio
import torchaudio
import os
from pydub import AudioSegment
import numpy as np
import traceback
import threading


class SeparationHelper:
    def __init__(self):
        self.selection = False
        self.instruments = [False, False, False, False]
        return

    def convert_to_wav(self, input_file, output_file):
        audio = AudioSegment.from_file(input_file)
        audio.export(output_file, format='wav')

    def convert_to_mp3(self, input_file, output_file):
        audio = AudioSegment.from_file(input_file)
        audio.export(output_file, format='mp3')
        
    def separate(self, filepath, sample_rate, tail, waveform):
        separation = SeparateAudio.SeparateAudio(waveform, sample_rate)
        audios = separation.runSeparation()
        print(audios)
        print("separation")
        # Vocals Audio
        vocals = audios["vocals"]
        instrumental = audios["other"] + audios["drums"] + audios["bass"]
        dir = os.path.splitext(filepath)[0]
        if not os.path.exists(dir):
            os.mkdir(dir)
        else:
            dir = self.check_file(dir)
            os.mkdir(dir)

        if not self.selection:
            print("saving")
            try:
                if "mp3" in tail.lower():
                    print("saving mp3 files")
                    # Save vocals and instrumental as WAV files
                    torchaudio.save(os.path.join(dir, "vocals.wav"), vocals, sample_rate)
                    torchaudio.save(os.path.join(dir, "instr.wav"), instrumental, sample_rate)

                    # Convert WAV to MP3 using pydub
                    self.convert_to_mp3(os.path.join(dir, "vocals.wav"), os.path.join(dir, "vocals.mp3"))
                    self.convert_to_mp3(os.path.join(dir, "instr.wav"), os.path.join(dir, "instr.mp3"))

                    # Delete the intermediate WAV files
                    os.remove(os.path.join(dir, "vocals.wav"))
                    os.remove(os.path.join(dir, "instr.wav"))
                    print("mp3 files saved")
                    # messagebox.showinfo("Success", "Separation completed successfully")
                else:    
                    torchaudio.save(os.path.join(dir, "vocals" + tail), vocals, sample_rate)
                    torchaudio.save(os.path.join(dir, "instr" + tail), instrumental, sample_rate)
                    # messagebox.showinfo("Success", "Separation completed successfully")
            except Exception as e:
                traceback.print_exc()

        else:
            if self.instruments[0]:
                if "mp3" in tail.lower():
                    # Save vocals as WAV and convert to MP3
                    torchaudio.save(os.path.join(dir, "vocals.wav"), vocals, sample_rate)
                    self.convert_to_mp3(os.path.join(dir, "vocals.wav"), os.path.join(dir, "vocals.mp3"))
                    os.remove(os.path.join(dir, "vocals.wav"))
                else:
                    # Save vocals as their original format
                    torchaudio.save(os.path.join(dir, "vocals" + tail), vocals, sample_rate)
            if self.instruments[1]:
                if "mp3" in tail.lower():
                    # Save drums as WAV and convert to MP3
                    torchaudio.save(os.path.join(dir, "drums.wav"), vocals, sample_rate)
                    self.convert_to_mp3(os.path.join(dir, "drums.wav"), os.path.join(dir, "drums.mp3"))
                    os.remove(os.path.join(dir, "drums.wav"))
                else:
                    # Save drums as their original format
                    torchaudio.save(os.path.join(dir, "drums" + tail), vocals, sample_rate)
            if self.instruments[2]:
                if "mp3" in tail.lower():
                    # Save bass as WAV and convert to MP3
                    torchaudio.save(os.path.join(dir, "bass.wav"), vocals, sample_rate)
                    self.convert_to_mp3(os.path.join(dir, "bass.wav"), os.path.join(dir, "bass.mp3"))
                    os.remove(os.path.join(dir, "bass.wav"))
                else:
                    # Save bass as their original format
                    torchaudio.save(os.path.join(dir, "bass" + tail), vocals, sample_rate)
            if self.instruments[3]:
                if "mp3" in tail.lower():
                    # Save other as WAV and convert to MP3
                    torchaudio.save(os.path.join(dir, "other.wav"), vocals, sample_rate)
                    self.convert_to_mp3(os.path.join(dir, "other.wav"), os.path.join(dir, "other.mp3"))
                    os.remove(os.path.join(dir, "other.wav"))
                else:
                    # Save other as their original format
                    torchaudio.save(os.path.join(dir, "other" + tail), vocals, sample_rate)
        messagebox.showinfo("Success", "Separation completed successfully")

    def display_error_message(self, message):
        messagebox.showerror("Error", message)

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
    
    def select_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Audio Types", ".mp3 .wav")])


        # file = open(filepath, 'rb')

        pathObject = os.path.abspath(filepath)
        print(pathObject)
        head, tail = os.path.split(pathObject)
        
        info = torchaudio.info(filepath)
        print(info)
        print("================================")
        print(tail)
        try:
            
            if "mp3" in tail:
                # if os.name == 'nt':
                #     print("inside window block")
                #     waveform, sample_rate = self.load_mp3(filepath)
                # else:
                waveform, sample_rate = torchaudio.load(filepath, format="mp3")
            else:
                waveform, sample_rate = torchaudio.load(filepath)

            self.separate(filepath, sample_rate, tail, waveform)
        except Exception as e:
            self.display_error_message(str(e))

    def select_directory(self):
        filepath = filedialog.askdirectory()

        for file in os.listdir(filepath):
            try:
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
            except Exception as e:
                self.display_error_message(str(e))
