#=====================================================
#  FPGA trigger config
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
print "* Trigger config"
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

#format: trigger configure a
# a = 0 - disable
# a = 1 - external connector lane 0
# a = 2 - external connector lane 1
#....
# a = 15 - external connector lane 16
usb2io_sendcmd(ser, "trigger configure 5\r\n") 

raw_input("Press Enter to exit ...")