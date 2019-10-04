# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 08:51:55 2019

@author: 13539
"""
import sys
import wave
import numpy as np
import matplotlib.pyplot as plt

def wave_plot(filename,unit_size):
    wfname0 = filename + "0.wav"
    wfname1 = filename + "1.wav"
    wfname2 = filename + "2.wav"
    wfname3 = filename + "3.wav"

    wf0 = wave.open(wfname0,'r')
    wf1 = wave.open(wfname1,'r')
    wf2 = wave.open(wfname2,'r')
    wf3 = wave.open(wfname3,'r')

    channels = wf0.getnchannels()
    framerate = wf0.getframerate()
    frame_num = wf0.getnframes()
#    samplewidth= wf0.getsampwidth()
    print("channels  = ",channels)
    print("framerate = ",framerate)
    print(wf0.getparams())

#    unit_size = 2048
    unit_num =  frame_num // (unit_size *2)
#    amp = ( 2 ** 8 ) ** samplewidth / 2


    hammingWindow = np.hamming(unit_size)
    fs = framerate #サンプリングレート
    d = 1.0 / fs #サンプリングレートの逆数
    freqList = np.fft.fftfreq(unit_size, d)

    for i in range(unit_num):
#        pos = wf.tell()
#        print(pos)
        data0 = wf0.readframes(unit_size)
        data0 = np.frombuffer(data0,'int16')

        data1 = wf1.readframes(unit_size)
        data1 = np.frombuffer(data1,'int16')

        data2 = wf2.readframes(unit_size)
        data2 = np.frombuffer(data2,'int16')

        data3 = wf3.readframes(unit_size)
        data3 = np.frombuffer(data3,'int16')

        x= np.arange(0,unit_size,1)
        plt.axis([0,unit_size-1,-32678,32767])
        plt.plot(x,data0, color='red')
        plt.plot(x,data1, color='green')
        plt.plot(x,data2, color='cyan')
        plt.plot(x,data3, color='magenta')
        plt_title ="unit" + str(i) 
        plt.title(plt_title)
        plt.xlabel("time[s]")
        plt.ylabel("normalized power")
        plt.show()

        windowedData = data0 * hammingWindow
        fftdata = np.fft.fft(windowedData)
        Rfftdata = np.abs(fftdata) # 複素数=>絶対値
        Rfftdata0 = Rfftdata/(unit_size/2)
        Rfftdata0[0] = Rfftdata0[0]/2

        windowedData = data1 * hammingWindow
        fftdata = np.fft.fft(windowedData)
        Rfftdata = np.abs(fftdata) # 複素数=>絶対値
        Rfftdata1 = Rfftdata/(unit_size/2)
        Rfftdata1[0] = Rfftdata1[0]/2

        windowedData = data2 * hammingWindow
        fftdata = np.fft.fft(windowedData)
        Rfftdata = np.abs(fftdata) # 複素数=>絶対値
        Rfftdata2 = Rfftdata/(unit_size/2)
        Rfftdata2[0] = Rfftdata2[0]/2

        windowedData = data3 * hammingWindow
        fftdata = np.fft.fft(windowedData)
        Rfftdata = np.abs(fftdata) # 複素数=>絶対値
        Rfftdata3 = Rfftdata/(unit_size/2)
        Rfftdata3[0] = Rfftdata3[0]/2

        max_value = max(Rfftdata0)
        if(max_value < max(Rfftdata1)):
            max_value < max(Rfftdata1)
        if(max_value < max(Rfftdata2)):
            max_value < max(Rfftdata2)
        if(max_value < max(Rfftdata3)):
            max_value < max(Rfftdata3)

        plt.axis([0,1.0/d/2,0,max_value*1.5])
#        plt.axis([0,1.0/d/2,0,500])
        plt.plot(freqList,Rfftdata0, color='red')
        plt.plot(freqList,Rfftdata1, color='green')
        plt.plot(freqList,Rfftdata2, color='cyan')
        plt.plot(freqList,Rfftdata3, color='magenta')

        plt.title("")
        plt.xlabel("Frequency[Hz]")
        plt.ylabel("amplitude spectrum")
        plt.show()


def main():
    if (len(sys.argv)>=2):         #出力ファイル名
        wavfile=sys.argv[1]
        wfile=wavfile.split(".")
        wfile=wfile[0]
    else:
        wfile = "test"

    if (len(sys.argv)>=3):         #出力ファイル名
        ARG=sys.argv[2]

        if (ARG =='0'):
            unit_size=1024
        elif(ARG =='1'):
            unit_size=2048
        elif(ARG =='2'):
            unit_size=4096
        elif(ARG =='3'):
            unit_size=8192
        elif(ARG =='4'):
            unit_size=16384
        else:
            unit_size=4096
    else:
        unit_size=4096

    wave_plot(wfile,unit_size)

if __name__ == "__main__":
    main()