'''
本文件主要用于加载libs文件夹下的各个工具
'''
import os
import shutil
import re


def clean_tmp(tmppath = "./tmp/"):
    files = os.listdir(tmppath)
    for rubbish_file in files:
        if(os.path.isdir(tmppath + rubbish_file)):
            try:
                shutil.rmtree(tmppath + rubbish_file)
            except:
                clean_tmp(tmppath + rubbish_file + "/")
        else:
            os.remove(tmppath + rubbish_file)

def include():
    clean_tmp()
    include_code = ""
    
    dirname = "./libs/"
    dirlist = os.listdir(dirname)
    for dir_name in dirlist:
        subdir = dirname + dir_name + "/"
        subdirlist = os.listdir(subdir)
        subdirlist = [subdir.replace(".py","") for subdir in subdirlist]
        if("__pycache__" in subdirlist):
            subdirlist.remove(subdirlist[subdirlist.index("__pycache__")])
            for module_name in subdirlist:
                include_code += "import libs.%s.%s\n" % (dir_name, module_name)
        else:
            for module_name in subdirlist:
                include_code += "import libs.%s.%s\n" % (dir_name, module_name)
            
    return include_code




