#=====================================================
# Step motor controller start
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
print "* Step motor controller start"
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


print("Starting step motor cntroller...")

# start channel 1
#if usb2io_sendcmd(ser, "stepmotor start 1\r\n") != "OK\r\n":
#	print "failed."
#	sys.exit(0)

# start channel 2
#if usb2io_sendcmd(ser, "stepmotor start 2\r\n") != "OK\r\n":
#	print "failed."
#	sys.exit(0)

# start all channels 
if usb2io_sendcmd(ser, "stepmotor start 0\r\n") != "OK\r\n":
	print "failed."
	sys.exit(0)


raw_input("Press Enter to exit...")