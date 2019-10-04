# -*- coding: utf-8 -*- 
import tkinter as tk 
class Application( tk. Frame): 
    def __init__( self, master = None): 
        super().__init__( master) 
        master.title(" テキスト ボックス 内容 の 取得") 
        master.geometry("350x150") 
        self.pack() 
        self. create_ widgets() # 部品 の 作成/ 設定 
    
    def create_widgets(self): 
        self.lb = tk.Label(self) 
        self.lb["text"] = "ラベル" 
        self.lb.pack( side ="top") 
        self.en = tk.Entry(self) 
        self.en.pack() 
        self.en.focus_set() 
        self.bt = tk.Button(self) # この よう にも 書ける 
        #self.bt = tk.Button( text ="ボタン", command = self.print_ txtval) 
        self.bt["text"] = "ボタン" 
        self.bt["command"] = self.print_txtval 
        self.bt.pack( side ="bottom")

def print_ txtval(self): 
    val_en = self.en. get() 
    print(val_en) 


root = tk.Tk() 
app = Application( master = root) 
app.mainloop()

辛島信芳. Pythonをおぼえた人がGUIアプリケーション開発をするためのtkinter速習入門: 標準ライブラリでGUI作成 (Kindle の位置No.115-117). Kindle 版. 