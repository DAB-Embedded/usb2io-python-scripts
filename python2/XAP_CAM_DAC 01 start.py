#=====================================================
#  XAP DAC Start
#=====================================================
import os
import sys
import time
import serial
import select

COM_PORT_ENG                = 'COM17'

#---- Application ---------------------------------------------------------
print "===================================="
print "* XAP DAC Start"
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

print("Starting spimaster...")
wro = ser.write("spimaster start\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)

print "Done\n\r"
raw_input("Press Enter to exit...")