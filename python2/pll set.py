#=====================================================
#  Pll config
#  
#
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
print "* PLL config"
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

usb2io_sendcmd(ser, "hello\r\n")

print("Configuring:")
print("0 - 50 Mhz")
print("1 - Si570 output")


usb2io_sendcmd(ser, "gpio configure 1, 6\r\n")
usb2io_sendcmd(ser, "gpio configure 0, 5\r\n")

usb2io_sendcmd(ser, "pll setfreq 10000000\r\n")


raw_input("Press Enter to exit...")