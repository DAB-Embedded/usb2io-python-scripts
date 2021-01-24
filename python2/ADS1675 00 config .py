#=====================================================
#  ADS1675 config
#  
#
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
print "* ADS1675 config"
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


# Set Ext voltage to 2.5V
print("Setting voltage to 2.5V ...")
if (usb2io_sendcmd(ser, "expv write 2500\r\n") != "OK\r\n"):
	print "failed."
	sys.exit(0)

                      
print("configuring ADS1675 ...")

# data rate:
#	 0 - 125 KSPS
#	 1 - 250 KSPS
#	 2 - 500 KSPS
#	 3 - 1 MSPS
#	 4 - 2 MSPS
#	 5 - 4 MSPS
drate = 0
# filter:
#	 0 - Single cycle (low latency)
#	 1 - Fast responce (low latency)
#	 2 - wide bandwidth

fltr = 2

if (usb2io_sendcmd(ser, "ads1675 configure " + str(drate) + ", " + str(fltr) + "\r\n") != "OK\r\n"):
	print "failed."
	sys.exit(0)


raw_input("Press Enter to exit ...")