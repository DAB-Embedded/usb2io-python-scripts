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
from putbuffer import put_buffer

COM_PORT_ENG                = 'COM17'
image_width = 2
image_heigh = 8

def AddCommand(buffer, cmd):
	buffer.append(cmd)
	buffer.append(0x00) #command code
def AddData(buffer, cmd):
	buffer.append(cmd)
	buffer.append(0x01) #data code

print "===================================="
print "* LCD  send buffer"
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

buffer = bytearray()
pixdata = 0x01

for y in range(0, 8):
    AddCommand(buffer, 0xb0 + y) 
    AddCommand(buffer, 0x00)
    AddCommand(buffer, 0x10)
    for x in range(0, 128):
        AddData(buffer, pixdata)
    pixdata <<= 1
    pixdata |= 1

# send buffer to uC SDRAM
if (put_buffer(ser, buffer) == 0):
	sys.exit(0)

usb2io_sendcmd(ser, "lcd fpga buffer write " + str(len(buffer) / 2) + "\r\n")

ser.close()
print "Done"
raw_input("Press Enter to exit ...")

