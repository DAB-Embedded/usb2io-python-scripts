#=====================================================
#  DCMI camera fpga test
#=====================================================
import os
import sys
import time
import serial
import select
import struct
from usb2io import usb2io_sendcmd

COM_PORT_ENG                = 'COM17'

#---- Application ---------------------------------------------------------
print "===================================="
print "* DCMI camera fpga test *"
print "===================================="

local_com_port = sys.argv[1] if (len(sys.argv) > 1) else COM_PORT_ENG

# Open serial port7
print "Open serial port " + local_com_port
try:
    ser = serial.Serial(local_com_port, 115200, timeout=3)
    print "COM port OK" 
except:
    print "Error COM port" 
    sys.exit(0)

usb2io_sendcmd(ser, "fpga camera start 1\r\n")# Close serial port
ser.close()
raw_input("Press Enter to exit ...")

