# -*- coding: utf-8 -*- 
import os 
from inspect import getfile
#from psutil import *

def IsSubString(SubStrList,Str): 
    flag=True
    for substr in SubStrList: 
        if not(substr in Str): 
            flag=False
    return flag 

def GetFileList(FindPath,FlagStr=[]): 
    FileList=[]
    try:
        FileNames=os.listdir(FindPath) 
    except:
        return 0
    if (len(FileNames)>0): 
        for fn in FileNames: 
            if (len(FlagStr)>0): 
                #返回指定类型的文件名 
                if (IsSubString(FlagStr,fn)): 
                    FileList.append(fn) 
            else: 
                #默认直接返回所有文件名  
                FileList.append(fn) 
    #对文件名排序 
    if (len(FileList)>0): 
        FileList.sort() 
    return FileList