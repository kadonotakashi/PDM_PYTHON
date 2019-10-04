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
    wf = wave.open(filename,'r')
    channels = wf.getnchannels()
    framerate = wf.getframerate()
    frame_num = wf.getnframes()
    print("channels  = ",channels)
    print("framerate = ",framerate)
    print(wf.getparams())

#    unit_size = 2048
    unit_num =  frame_num // (unit_size *2)
    amp = ( 2 ** 8 ) ** wf.getsampwidth() / 2


    hammingWindow = np.hamming(unit_size);
    fs = framerate #サンプリングレート
    d = 1.0 / fs #サンプリングレートの逆数
    freqList = np.fft.fftfreq(unit_size, d)

    for i in range(unit_num):    
#        pos = wf.tell()
#        print(pos)
        data = wf.readframes(unit_size)
        data = np.frombuffer(data,'int16')
    
        x= np.arange(0,unit_size,1)
        plt.axis([0,unit_size-1,-32678,32767])
        plt.plot(x,data)
        plt_title ="unit" + str(i) 
        plt.title(plt_title)
        plt.xlabel("time[s]")
        plt.ylabel("normalized power")
        plt.show()

        
        windowedData = data * hammingWindow
        fftdata = np.fft.fft(windowedData)
        Rfftdata = np.abs(fftdata) # 複素数=>絶対値
        Rfftdata = Rfftdata/(unit_size/2)
        Rfftdata[0] = Rfftdata[0]/2
        
        plt.axis([0,1.0/d/2,0,max(Rfftdata)*1.5])
        plt.plot(freqList,Rfftdata)

        plt.title("")
        plt.xlabel("Frequency[Hz]")
        plt.ylabel("amplitude spectrum")
        plt.show()


def main():
    if (len(sys.argv)>=2):         #出力ファイル名
        InputFileName=sys.argv[1]
    else:
        InputFileName = "test.wav"

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
        unit_size=1024
                    
    wave_plot(InputFileName,unit_size)

    
if __name__ == "__main__":
    main()