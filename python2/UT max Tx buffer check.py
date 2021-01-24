#=====================================================
#  Tx buffer check
#  
#
#=====================================================
import os
import sys
import time
import serial
import select
from putbuffer import put_buffer
import math
from usb2io import usb2io_sendcmd

COM_PORT_ENG                = 'COM17'

#---- Application ---------------------------------------------------------
print "===================================="
print "* Tx buffer check"
print "===================================="

local_com_port = sys.argv[1] if (len(sys.argv) > 1) else COM_PORT_ENG

# Open serial port
print "Open serial port " + local_com_port
try:
    ser = serial.Serial(local_com_port, 115200, timeout=10, writeTimeout = 10)
    print "COM port OK" 
except:
    print "Error COM port" 
    sys.exit(0)

bufSize = 64 * 1024 * 1024

while (bufSize > 1):
	data = bytearray(bufSize)
	print("Try " + str(bufSize))
	
	try:
		ser.write(data)
	except:
		print("        Failed")
		bufSize >>= 1;
		continue
	print("Success.")
	break;

print("Max buffer size = " + str(bufSize))
raw_input("Press Enter to exit ...")