#=====================================================
#  LTC2500 config and start
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
print "* LTC2500 gpio config"
print "* pin connection:"
print "* GPIO 0 - MCLK"
print "* GPIO 1 - DRL"
print "* GPIO 2 - RDLA"
print "* GPIO 3 - SDOA"
print "* GPIO 4 - SCKA"
print "* GPIO 5 - SDI"
print "* GPIO 6 - PRE"
print "* GPIO 7 - Trigger"
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

print("Configuring pins to LTC2500...")

if (usb2io_sendcmd(ser, "gpio configure 0, 15\r\n", 1)!= "OK\r\n"):
	print "failed."
	sys.exit(0)

if (usb2io_sendcmd(ser, "gpio configure 1, 15\r\n", 1) != "OK\r\n"):
	print "failed."
	sys.exit(0)

if (usb2io_sendcmd(ser, "gpio configure 2, 15\r\n", 1) != "OK\r\n"):
	print "failed."
	sys.exit(0)

if (usb2io_sendcmd(ser, "gpio configure 3, 15\r\n", 1) != "OK\r\n"):
	print "failed."
	sys.exit(0)

if (usb2io_sendcmd(ser, "gpio configure 4, 15\r\n", 1) != "OK\r\n"):
	print "failed."
	sys.exit(0)

if (usb2io_sendcmd(ser, "gpio configure 5, 15\r\n", 1) != "OK\r\n"):
	print "failed."
	sys.exit(0)

if (usb2io_sendcmd(ser, "gpio configure 6, 15\r\n", 1) != "OK\r\n"):
	print "failed."
	sys.exit(0)

if (usb2io_sendcmd(ser, "gpio configure 7, 15\r\n", 1) != "OK\r\n"):
	print "failed."
	sys.exit(0)

raw_input("Done. Press Enter to exit ...")