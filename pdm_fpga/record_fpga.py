# -*- coding: utf-8 -*-
import tkinter as tk
import pdm_fpga as mic

pdmmic= mic.pdm_fpga()


def StartRec():
#    print(fn_flag.get())
    print(Rate.get())
    pdmmic.RecordStartFPGA(fname.get(),fn_flag.get(),lngth.get(),gain.get(),Rate.get())


root = tk.Tk()
root.geometry("400x300")

lb = tk.Label(root, text ="PDM Mic(FPGA) 録音プログラム")
lb.grid(column=1,row=0)

"""出力ファイル名"""
fname_frame = tk.LabelFrame(root,text = "output file name")
fname_frame.grid(column=1,row=1)
fname= tk.StringVar()
fname_entry=tk.Entry( fname_frame,textvariable=fname )
fname.set("snd")
fname_entry.grid(column=1,row=0)

"""ファイル名に時刻を含める？"""
fn_flag = tk.BooleanVar()
ck=tk.Checkbutton(text="H:M:S to filename? ",variable = fn_flag)
ck.grid(column=2,row=1)

"""record length"""
lngth = tk.IntVar()
lngth.set(64)
lngth_frame = tk.LabelFrame(root,text = "Record Length")
lngth_frame.grid(column=1,row=3)

radiol0 = tk.Radiobutton( lngth_frame, text ="  2 sec @16kHz", value = 64, variable = lngth)
radiol1 = tk.Radiobutton( lngth_frame, text ="  8 sec ", value = 256, variable = lngth)
radiol2 = tk.Radiobutton( lngth_frame, text =" 16 sec ", value = 512, variable = lngth)
radiol3 = tk.Radiobutton( lngth_frame, text =" 30 sec ", value = 1024, variable = lngth)
radiol4 = tk.Radiobutton( lngth_frame, text =" 60 sec ", value = 2048, variable = lngth)
radiol5 = tk.Radiobutton( lngth_frame, text ="120 sec ", value = 4096, variable = lngth)

radiol0.grid(column=0,row=0)
radiol1.grid(column=0,row=1)
radiol2.grid(column=0,row=2)
radiol3.grid(column=0,row=3)
radiol4.grid(column=0,row=4)
radiol5.grid(column=0,row=5)

""" Mic Gain"""
gain = tk.IntVar()
gain.set(2)
Gain_frame = tk.LabelFrame(root,text = "Mic Gain")
Gain_frame.grid(column=2,row=3)

radiog0 = tk.Radiobutton( Gain_frame, text =" x  1.0 ", value = 1, variable = gain)
radiog1 = tk.Radiobutton( Gain_frame, text =" x  2.0 ", value = 2, variable = gain)
radiog2 = tk.Radiobutton( Gain_frame, text =" x  4.0 ", value = 4, variable = gain)
radiog3 = tk.Radiobutton( Gain_frame, text =" x  8.0 ", value = 8, variable = gain)
radiog4 = tk.Radiobutton( Gain_frame, text =" x 16.0 ", value = 16, variable = gain)
radiog5 = tk.Radiobutton( Gain_frame, text =" x 32.0 ", value = 32, variable = gain)
radiog6 = tk.Radiobutton( Gain_frame, text =" x 64.0 ", value = 64, variable = gain)

radiog0.grid(column=0,row=0)
radiog1.grid(column=0,row=1)
radiog2.grid(column=0,row=2)
radiog3.grid(column=0,row=3)
radiog4.grid(column=0,row=4)
radiog5.grid(column=0,row=5)
radiog6.grid(column=0,row=6)

""" sample rate """
Rate = tk.IntVar()
Rate.set(0)
Rate_frame = tk.LabelFrame(root,text = "Sample Rate")
Rate_frame.grid(column=3,row=3)

radiog0 = tk.Radiobutton( Rate_frame, text =" 16kHz ", value = 0, variable = Rate)
radiog1 = tk.Radiobutton( Rate_frame, text =" 32kHz ", value = 1, variable = Rate)

radiog0.grid(column=0,row=0)
radiog1.grid(column=0,row=1)

"""record start"""
bt_start = tk.Button(text="録音開始",command=StartRec)
bt_start.grid(column=3,row=1)

root. mainloop()
