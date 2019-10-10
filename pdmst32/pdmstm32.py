# -*- coding: utf-8 -*-
import sys
import serial.tools.list_ports
import numpy as np
import pandas as pd
import datetime
import csv
import os
class pdmstm32:

    def __init__(self):
        self.filename="snd"
        self.ser = serial.Serial()
        self.RecordBlock = 0
        self.MicGain = 32

    def ComOpen(self):
        PORTNO = list(serial.tools.list_ports.comports())[0][0]
        '''ここで不都合なポート番号が検出されるときは決めうち '''
#        PORTNO='COM9'
        print(PORTNO, "をopenします")
        self.ser = serial.Serial(port=PORTNO, baudrate=921600)
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

    def ComClose(self):
        self.ser.close()

    def toWaveFile(self):
        fw0 = open(self.filename +"_ch0.wav", 'wb')
        fw1 = open(self.filename +"_ch1.wav", 'wb')
        #read header

        headerfilename = "data/wave_header16k.bin"
        fr = open(headerfilename, 'rb')
        a = np.fromfile(headerfilename, np.uint8)   #base
        fr.close()

        wavedataSize =  self.RecordBlock * 512 * 2  #record block unit = 1kbyte(16bit * 512k)

        temp3 = wavedataSize // (256 * 256 * 256)
        a[43]=temp3
        a[7]=temp3

        temp2 = (wavedataSize % (256 * 256 * 256))//(256 * 256)
        a[42]=temp2
        a[6]=temp2
        temp1 = (wavedataSize % (256 * 256)) // 256
        a[41]=temp1
        a[5]=temp1
        a[40]=0x00
        a[4]=0x2C

        fw0.write(a)
        fw1.write(a)

        RCRDBLK_STR = format(self.RecordBlock,'04x')
        send_command = "(GW"+RCRDBLK_STR+"00)"
        print(send_command)
        send_command=send_command.encode('utf-8')
        self.ser.write(send_command)

        for block in range(self.RecordBlock):
            #    rcvbuf =  ser.read(6)   #header
            #    print(rcvbuf)
            rcvbuf0 =  self.ser.read(1024)
            rcvbuf1 =  self.ser.read(1024)

            fw0.write(rcvbuf0)
            fw1.write(rcvbuf1)
            #   rcvbuf =  ser.read(2)   #footer
            #    print(rcvbuf)
        print((block+1) ,"block recv end")

        fw0.close()
        fw1.close()


    def toWaveFile2ch(self):
        unit_size = 512

        fw = open(self.filename +"_st.wav", 'wb')
        #read header

        headerfilename = "./data/wave_header16k_st.bin"
        fr = open(headerfilename, 'rb')
        a = np.fromfile(headerfilename, np.uint8)   #base
        fr.close()

        wavedataSize =  self.RecordBlock * unit_size * 2 *2 #record block unit = 1kbyte(512 x 2byte * 2ch)

