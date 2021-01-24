#=====================================================
#  Get buffer functional test
#  
#
#=====================================================
import os
import sys
import time
import serial
import select
import struct
import zlib
import binascii
import rawx.base
import rawx.const
import rawx.error
import rawx.tools
import rawx.protocol.rawxt
from rawx.protocol.rawxt import *
from getbuffer import get_buffer

COM_PORT_ENG                = 'COM17'

#---- Application ---------------------------------------------------------
print "===================================="
print "* Get buffer tester"
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

(status, data_out) = get_buffer(ser, 128)

print "get_buffer return status: %r" % status
print data_out.encode("hex")


# Close serial port
ser.close()
print "API test done" 

