#=====================================================
#  UART write
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
    ser = serial.Serial(local_com_port, 115200, timeout=3)
    print "COM port OK" 
except:
    print "Error COM port" 
    sys.exit(0)


print("Writing...")

# format: uart write channel, data_word
if usb2io_sendcmd(ser, "uart write 1, 0x30\r\n") != "OK\r\n":
	print "failed."
	sys.exit(0)


raw_input("Press Enter to exit ...")