#=====================================================
#  UART write buffer
#=====================================================
import os
import sys
import time
import serial
import select
from usb2io import usb2io_sendcmd
from putbuffer import put_buffer

COM_PORT_ENG                = 'COM17'

#---- Application ---------------------------------------------------------
print "===================================="
print "* UART4 write"
print "* pin connection:"
print "* GPIO2  - UART4 CTS"
print "* GPIO3  - UART4 Rx"
print "* GPIO4  - UART4 Tx"
print "* GPIO5  - UART4 RTS"
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

data_count = 4

#put data to buffer
data = bytearray(data_count)
for i in range (0, data_count):
	data[i] = i + 1
                             
# send to target
print("Sending buffer...")

if (put_buffer(ser, data) == 0):
	sys.exit(0)


print("UART Writing...")

# format: uart writebuffer channel, data_count
if usb2io_sendcmd(ser, "uart writebuffer 4," + str(data_count) + "\r\n") != "OK\r\n":
	print "failed."
	sys.exit(0)


raw_input("Press Enter to exit ...")