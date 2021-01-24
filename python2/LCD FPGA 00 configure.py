#=====================================================
#  LCD functional test
#  
#
#=====================================================
import os
import sys
import time
import serial
import select
import struct
import zlib
import binascii
from usb2io import usb2io_sendcmd

COM_PORT_ENG                = 'COM17'

print "===================================="
print "* LCD  configure"
print "===================================="

local_com_port = sys.argv[1] if (len(sys.argv) > 1) else COM_PORT_ENG

def writeCommand(ser, cmd):
	strx = "ssd1322 write command " + str(cmd & 0xFF) + "\r\n"
	wro = ser.write(strx)
	time.sleep(0.02)
	rrd = ser.readline()

def writeData(ser, data):
	strx = "ssd1322 write data " + str(data & 0xFF) + "\r\n"
	wro = ser.write(strx)
	time.sleep(0.02)
	rrd = ser.readline()

# Open serial port
print "Open serial port " + local_com_port
try:
    ser = serial.Serial(local_com_port, 115200, timeout=3)
    print "COM port OK" 
except:
    print "Error COM port" 
    sys.exit(0)


print "Configure EXT voltage to 3.3V"
usb2io_sendcmd(ser, "expv write 3300\r\n")

print "Configure PIN"
usb2io_sendcmd(ser, "gpio configure 0, 22\r\n", 1)
usb2io_sendcmd(ser, "gpio configure 1, 22\r\n", 1)
usb2io_sendcmd(ser, "gpio configure 2, 22\r\n", 1)
usb2io_sendcmd(ser, "gpio configure 3, 22\r\n", 1)
usb2io_sendcmd(ser, "gpio configure 4, 22\r\n", 1)
usb2io_sendcmd(ser, "gpio configure 5, 22\r\n", 1)
usb2io_sendcmd(ser, "gpio configure 6, 22\r\n", 1)
usb2io_sendcmd(ser, "gpio configure 7, 22\r\n", 1)
usb2io_sendcmd(ser, "gpio configure 8, 22\r\n", 1)
usb2io_sendcmd(ser, "gpio configure 9, 22\r\n", 1)
usb2io_sendcmd(ser, "gpio configure 10, 22\r\n", 1)
usb2io_sendcmd(ser, "gpio configure 11, 22\r\n", 1)

# reset lcd          
print "Reset"                                  
usb2io_sendcmd(ser, "gpio configure 12, 1\r\n", 1)
time.sleep(0.1)
usb2io_sendcmd(ser, "gpio configure 12, 2\r\n", 1)
time.sleep(0.1)

print "Done"
raw_input("Press Enter to exit ...")
