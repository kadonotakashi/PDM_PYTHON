# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 09:44:17 2019

@author: 13539
"""

import sys
import serial.tools.list_ports
import pandas as pd
import numpy as np

headerfilename = "data/wave_header32k.bin"

"""
引数チェック
"""
if len(sys.argv) >= 3:         #採取ブロック数
    ARG = sys.argv[2]
    record_block = int(ARG)
            #debug中は32-128に制限する
    if record_block >512:
        record_block = 512
else:
    record_block = 4


if (len(sys.argv)>=2):         #出力ファイル名
    OutputFileName=sys.argv[1]
else:
    OutputFileName = "datafile"

print("output file name     : ", OutputFileName)
print("num of record block  : ", record_block)


"""
ファイルを開いてheaderを書いておく
"""
fw0 = open(OutputFileName +"0.wav", 'wb')
fw1 = open(OutputFileName +"1.wav", 'wb')
fw2 = open(OutputFileName +"2.wav", 'wb')
fw3 = open(OutputFileName +"3.wav", 'wb')
fr = open(headerfilename, 'rb')

a = np.fromfile(headerfilename, np.uint8)   #base
fr.close()

#データ量に応じて編集
wavedataSize = record_block * 4096 *2

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
a[4]=0x22

fw0.write(a)
fw1.write(a)
fw2.write(a)
fw3.write(a)

"""
シリアルポートオープン
"""
PORTNO = list(serial.tools.list_ports.comports())[0][0]
'''ここで不都合なポート番号が検出されるときは決めうち '''
#PORTNO='COM9'
#PORTNO='COM15'
print(PORTNO, "を検出しました")
ser = serial.Serial(port=PORTNO, baudrate=921600)
#FTDIのデバイスでパラレル接続しているのでbaudrateの設定は、通信速度に関係しない

ser.reset_input_buffer()
ser.reset_output_buffer()

"""
コマンド送出
"""
#１６ｋHz Sample
send_command = "(SF000000)"
print(send_command)
send_command=send_command.encode('utf-8')
ser.write(send_command)

rcvbuf =  ser.read(10)
print(rcvbuf)

#録音コマンド
RCRDBLK_STR = format(record_block,'04x')
#print(RCRDBLK_STR)
send_command = "(GW"+RCRDBLK_STR+"00)"
print(send_command)
send_command=send_command.encode('utf-8')
ser.write(send_command)

for block in range(record_block):

#    rcvbuf =  ser.read(6)   #header
#    print(rcvbuf)


#    print(rcvbuf)
    rcvbuf0 =  ser.read(4096)
    rcvbuf1 =  ser.read(4096)
    rcvbuf2 =  ser.read(4096)
    rcvbuf3 =  ser.read(4096)

    fw0.write(rcvbuf0)
    fw1.write(rcvbuf1)
    fw2.write(rcvbuf2)
    fw3.write(rcvbuf3)
#   rcvbuf =  ser.read(2)   #footer
#    print(rcvbuf)
print(block ,"recv end")
ser.close()
fw0.close()
fw1.close()
fw2.close()
fw3.close()


