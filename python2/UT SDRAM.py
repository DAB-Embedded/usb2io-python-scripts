#=====================================================
#  SDRAM test
#=====================================================
import os
import sys
import time
import serial
import select
from putbuffer import put_buffer
from getbuffer import get_buffer
import math
from usb2io import usb2io_sendcmd
import random


COM_PORT_ENG                = 'COM17'
data_cnt = 32 * 1024 * 1024 - 2048



#---- Application ---------------------------------------------------------
print "===================================="
print "* SDRAM test"
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

usb2io_sendcmd(ser, "hello\r\n")

print "Preparing data..." 
src = bytearray(data_cnt)
dest = bytearray(data_cnt)

for i in range(0, data_cnt):
	src[i] = random.randrange(256)


# send to target
print("Sending buffer...")
print("len = " + str(len(src)))

if (put_buffer(ser, src) == 0):
	print("Failed.");
	sys.exit(0)


# get buffer
print("Reading...")
(status, data_out) = get_buffer(ser, data_cnt)

print "get_buffer return status: %r" % status
dest[0 : data_cnt] = data_out

print("Compare...")

errCnt = 0
for i in range(0, data_cnt):
        if (dest[i] != src[i]):
		errCnt = errCnt + 1
print("Errors: " + str(errCnt))
raw_input("Press Enter to exit ...")