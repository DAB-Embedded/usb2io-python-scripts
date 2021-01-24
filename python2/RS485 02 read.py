#=====================================================
#  RS485 read
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
print "* RS485 (over UART4)"
print "* pin connection:"
print "* GPIO 2 -  #Re"
print "* GPIO 3 -  Rx"
print "* GPIO 4 -  Tx"
print "* GPIO 5 -  DE"
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
# format: rs485 read channel, timeout\r\n
usb2io_sendcmd(ser, "rs485 read 4, 10000\r\n")


raw_input("Press Enter to exit ...")