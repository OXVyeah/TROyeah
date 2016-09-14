

import wmi 


def network(): 
    c = wmi.WMI ()     
    for interface in c.Win32_NetworkAdapterConfiguration (IPEnabled=1): 
        mac = interface.MACAddress 
    return mac

print network()