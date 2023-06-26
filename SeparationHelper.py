from tkinter import filedialog
import SeparateAudio
import torchaudio
import os
import math

import numpy
import pywt
from scipy import signal



class SeparationHelper:
    def __init__(self):
        self.selection = False
        self.instruments = [False, False, False, False]
        return


    def openFile(self):
        filepath = filedialog.askopenfilename(filetypes=[("Audio Types", ".mp3 .wav")])

        pathObject = os.path.abspath(filepath)
        print(pathObject)
        head, tail = os.path.split(pathObject)

        print(tail)

        if "mp3" in tail:
            waveform, sample_rate = torchaudio.load(filepath, format="mp3")
        else:
            waveform, sample_rate = torchaudio.load(filepath)

        self.detect_bpm(sample_rate, waveform)

        self.separate(filepath, sample_rate, tail, waveform)

    def detect_bpm(self, sample_rate, waveform):
        n = 0
        window = 5
        samps = waveform.numpy()
        samps = samps[0] + samps[1]
        samps.reshape(-1, )
        fs = sample_rate
        nsamps = samps.shape[0]
        window_samps = int(window * fs)
        samps_ndx = 0  # First sample in window_ndx
        max_window_ndx = math.floor(nsamps / window_samps)
        bpms = numpy.zeros(max_window_ndx)
        # Iterate through all windows
        print("detecting bpm")
        print(max_window_ndx)
        for window_ndx in range(0, max_window_ndx):

            # Get a new set of samples
            # print(n,":",len(bpms),":",max_window_ndx_int,":",fs,":",nsamps,":",samps_ndx)
            data = samps[samps_ndx: samps_ndx + window_samps]
            if not ((len(data) % window_samps) == 0):
                print("error")
                raise AssertionError(str(len(data)))

            bpm, correl_temp = bpmDetector(data, fs)
            if bpm is None:
                print("None")
                continue
            bpms[window_ndx] = bpm
            correl = correl_temp

            # Iterate at the end of the loop
            samps_ndx = samps_ndx + window_samps

            # Counter for debug...
            n = n + 1

            bpm = numpy.median(bpms)
            print("Completed!  Estimated Beats Per Minute:", bpm)

    def separate(self, filepath, sample_rate, tail, waveform):
        separation = SeparateAudio.SeparateAudio(waveform, sample_rate)
        audios = separation.runSeparation()
        print("separation")
        # Vocals Audio
        print(audios.keys())
        vocals = audios['vocals']
        # torchaudio.save(filepath + )
        # Instrumental Audio
        instrumental = audios['other'] + audios['drums'] + audios['bass']
        dir = os.path.splitext(filepath)[0]
        if not os.path.exists(dir):
            os.mkdir(dir)
        else:
            dir = self.check_file(dir)
            os.mkdir(dir)

        if not self.selection:
            torchaudio.save(os.path.join(dir, "vocals" + tail), vocals, sample_rate)
            torchaudio.save(os.path.join(dir, "instr" + tail), instrumental, sample_rate)
        else:
            if self.instruments[0]:
                torchaudio.save(os.path.join(dir, "vocals" + tail), vocals, sample_rate)
            if self.instruments[1]:
                torchaudio.save(os.path.join(dir, "drums" + tail), vocals, sample_rate)
            if self.instruments[2]:
                torchaudio.save(os.path.join(dir, "bass" + tail), vocals, sample_rate)
            if self.instruments[3]:
                torchaudio.save(os.path.join(dir, "other" + tail), vocals, sample_rate)

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


def bpmDetector(data, fs):
    cA = []
    cD = []
    correl = []
    cD_sum = []
    levels = 4
    max_decimation = 2 ** (levels - 1)
    min_ndx = math.floor(60.0 / 220 * (fs / max_decimation))
    max_ndx = math.floor(60.0 / 40 * (fs / max_decimation))

    for loop in range(0, levels):
        cD = []
        # 1) DWT
        if loop == 0:
            [cA, cD] = pywt.dwt(data, "db4")
            cD_minlen = len(cD) / max_decimation + 1
            cD_sum = numpy.zeros(math.floor(cD_minlen))
        else:
            [cA, cD] = pywt.dwt(cA, "db4")

        # 2) Filter
        cD = signal.lfilter([0.01], [1 - 0.99], cD)

        # 4) Subtract out the mean.

        # 5) Decimate for reconstruction later.
        cD = abs(cD[:: (2 ** (levels - loop - 1))])
        cD = cD - numpy.mean(cD)

        # 6) Recombine the signal before ACF
        #    Essentially, each level the detail coefs (i.e. the HPF values) are concatenated to the beginning of the array
        cD_sum = cD[0: math.floor(cD_minlen)] + cD_sum

    if [b for b in cA if b != 0.0] == []:
        return no_audio_data()

    # Adding in the approximate data as well...
    cA = signal.lfilter([0.01], [1 - 0.99], cA)
    cA = abs(cA)
    cA = cA - numpy.mean(cA)
    cD_sum = cA[0: math.floor(cD_minlen)] + cD_sum

    # ACF
    correl = numpy.correlate(cD_sum, cD_sum, "full")

    midpoint = math.floor(len(correl) / 2)
    correl_midpoint_tmp = correl[midpoint:]
    peak_ndx = peak_detect(correl_midpoint_tmp[min_ndx:max_ndx])
    if len(peak_ndx) > 1:
        return no_audio_data()

    peak_ndx_adjusted = peak_ndx[0] + min_ndx
    bpm = 60.0 / peak_ndx_adjusted * (fs / max_decimation)
    print(bpm)
    return bpm, correl

def no_audio_data():
    print("No audio data for sample, skipping...")
    return None, None


# simple peak detection
def peak_detect(data):
    max_val = numpy.amax(abs(data))
    peak_ndx = numpy.where(data == max_val)
    if len(peak_ndx[0]) == 0:  # if nothing found then the max must be negative
        peak_ndx = numpy.where(data == -max_val)
    return peak_ndx




