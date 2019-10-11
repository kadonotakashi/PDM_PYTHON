# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 09:44:17 2019

@author: 13539
"""

import sys
import serial.tools.list_ports
import pandas as pd
import numpy as np

headerfilename = "data/wave_header16k.bin"

"""
引数チェック
"""
if len(sys.argv) >= 2:         #gain
    ARG = sys.argv[1]
    gain = int(ARG)
            #debug中は32-128に制限する
    if gain >7:
        gain = 7
else:
    gain = 4

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
#set Mic Gain
GAIN_STR = format(gain ,'02x')

send_command = "(SG"+GAIN_STR+"0000)"
print(send_command)
send_command=send_command.encode('utf-8')
ser.write(send_command)
rcvbuf =  ser.read(10)

ser.close()
