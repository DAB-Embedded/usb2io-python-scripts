#=====================================================
#  I2S functional test
#  
#
#=====================================================
import os
import sys
import time
import serial
import select

COM_PORT_ENG                = 'COM17'

#---- Application ---------------------------------------------------------
print "===================================="
print "* I2S write"
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

print("Sending data...")

wro = ser.write("i2s write 1, 0x5, 0x0, 0x00, 0x00, 0x15, 0x00, 0x00, 0x00, 0x55, 0x00, 0x00, 0x00, 0x55, 0x01, 0x00, 0x00\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)
                                                     




raw_input("Press Enter to exit ...")