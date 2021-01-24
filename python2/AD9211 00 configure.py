#=====================================================
#  AD9211 configure
#=====================================================
import os
import sys
import time
import serial
import select
from usb2io import usb2io_sendcmd
from getbuffer import get_buffer
import numpy as np
import matplotlib.pyplot as plt


COM_PORT_ENG                = 'COM17'

#---- Application ---------------------------------------------------------
print "===================================="
print "* AD9211 configure"
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


if (usb2io_sendcmd(ser, "ad9211 configure\r\n") != "OK\r\n"):
	print "failed."
	sys.exit(0)

                                	                        
raw_input("Press Enter to exit ...")