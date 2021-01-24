#=====================================================
#  I2S functional test
#  
#
#=====================================================
import os
import sys
import time
import serial
import select
from putbuffer import put_buffer
import math
from usb2io import usb2io_sendcmd

COM_PORT_ENG                = 'COM17'
data_cnt = 30 * 22000 * 2 # seconds * samples rate * chan count

#---- Application ---------------------------------------------------------
print "===================================="
print "* I2S write"
print "===================================="

local_com_port = sys.argv[1] if (len(sys.argv) > 1) else COM_PORT_ENG

# Open serial port
print "Open serial port " + local_com_port
try:
    ser = serial.Serial(local_com_port, 115200, timeout=10)
    print "COM port OK" 
except:
    print "Error COM port" 
    sys.exit(0)

data = bytearray(data_cnt * 8)
for i in range(0, data_cnt):
	sampleR = int(0x40000000 + 0x40000000 * math.sin(2 * 3.14 * i/44))
	sampleL = int(0x40000000 + 0x40000000 * math.sin(2 * 3.14 * i/11))
	#sampleR = 0
	#sampleR = 0

	data[i * 8 ] = sampleR & 0xFF
	data[i * 8 + 1] = (sampleR >> 8) & 0xFF
	data[i * 8 + 2] = (sampleR >> 16) & 0xFF
	data[i * 8 + 3] = (sampleR >> 24) & 0xFF

	data[i * 8 + 4] = sampleL & 0xFF
	data[i * 8 + 5] = (sampleL >> 8) & 0xFF
	data[i * 8 + 6] = (sampleL >> 16) & 0xFF
	data[i * 8 + 7] = (sampleL >> 24) & 0xFF


# send to target
print("Sending buffer...")
print("len = " + str(len(data)))

if (put_buffer(ser, data) == 0):
	sys.exit(0)


print("Starting...")
usb2io_sendcmd(ser, "i2s writebuffer 1, " + str(data_cnt) + "\r\n")

raw_input("Press Enter to exit ...")