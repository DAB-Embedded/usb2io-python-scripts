#=====================================================
# FDCAN config
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
print "* FDCAN config"
print "* GPIO 6 - Tx"
print "* GPIO 7 - phy S"
print "* GPIO 8 - phy FLT"
print "* GPIO 9 - Rx"
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

print("Configuring 4 gpio pins...")

usb2io_sendcmd(ser, "gpio configure 7, 1\r\n") # silent mode OFF
usb2io_sendcmd(ser, "gpio configure 8, 0\r\n") # input
usb2io_sendcmd(ser, "gpio configure 9, 9\r\n") # FDCAN1 repeater
usb2io_sendcmd(ser, "gpio configure 6, 9\r\n") # FDCAN1 repeater



print("Configuring fdcan...")
usb2io_sendcmd(ser, "fdcan configure 50000, 0\r\n") #
raw_input("Press Enter to exit ...")
