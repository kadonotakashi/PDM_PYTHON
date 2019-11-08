# -*- coding: utf-8 -*-
import sys
import serial.tools.list_ports
import numpy as np
import pandas as pd
import datetime
import csv
import os
class pdm_fpga:

    def __init__(self):
        self.filename="snd"
        self.ser = serial.Serial()
        self.RecordBlock = 0
        self.MicGain = 32
        self.SampleRate = 0

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


    def toWaveFileFPGA(self):
        fw0 = open(self.filename +"_ch0.wav", 'wb')
        fw1 = open(self.filename +"_ch1.wav", 'wb')
        fw2 = open(self.filename +"_ch2.wav", 'wb')
        fw3 = open(self.filename +"_ch3.wav", 'wb')

        #read header
        if self.SampleRate==0: #16kHz
            print("16k")
            headerfilename = "data/wave_header16k.bin"
            fr = open(headerfilename, 'rb')
            a = np.fromfile(headerfilename, np.uint8)   #base
            fr.close()

            wavedataSize =  self.RecordBlock * 512 * 4  #record block unit = 1kbyte(16bit * 512k)
            #set sample rate to 16kHz
            send_command = "(SF010000)"

        else:   #32kHz
            print("32k")
            headerfilename = "data/wave_header32k.bin"
            fr = open(headerfilename, 'rb')
            a = np.fromfile(headerfilename, np.uint8)   #base
            fr.close()
            wavedataSize =  self.RecordBlock * 512 * 4  #record block unit = 1kbyte(16bit * 512k)
            #set sample rate to 32kHz
            send_command = "(SF000000)"

        print(send_command)
        send_command=send_command.encode('utf-8')
        self.ser.write(send_command)
        rcvbuf =  self.ser.read(10)
        rcvbuf.decode('utf-8')
        print(rcvbuf)

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
        fw2.write(a)
        fw3.write(a)

        #Gain 設定
        GAIN_STR =  format(self.MicGain,'02x')
        send_command = "(SG" + GAIN_STR + "0000)"
        print(send_command)
        send_command=send_command.encode('utf-8')
        self.ser.write(send_command)
        rcvbuf =  self.ser.read(10)
        rcvbuf.decode('utf-8')
        print(rcvbuf)

        #set record length to FPGA
        RCRDBLK_STR = format(self.RecordBlock,'04x')
        send_command = "(GW"+RCRDBLK_STR+"00)"
        print(send_command)
        send_command=send_command.encode('utf-8')
        self.ser.write(send_command)
#        rcvbuf =  self.ser.read(10)
#        rcvbuf.decode('utf-8')
#        print(rcvbuf)

        for block in range(self.RecordBlock):
            #    rcvbuf =  ser.read(6)   #header
            #    print(rcvbuf)
            rcvbuf0 =  self.ser.read(4096)
            rcvbuf1 =  self.ser.read(4096)
            rcvbuf2 =  self.ser.read(4096)
            rcvbuf3 =  self.ser.read(4096)

            fw0.write(rcvbuf0)
            fw1.write(rcvbuf1)
            fw2.write(rcvbuf2)
            fw3.write(rcvbuf3)
            #   rcvbuf =  ser.read(2)   #footer
            #    print(rcvbuf)
        print((block+1) ,"block recv end")

        fw0.close()
        fw1.close()
        fw2.close()
        fw3.close()

    def RecordStartFPGA(self,filename,fname_flag,RecordLength,Mic_Gain,SampleRate):
        #ファイル名の決定
        self.filename=filename
        print(fname_flag)
        print(filename)
        if fname_flag==True:
            time_now = datetime.datetime.now()
            self.filename=filename +"_" + str(time_now.hour) + str(time_now.minute) + str(time_now.second)

        #録音時間
        self.SampleRate = SampleRate
        self.MicGain = Mic_Gain
        self.RecordBlock = RecordLength
        print(self.SampleRate)

        self.ComOpen()      #シリアルポートオープン
        self.toWaveFileFPGA()   #録音
        self.ComClose()
