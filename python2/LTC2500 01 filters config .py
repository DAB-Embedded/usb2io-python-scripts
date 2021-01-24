#=====================================================
#  LTC2500 config
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
print "* LTC2500 filters"
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


print("configuring LTC2500 filters...")

# type:
# 1 - SINC1
# 2 - SINC2
# 3 - SINC3
# 4 - SINC4
# 5 - SSINC
# 6 - FLAT PASSBAND
# 7 - AVERAGING
filter_type = 1

# downsampling factor
# 2 - 4
# 3 - 8
# 4 - 16
# 5 - 32
# 6 - 64
# 7 - 128
# 8 - 256
# 9 - 512
# 10 - 1024
# 11 - 2048 
# 12 - 4096
# 13 - 8192
# 14 - 16384
df = 2

# digital gain expansion
dge = 0

# digital gain compression
dgc = 0

if (usb2io_sendcmd(ser, "ltc2500 filters configure " + str(filter_type) + ", " + str(df) + ", " + str(dge) + ", " + str(dgc) + "\r\n") != "OK\r\n"):
	print "failed."
	sys.exit(0)


raw_input("Press Enter to exit ...")