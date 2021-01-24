#=====================================================
#  I2C functional test
#=====================================================
import os
import sys
import time
import serial
import select

COM_PORT_ENG                = 'COM17'
# port select. 1 - stnm32, 2 - fpga
port = 1
#---- Application ---------------------------------------------------------
print "===================================="
print "* I2C scan"
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

    
print "Scan I2C bus"
wro = ser.write("i2c scan " + str(port) + "\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)


# Close serial port
ser.close()
raw_input("Press Enter to exit ...")

