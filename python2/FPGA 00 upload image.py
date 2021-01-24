#=====================================================
#  FPGA image upload using RAW transfer
#  
#
#=====================================================
import os
import sys
import time
import serial
import select
from putbuffer import put_fpga_image_raw

COM_PORT_ENG                = 'COM17'
fpga_filename               = "USB2IO_Waveform.rbf"

#---- Application ---------------------------------------------------------
print "===================================="
print "* RAW transfer test"
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

print "Upload image to FPGA SRAM using RAW protocol"
rrd = put_fpga_image_raw(ser, fpga_filename)
if (rrd == 1):
	print "Success.\r\n"
else:
	print "Failed.\r\n"

# Close serial port
ser.close()
raw_input("Press Enter to exit...")

