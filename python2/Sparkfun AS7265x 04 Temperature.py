from AS7265x import AS7265x
import os
import sys
import time
import serial
import select
from usb2io import usb2io_sendcmd

COM_PORT_ENG                = 'COM17'

#---- Application ---------------------------------------------------------
print "===================================="
print "* Sparkfun AS7265x Sersor example"
print "* GPIO0 - Reset                  "
print "* GPIO2 - Interrupt              "
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


device = AS7265x(ser)

# get master T       
value = device.getTemperature(0)
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "T0 = %d" %value[1]

# get slave 0
value = device.getTemperature(1)
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "T1 = %d" %value[1]

# get slave 1
value = device.getTemperature(2)
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "T2 = %d" %value[1]

