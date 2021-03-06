#=====================================================
#  UART read buffer
#=====================================================
import os
import sys
import time
import serial
import select
from usb2io import usb2io_sendcmd
from getbuffer import get_buffer

COM_PORT_ENG                = 'COM17'

#---- Application ---------------------------------------------------------
print "===================================="
print "* UART1 config"
print "* pin connection:"
print "* GPIO10  - UART1 Rx"
print "* GPIO11  - UART1 Tx"
print "* GPIO12  - UART1 RTS"
print "* GPIO13  - UART1 CTS"
print "===================================="

local_com_port = sys.argv[1] if (len(sys.argv) > 1) else COM_PORT_ENG

# Open serial port
print "Open serial port " + local_com_port
try:
    ser = serial.Serial(local_com_port, 115200, timeout=30)
    print "COM port OK" 
except:
    print "Error COM port" 
    sys.exit(0)


print("Reading...")
data_count = 12
# format: uart readbuffer channel, data_count, timeout\r\n
if (usb2io_sendcmd(ser, "uart readbuffer 1, " + str(data_count) + ", 1000\r\n") != "OK\r\n"):
    sys.exit(0);

(status, data_out) = get_buffer(ser, data_count)
print "get_buffer return status: %r" % status
print data_out.encode("hex")


raw_input("Press Enter to exit ...")