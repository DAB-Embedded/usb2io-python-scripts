#=====================================================
#  Step motor disable
#  
#
#=====================================================
import os
import sys
import time
import serial
import select
from configDRV8711 import disableDRV8711

COM_PORT_ENG                = 'COM17'

#---- Application ---------------------------------------------------------
print "===================================="
print "* Step motor disable"
print "===================================="

local_com_port = sys.argv[1] if (len(sys.argv) > 1) else COM_PORT_ENG

# Open serial port
print "Open serial port " + local_com_port
try:
    ser = serial.Serial(local_com_port, 115200, timeout=3)
    print "COM port OK" 
except:
    print "Error COM port" 
    sys.exit(0)



disableDRV8711(ser)                             
raw_input("Press Enter to exit...")