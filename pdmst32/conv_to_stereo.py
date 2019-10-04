# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12

@author: 13539

2 monoral trac => stereo


"""
import sys
import wave
import numpy as np
import matplotlib.pyplot as plt

def wave_plot(filename,flag):
    wfname0 = filename + "_ch0.wav"
    wfname1 = filename + "_ch1.wav"
    wfnameST = filename + "_st.wav"
    headerfilename = "data/wave_header16k_st.bin"

    wf0 = wave.open(wfname0,'r')
    wf1 = wave.open(wfname1,'r')
    wfst = open(wfnameST,'wb')

    fr = open(headerfilename, 'rb')
    framerate = wf0.getframerate()
    frame_num = wf0.getnframes()
    samplewidth= wf0.getsampwidth()

#    print(wf0.getparams())

    a = np.fromfile(headerfilename, np.uint8)   #base
    fr.close()

#データ量に応じて編集
#    wavedataSize = frame_num * samplewidth
    wavedataSize = frame_num * samplewidth * 2 #stereo

#    framerate == 16000:
    a[24]=0x80
    a[25]=0x3e
    a[26]=0x00
    a[27]=0x00

    temp3 = wavedataSize // (256 * 256 * 256)
    a[43]=temp3
    temp2 = (wavedataSize % (256 * 256 * 256))//(256 * 256)
    a[42]=temp2
    temp1 = (wavedataSize % (256 * 256)) // 256
    a[41]=temp1
    temp0 = (wavedataSize % (256))
    a[40] = temp0

    #
    wavedataSize = frame_num * samplewidth * 2 +36
    temp3 = wavedataSize // (256 * 256 * 256)
    a[7] = temp3
    temp2 = (wavedataSize % (256 * 256 * 256))//(256 * 256)
    a[6] = temp2
    temp1 = (wavedataSize % (256 * 256)) // 256
    a[5] = temp1
    temp0 = (wavedataSize % (256))
    a[4] = temp0
    wfst.write(a)

    unit_size=512;
    unit_num =  frame_num // (unit_size)
#    amp = ( 2 ** 8 ) ** samplewidth / 2


    hammingWindow = np.hamming(unit_size)
    fs = framerate #サンプリングレート
    d = 1.0 / fs #サンプリングレートの逆数
    freqList = np.fft.fftfreq(unit_size, d)




    for i in range(unit_num):
        rd_data = wf0.readframes(unit_size)
        w_ch0 = np.frombuffer(rd_data,'int16')
        rd_data = wf1.readframes(unit_size)
        w_ch1 = np.frombuffer(rd_data,'int16')

#        print(type(w_ch0))

        w_st = np.empty((2,unit_size),'int16')
        w_st[0] = w_ch0
        w_st[1] = w_ch1
#        print(w_st)
        w_st = w_st.T
#        print(w_st)

        w_stx = w_st.flatten()
#        print(w_stx)

#        for j in range (unit_num):
#            w_st=np.append(w_st,w_ch0[j])
#            w_st=np.append(w_st,w_ch1[j])

        wfst.write(w_stx)
#        wfst.write(w_ch0)
#        wfst.write(w_ch1)

        if flag==1:
            x= np.arange(0,unit_size,1)
            plt.axis([0,unit_size-1,-32678,32767])
            plt.plot(x,w_ch0, color='red')
            plt.plot(x,w_ch1, color='green')
            plt_title ="unit" + str(i)
            plt.title(plt_title)
            plt.xlabel("time[s]")
            plt.ylabel("normalized power")
            plt.show()

            windowedData = w_ch0 * hammingWindow
            fftdata = np.fft.fft(windowedData)
            Rfftdata = np.abs(fftdata) # 複素数=>絶対値
            Rfftdata0 = Rfftdata/(unit_size/2)
            Rfftdata0[0] = Rfftdata0[0]/2

            windowedData = w_ch1 * hammingWindow
            fftdata = np.fft.fft(windowedData)
            Rfftdata = np.abs(fftdata) # 複素数=>絶対値
            Rfftdata1 = Rfftdata/(unit_size/2)
            Rfftdata1[0] = Rfftdata1[0]/2

            max_value = max(Rfftdata0)
            if(max_value < max(Rfftdata1)):
                max_value = max(Rfftdata1)

            plt.axis([0,1.0/d/2,0,max_value*1.5])
#        plt.axis([0,1.0/d/2,0,500])
            plt.plot(freqList,Rfftdata0, color='red')
            plt.plot(freqList,Rfftdata1, color='green')

            plt.title("")
            plt.xlabel("Frequency[Hz]")
            plt.ylabel("amplitude spectrum")
            plt.show()

    wfst.close()
    wf0.close()
    wf1.close()

def main():
    """引数チェック"""
    if (len(sys.argv)>=2):         #入力ファイル名
        wavfile=sys.argv[1]
        wfile=wavfile.split(".")
        wfile=wfile[0]
    else:
        wfile = "test"

    flag = 0
    if (len(sys.argv)>=3):         #G指定でグラフ表示
        ARG=sys.argv[2]

        if (ARG =='G'): #グラフ描画
            flag = 1
        else:
            flag = 0


    wave_plot(wfile,flag)


if __name__ == "__main__":
    main()