#    framerate == 16000:
        a[24]=0x80
        a[25]=0x3e
        a[26]=0x00
        a[27]=0x00

        temp3 = wavedataSize // (256 * 256 * 256)
        a[43]=temp3
        a[7]=temp3

        temp2 = (wavedataSize % (256 * 256 * 256))//(256 * 256)
        a[42]=temp2
        a[6]=temp2
        temp1 = (wavedataSize % (256 * 256)) // 256
        a[41]=temp1
        a[5]=temp1
        a[40]=0x00
        a[4]=0x2C

        fw.write(a)

        #Gain 設定
        GAIN_STR =  format(self.MicGain,'02x')
        send_command = "(SG" + GAIN_STR + GAIN_STR + "00)"
        print(send_command)
        send_command=send_command.encode('utf-8')
        self.ser.write(send_command)
        rcvbuf =  self.ser.read(10)

        #録音開始
        RCRDBLK_STR = format(self.RecordBlock,'04x')
        send_command = "(GW"+RCRDBLK_STR+"00)"
        print(send_command)
        send_command=send_command.encode('utf-8')
        self.ser.write(send_command)


        for block in range(self.RecordBlock):
            #    rcvbuf =  ser.read(6)   #header
            #    print(rcvbuf)
            rcvbuf =  self.ser.read(unit_size*2 )   # 16bit/sample
            w_ch0 = np.frombuffer(rcvbuf,'int16')
            rcvbuf =  self.ser.read(unit_size*2 )
            w_ch1 = np.frombuffer(rcvbuf,'int16')

            wrbuf = np.empty((2,unit_size),'int16')
            wrbuf[0] = w_ch0
            wrbuf[1] = w_ch1

            wrbuf = wrbuf.T
            wrbuf = wrbuf.flatten()

            fw.write(wrbuf)
            if (block%16 == 0):
                print(block)
            #   rcvbuf =  ser.read(2)   #footer
            #    print(rcvbuf)
        print((block+1) ,"block recv end")

        fw.close()

    def toWaveFile_32k_mono(self):
        fw0 = open(self.filename +"_32k.wav", 'wb')
        #read header

        headerfilename = "data/wave_header32k.bin"
        fr = open(headerfilename, 'rb')
        a = np.fromfile(headerfilename, np.uint8)   #base
        fr.close()

        wavedataSize =  self.RecordBlock * 512  *2 #record block unit = 1kbyte(16bit * 512k)
        temp3 = wavedataSize // (256 * 256 * 256)
        a[43]=temp3
        a[7]=temp3

        temp2 = (wavedataSize % (256 * 256 * 256))//(256 * 256)
        a[42]=temp2
        a[6]=temp2
        temp1 = (wavedataSize % (256 * 256)) // 256
        a[41]=temp1
        a[5]=temp1
        a[40]=0x00
        a[4]=0x2C

        fw0.write(a)

        #Gain 設定
        GAIN_STR =  format(self.MicGain,'02x')
        send_command = "(SG" + GAIN_STR + GAIN_STR + "00)"
        print(send_command)
        send_command=send_command.encode('utf-8')
        self.ser.write(send_command)
        rcvbuf =  self.ser.read(10)


        #録音開始
        RCRDBLK_STR = format(self.RecordBlock,'04x')
        send_command = "(GW"+RCRDBLK_STR+"00)"
        print(send_command)
        send_command=send_command.encode('utf-8')
        self.ser.write(send_command)

        for block in range(self.RecordBlock):
            rcvbuf0 =  self.ser.read(1024)
            fw0.write(rcvbuf0)

        print((block+1) ,"block recv end")
        fw0.close()

    def RecordStart(self,filename,fname_flag,RecordLength):
        #ファイル名の決定
        self.filename=filename
        print(fname_flag)
        print(filename)
        if fname_flag==True:
            time_now = datetime.datetime.now()
            self.filename=filename +"_" + str(time_now.hour) + str(time_now.minute) + str(time_now.second)

        #録音時間
        self.RecordBlock = RecordLength
        self.ComOpen()      #シリアルポートオープン
        self.toWaveFile()   #録音
        self.ComClose()


    def RecordStart2ch(self,filename,fname_flag,RecordLength,Mic_Gain):
        #ファイル名の決定
        self.filename=filename
        print(fname_flag)
        print(filename)
        if fname_flag==True:
            time_now = datetime.datetime.now()
            self.filename=filename +"_" + str(time_now.hour) + str(time_now.minute) + str(time_now.second)

        #録音時間
        self.MicGain = Mic_Gain
        self.RecordBlock = RecordLength
        self.ComOpen()      #シリアルポートオープン
        self.toWaveFile2ch()   #録音
        self.ComClose()

    def RecordStart32k(self,filename,fname_flag,RecordLength,Mic_Gain):
        #ファイル名の決定
        self.filename=filename
        print(fname_flag)
        print(filename)
        if fname_flag==True:
            time_now = datetime.datetime.now()
            self.filename=filename +"_" + str(time_now.hour) + str(time_now.minute) + str(time_now.second)

        #録音時間
        self.MicGain = Mic_Gain
        self.RecordBlock = RecordLength
        self.ComOpen()      #シリアルポートオープン
        self.toWaveFile_32k_mono()   #録音
        self.ComClose()
