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
AddCommand(buffer, 0xae) #/* set display off */
AddCommand(buffer, 0x00) #/* set lower column start address */
AddCommand(buffer, 0x10) #/* set higher column start address */
AddCommand(buffer, 0x40) #/* set display start line */
AddCommand(buffer, 0x2E) #
AddCommand(buffer, 0x81) #/* set contrast control */
AddCommand(buffer, 0x32) #
AddCommand(buffer, 0x82) #
AddCommand(buffer, 0x80) #
AddCommand(buffer, 0xa1) #/* set segment remap */
AddCommand(buffer, 0xa6) #/* set normal display */
AddCommand(buffer, 0xa8) #/* set multiplex ratio */
AddCommand(buffer, 0x3f) #/* 1/64 */
AddCommand(buffer, 0xad) #/* master configuration */
AddCommand(buffer, 0x8e) #/* external vcc supply */
AddCommand(buffer, 0xc8) #/* set com scan direction */
AddCommand(buffer, 0xd3) #/* set display offset */
AddCommand(buffer, 0x40) #
AddCommand(buffer, 0xd5) #/* set display clock divide/oscillator frequency */
AddCommand(buffer, 0xf0) #
AddCommand(buffer, 0xD8) #/*set area color mode off */
AddCommand(buffer, 0x05) #
AddCommand(buffer, 0xD9) #
AddCommand(buffer, 0xF1) #
AddCommand(buffer, 0xda) #/* set com pin configuartion */
AddCommand(buffer, 0x12) #
AddCommand(buffer, 0x91) #
AddCommand(buffer, 0x3F) #
AddCommand(buffer, 0x3F) #
AddCommand(buffer, 0x3F) #
AddCommand(buffer, 0x3F) #
AddCommand(buffer, 0xaf) # /* set display on */ 

# send buffer to uC SDRAM
if (put_buffer(ser, buffer) == 0):
	sys.exit(0)

usb2io_sendcmd(ser, "lcd fpga buffer write " + str(len(buffer) / 2) + "\r\n")

ser.close()
print "Done"
raw_input("Press Enter to exit ...")

