#=====================================================
#  UART read
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
    ser = serial.Serial(local_com_port, 115200, timeout=30)
    print "COM port OK" 
except:
    print "Error COM port" 
    sys.exit(0)


print("Reading...")
# format: uart read channel, timeout\r\n
usb2io_sendcmd(ser, "uart read 1, 1000\r\n")


raw_input("Press Enter to exit ...")