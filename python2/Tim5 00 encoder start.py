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
# 0 - TI1 mode
# 1 - TI2 mode
# 2 - TI12 mode
mode = 2

#---- Application ---------------------------------------------------------
print "===================================="
print "* Tim5 Encoder start"
print "* pin connection:"
print "* GPIO 12 - lane A"
print "* GPIO 13 - lane B"
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

# Configure gpio
print "gpio config..."
usb2io_sendcmd(ser, "gpio configure 12, 21\r\n")
usb2io_sendcmd(ser, "gpio configure 13, 21\r\n")


print "starting encoder..."                            
#format: tim5 encoder start a
# a = mode
usb2io_sendcmd(ser, "tim5 encoder start " + str(mode) + "\r\n") 

raw_input("Press Enter to exit ...")