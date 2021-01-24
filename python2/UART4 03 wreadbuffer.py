#=====================================================
#  UART write-read buffer
#=====================================================
import os
import sys
import time
import serial
import select
from usb2io import usb2io_sendcmd
from putbuffer import put_buffer
from getbuffer import get_buffer

COM_PORT_ENG                = 'COM17'

#---- Application ---------------------------------------------------------
print "===================================="
print "* UART4 write/read"
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


print("UART Wreading...")

# format: uart wreadbuffer channel, data_count
res = usb2io_sendcmd(ser, "uart wreadbuffer 4," + str(data_count) + "\r\n")
if (res.find("OK") != -1):	
	# parse result
	bytes_str = res[3:]
	rx_cnt = int(bytes_str, 10) 

#	print "received = " + str(rx_cnt)
	(status, data_out) = get_buffer(ser, rx_cnt)
	if (status == True):
		print data_out.encode("hex")
	else:
		print "Get buffer failed"
	print "\r\n"

else:
	print "failed."

raw_input("Press Enter to exit ...")