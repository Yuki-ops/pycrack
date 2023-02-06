import tkinter as tk
import threading
import struct
import zlib
import os
from tkinter import filedialog
from tkinter import messagebox


class PNG图片CRC检测:
    def __init__(self):
        root = tk.Toplevel()
        Create_Windows(root)
        root.mainloop()


class Create_Windows:
    def __init__(self, root):
        self.root = root
        self.root.title("图片CRC检测")
        self.root.geometry("400x320+230+230")
        Init_Interface(self.root)

class Init_Interface:
    def __init__(self, root):
        self.root = root
        self.head_img = {"89504E470D0A1A0A":"Png"}
        self.Layout()

    def Layout(self):
        self.data_bin = b""
        self.handler = False
        self.interface = tk.Frame(self.root)
        self.interface.pack()
        
        self.top = tk.Frame(self.interface)
        self.top.pack(anchor="nw")
        upload = tk.Button(self.top, text="选择文件", command=self.Get_Local_File)
        upload.pack(side="left", anchor="nw", pady=10, padx=5)
        self.filedir = tk.Text(self.top, width=40, height=1)
        self.filedir.pack(side="left")

        self.main_output = tk.Frame(self.interface)
        self.main_output.pack(anchor="n")
        describe = tk.Label(self.main_output, text="输出信息<output message>:")
        describe.pack(anchor="nw")
        self.output = tk.Text(self.main_output, width=48, height=15)
        self.output.pack(side="left")
        
        scroll = tk.Scrollbar(self.main_output)
        scroll.config(command=self.output.yview)
        self.output.config(yscrollcommand=scroll.set)
        scroll.pack(side="left", fill=tk.Y)

        self.bottom = tk.Frame(self.interface)
        

        
        
    
    def Get_Local_File(self):
        self.filepath = tk.filedialog.askopenfilename(parent=self.root)   #此处的parent用于当点击上传文件时始将焦距设置为子工具窗口，规避点击上传后根窗口出现在子窗口之上的问题
        if(bool(self.filepath)):
            self.Run_By_Thread(self.Process_The_File, self.filepath)
        else:
            return False


    def Run_By_Thread(self, func, args):
        thread = threading.Thread(target=func, args=(args,))
        thread.start()
        
    def Process_The_File(self, filepath):
        self.output.delete(0.0, "end")
        self.data_bin, data_bin = open(self.filepath, "rb").read(), open(self.filepath, "rb").read()
        head = data_bin[0:8].hex().upper()
        checkresult = self.Check_File_Type(head)
        if(checkresult):
            self.filedir.delete(0.0, "end")
            self.filedir.insert(1.0, self.filepath)
            exec("self.Check_CRC_%s(data_bin)" % checkresult)
        else:
            return False
        
    def Check_CRC_Png(self, data_bin):
        self.output.insert(0.0, "[+]检测图片类型为<Png>\n")
        crc32key = zlib.crc32(data_bin[12:29])
        Truecrc32key = int(data_bin[29:33].hex(),16)
        if(crc32key == Truecrc32key):
            self.output.insert("end", "[+]图片CRC校验码无误\n")
        else:
            self.output.insert("end", "[-]图片CRC校验码错误，检测到图片高宽已被修改\n\n")
            self.output.insert("end", "[*]图片的真实CRC校验码为：%i\n[*]开始爆破图片width、height\n" % Truecrc32key)
            for width in range(4096):
                breakstatus = False
                for height in range(4096):
                    if(zlib.crc32(data_bin[12:16] + struct.pack(">ii", width, height) + data_bin[24:29]) == Truecrc32key):
                        self.output.insert("end", "[+]图片的宽为%i\n[+]图片的高为%i\n\n" % (width, height))
                        self.whdata_bin = struct.pack(">ii", width, height)
                        self.bottom.pack(pady=10)
                        handler_img = tk.Button(self.bottom, text="更改", width=45, height=1, command=self.Handler_Img)
                        handler_img.pack()
                        
                        breakstatus = True
                        break
                        
                if(breakstatus):
                    break
 
                        
    def Handler_Img(self):
        if(os.path.exists("tmp") == False):
            os.mkdir("tmp")
        if(self.handler):
            return True
        filedata = self.data_bin[0:16] + self.whdata_bin + self.data_bin[24:len(self.data_bin)]
        open("./tmp/result.png", "wb").write(filedata)
        self.output.insert("end", "[+]图片修复完成\n[+]图片保存位置:./tmp/result.png\n\n")
        self.handler = True
        
    def Check_File_Type(self, head):
        for filetype in self.head_img:
            if(head == filetype):
                return self.head_img[filetype]
        messagebox.showwarning("Warning!", "加载图片失败，请确认文件类型是否为Png类型<Failed to load picture,please check the file type.>", parent=self.root)
        return False
        




