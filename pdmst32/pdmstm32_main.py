# -*- coding: utf-8 -*-
import tkinter as tk
import pdmstm32 as mic

pdmmic= mic.pdmstm32()


def StartRec():
    print(fn_flag.get())
    pdmmic.RecordStart(fname.get(),fn_flag.get(),lngth.get())


root = tk.Tk()
root.geometry("400x200")

lb = tk.Label(root, text ="PDM Mic 録音プログラム")
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
lngth_frame.grid(column=1,row=2)

radiol0 = tk.Radiobutton( lngth_frame, text ="  2 sec ", value = 64, variable = lngth)
radiol1 = tk.Radiobutton( lngth_frame, text ="  8 sec ", value = 256, variable = lngth)
radiol2 = tk.Radiobutton( lngth_frame, text =" 16 sec ", value = 512, variable = lngth)

radiol0.grid(column=0,row=0)
radiol1.grid(column=0,row=1)
radiol2.grid(column=0,row=2)

"""record start"""
bt_start = tk.Button(text="録音開始",command=StartRec)
bt_start.grid(column=2,row=2)

root. mainloop()
