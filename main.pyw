import tkinter as tk
from tkinter import messagebox
import os
import sys
import __init__



#创建窗口
class Create_Windows:
    def __init__(self, root):
        self.root = root
        self.root.title("CTF工具集合")
        self.root.geometry("600x600+200+200")
        Init_Interface(self.root)       #初始化窗口的页面



#初始化所有工具的调用按钮
class Init_Interface:
    def __init__(self,root):
        self.root = root
        self.init_interface = tk.Frame(self.root)
        self.init_interface.grid(sticky="S", pady=10, padx=10)
        self.libsdir = "./libs/"
        self.classification = os.listdir(self.libsdir)
        self.tools_name = {}
        self.Layout(self.classification)
        
        
    def Layout(self, tools_list):
        self.Create_Windows()
        for tool_name,tool_column in zip(tools_list, range(0, len(tools_list)*2, 2)):
            exec(tool_name + "=tk.Button(self.init_interface, text=\"" + tool_name + "\", bg=\"skyblue\", command=self.Sub_Windows_" + tool_name + ")")
            exec(tool_name + ".grid(row=0, column=" + str(tool_column) + ", columnspan=2)")
            exec(tool_name + ".config(width=10)")

    def Create_Windows(self):
        for sub_classification in self.classification:
            code = """def Sub_Windows_%s(self):\n    self.init_interface.destroy()\n    Child_Tool(self.root, sys._getframe().f_code.co_name)\nsetattr(Init_Interface,"Sub_Windows_%s", Sub_Windows_%s)""" % (sub_classification, sub_classification, sub_classification)
            exec(code)

    def Create_Child_Tools(self, tool_name):
        self.init_interface.destroy()
        Child_Tool(self.root, sys._getframe().f_code.co_name)
        

        

class Child_Tool:
    def __init__(self, root, funcname):
        self.root = root
        self.steg = tk.Frame(self.root)
        self.steg.pack(side="left", anchor="nw")
        self.libsdir = "./libs/"
        self.funcname = funcname
        self.Get_Tools_Name()
        
        
    def Get_Tools_Name(self):
        btn_back = tk.Button(self.steg, text="返回", command=self.Go_Back, bg="skyblue")
        btn_back.pack(anchor="nw", pady=10, padx=10)
        btn_back.config(width=10)
        
        dirname = self.funcname.split("_")[len(self.funcname.split("_")) - 1]
        sub_tools = os.listdir(self.libsdir + "%s/"%dirname)

        sub_tools.remove("__pycache__")
        sub_tools = [tool.replace(".py", "") for tool in sub_tools]
        for sub_tool in sub_tools:
            exec(sub_tool + "=tk.Button(self.steg, text=\"" + sub_tool + "\", command=libs." + dirname + "." + sub_tool + "." + sub_tool + ")")
            exec(sub_tool + ".pack(padx=5, pady=5)")
            exec(sub_tool + ".config(width=\"30\")")

    def Go_Back(self):
        self.steg.destroy()
        Init_Interface(self.root)


#用于加载libs中的工具的类
class Include_Libs:
    def __init__(self):
        self.Include()

    def Include(self):
        try:
            exec(__init__.include(), globals())
        except:
            Error("10000", "工具脚本加载失败,请按照规范编写工具脚本<Tools script import fail, Please write the tool script according to the specification>")
            exit(1)



#此类用于错误处理
class Error:
    def __init__(self, error_type, message):
        if(error_type == "10000"):
            self.Script_Include_Error(message)
            
    
    def Script_Include_Error(self, message):
        messagebox.showerror("Error!", message)
        exit(1)
            
                

if __name__ == "__main__":
    Include_Libs()
    root = tk.Tk()
    Create_Windows(root)
    root.mainloop()         #循环挂起窗口
