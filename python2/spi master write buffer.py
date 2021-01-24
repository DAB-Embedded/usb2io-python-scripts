#=====================================================
#  SPI Master write buffer
#=====================================================
import os
import sys
import time
import serial
import select
import modem.base
import modem.const
import modem.error
import modem.tools
import modem.protocol.ymodem
from modem.protocol.ymodem import *
from putbuffer import put_buffer

COM_PORT_ENG                = 'COM17'

#---- Application ---------------------------------------------------------
print "===================================="
print "* SPI Master write buffer"
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


wro = ser.write("hello\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)

print("Writing to buffer...")
wro = ser.write("spimaster write buffer 0x6\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)


raw_input("Press Enter to exit...")