# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 08:51:55 2019

@author: 13539
"""
import sys
import wave
import numpy as np
import matplotlib.pyplot as plt

def wave_plot(filename,unit_size,flag,direction):
    
    delay32k = [[0,4,8,12], #L45
                [0,3,6,9],  #L30
                [0,1,3,4],  #L15
                [0,0,0,0],  #center
                [4,3,1,0],  #R15
                [9,6,3,0],  #R30
                [12,8,4,0]] #R45
    
    delay16k = [[0,2,4,6], #L45
                [0,1,3,4], #L30
                [0,1,1,2], #L15
                [0,0,0,0], #center
                [2,1,1,0], #R15
                [4,3,1,0], #R30
                [6,4,2,0]] #R45
      
    wfname0 = filename + "0.wav"
    wfname1 = filename + "1.wav"
    wfname2 = filename + "2.wav"
    wfname3 = filename + "3.wav"
    wfnames = filename + "synth.wav"
    headerfilename = "data/wave_header32k.bin"

    wf0 = wave.open(wfname0,'r')
    wf1 = wave.open(wfname1,'r')
    wf2 = wave.open(wfname2,'r')
    wf3 = wave.open(wfname3,'r')
    wfs = open(wfnames,'wb')
    fr = open(headerfilename, 'rb')

    framerate = wf0.getframerate()
    frame_num = wf0.getnframes()
    samplewidth= wf0.getsampwidth()

    print(wf0.getparams())

    a = np.fromfile(headerfilename, np.uint8)   #base
    fr.close()

#データ量に応じて編集
    wavedataSize = frame_num * samplewidth


    if framerate == 16000:
        a[24]=0x80
        a[25]=0x3e
        a[26]=0x00
        a[27]=0x00
        freq_flag=1
    elif framerate == 32000:
        a[24]=0x80
        a[25]=0x7d
        a[26]=0x00
        a[27]=0x00
        freq_flag=2
    elif framerate == 8000:
        a[24]=0x40
        a[25]=0x1f
        a[26]=0x00
        a[27]=0x00
        freq_flag=0
    else:
        a[24]=0x00
        a[25]=0x00
        a[26]=0x00
        a[27]=0x00
        freq_flag=0
    

    temp3 = wavedataSize // (256 * 256 * 256)
    a[43]=temp3
    temp2 = (wavedataSize % (256 * 256 * 256))//(256 * 256)
    a[42]=temp2
    temp1 = (wavedataSize % (256 * 256)) // 256
    a[41]=temp1
    temp0 = (wavedataSize % (256))
    a[40] = temp0

    #
    wavedataSize = frame_num * samplewidth +36
    temp3 = wavedataSize // (256 * 256 * 256)
    a[7] = temp3
    temp2 = (wavedataSize % (256 * 256 * 256))//(256 * 256)
    a[6] = temp2
    temp1 = (wavedataSize % (256 * 256)) // 256
    a[5] = temp1
    temp0 = (wavedataSize % (256))
    a[4] = temp0
    wfs.write(a)


#    unit_size = 2048
    unit_num =  frame_num // (unit_size *2)
#    amp = ( 2 ** 8 ) ** samplewidth / 2


    hammingWindow = np.hamming(unit_size);
    fs = framerate #サンプリングレート
    d = 1.0 / fs #サンプリングレートの逆数
    freqList = np.fft.fftfreq(unit_size, d)


#    dtmp=np.zeros(unit_size,dtype='int16')
    d0a=np.zeros(unit_size,dtype='int16')
    d0b=np.zeros(unit_size,dtype='int16')
    d1a=np.zeros(unit_size,dtype='int16')
    d1b=np.zeros(unit_size,dtype='int16')
    d2a=np.zeros(unit_size,dtype='int16')
    d2b=np.zeros(unit_size,dtype='int16')
    d3a=np.zeros(unit_size,dtype='int16')
    d3b=np.zeros(unit_size,dtype='int16')
    data0=np.zeros(unit_size,dtype='int16')
    data1=np.zeros(unit_size,dtype='int16')
    data2=np.zeros(unit_size,dtype='int16')
    data3=np.zeros(unit_size,dtype='int16')
    datas=np.zeros(unit_size,dtype='int16')



    if framerate == 16000:
        delay = delay16k[3+direction]
    elif framerate == 32000:
        delay = delay32k[3+direction]
    else:
        delay = [0,0,0,0]
  

    for i in range(unit_num):    
#        pos = wf.tell()
#        print(pos)
        
        d0a = d0b.copy()
        d1a = d1b.copy()
        d2a = d2b.copy()
        d3a = d3b.copy()
        
        rd_data = wf0.readframes(unit_size)
        d0b = np.frombuffer(rd_data,'int16')
        rd_data = wf1.readframes(unit_size)
        d1b = np.frombuffer(rd_data,'int16')
        rd_data = wf2.readframes(unit_size)
        d2b = np.frombuffer(rd_data,'int16')
        rd_data = wf3.readframes(unit_size)
        d3b = np.frombuffer(rd_data,'int16')

        dly = delay[1]
        if dly==0:
            data0 = d0b.copy()
        else:
            data0[:dly] = d0a[-dly:].copy()
            data0[dly:] = d0b[0:-dly].copy()
            
        dly = delay[0]
        if dly==0:
            data1 = d1b.copy()
        else:
            data1[:dly] = d1a[-dly:].copy()
            data1[dly:] = d1b[0:-dly].copy()
            
        dly = delay[2]
        if dly==0:
            data2 = d2b.copy()
        else:
            data2[:dly] = d2a[-dly:].copy()
            data2[dly:] = d2b[0:-dly].copy()
            
        dly = delay[3]
        if dly==0:
            data3 = d3b.copy()
        else:
            data3[:dly] = d3a[-dly:].copy()
            data3[dly:] = d3b[0:-dly].copy()
            
        datas = data0 + data1 + data2 +data3
        wfs.write(datas)


        if flag==1:        
            x= np.arange(0,unit_size,1)
            plt.axis([0,unit_size-1,-32678,32767])
            plt.plot(x,data0, color='red')
            plt.plot(x,data1, color='green')
            plt.plot(x,data2, color='cyan')
            plt.plot(x,data3, color='magenta')
            plt.plot(x,datas, color='black')
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

            windowedData = datas * hammingWindow
            fftdata = np.fft.fft(windowedData)
            Rfftdata = np.abs(fftdata) # 複素数=>絶対値
            Rfftdatas = Rfftdata/(unit_size/2)
            Rfftdatas[0] = Rfftdatas[0]/2

            max_value = max(Rfftdata0)
            if(max_value < max(Rfftdata1)):
                max_value = max(Rfftdata1)
            if(max_value < max(Rfftdata2)):
                max_value = max(Rfftdata2)
            if(max_value < max(Rfftdata3)):
                max_value = max(Rfftdata3)
            if(max_value < max(Rfftdatas)):
                max_value = max(Rfftdatas)
        
            plt.axis([0,1.0/d/2,0,max_value*1.5])
#        plt.axis([0,1.0/d/2,0,500])
            plt.plot(freqList,Rfftdata0, color='red')
            plt.plot(freqList,Rfftdata1, color='green')
            plt.plot(freqList,Rfftdata2, color='cyan')
            plt.plot(freqList,Rfftdata3, color='magenta')
            plt.plot(freqList,Rfftdatas, color='black')

            plt.title("")
            plt.xlabel("Frequency[Hz]")
            plt.ylabel("amplitude spectrum")
            plt.show()

    wf0.close()
    wf1.close()
    wf2.close()
    wf3.close()
    wfs.close()

def main():
    """引数チェック"""
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

    flag = 0
    if (len(sys.argv)>=4):         #出力ファイル名
        ARG=sys.argv[3]

        if (ARG =='G'): #グラフ描画
            flag = 1    


    direction = 0
    if (len(sys.argv)>=5):         #出力ファイル名
        ARG=sys.argv[4]

        if (ARG =='-3'):
            direction = -3
        elif(ARG =='-2'):
            direction = -2
        elif(ARG =='-1'):
            direction = -1
        elif(ARG =='0'):
            direction = 0
        elif(ARG =='1'):
            direction = 1
        elif(ARG =='2'):
            direction = 2
        elif(ARG =='3'):
            direction = 3
        else:
            direction = 0
    else:
        direction = 0

    wave_plot(wfile,unit_size,flag,direction)

    
if __name__ == "__main__":
    main()