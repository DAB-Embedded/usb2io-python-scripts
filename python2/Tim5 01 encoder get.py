#=====================================================
#  Timer5 Encoder
#=====================================================
import os
import sys
import time
import serial
import select
from usb2io import usb2io_sendcmd

COM_PORT_ENG                = 'COM17'

#---- Application ---------------------------------------------------------
print "===================================="
print "* Tim5 Encoder get"
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

print "get encoder state..."                            
#format: tim5 encoder get
usb2io_sendcmd(ser, "tim5 encoder get\r\n") 
time.sleep(1)	
usb2io_sendcmd(ser, "tim5 encoder get\r\n") 
raw_input("Press Enter to exit ...")