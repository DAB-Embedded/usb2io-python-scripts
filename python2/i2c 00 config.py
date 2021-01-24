#=====================================================
#  I2C functional test
#=====================================================
import os
import sys
import time
import serial
import select
from usb2io import usb2io_sendcmd

COM_PORT_ENG                = 'COM17'
# port select. 1 - stnm32, 2 - fpga
port = 2

#baudrate. 0 - 100 KHz, 1 - 400 KHz, 2 - 1 MHz
baudrate = 0

#---- Application ---------------------------------------------------------
print "===================================="
print "* I2C configure"
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

if (port == 2):
	# configure pins
	usb2io_sendcmd(ser, "gpio configure 14, 20\r\n")
	usb2io_sendcmd(ser, "gpio configure 15, 20\r\n")
	usb2io_sendcmd(ser, "expv write 3300\r\n")
print "Configure I2C"
usb2io_sendcmd(ser, "i2c configure " + str(port) + ", " + str(baudrate) + "\r\n")

# Close serial port
ser.close()
raw_input("Press Enter to exit ...")

