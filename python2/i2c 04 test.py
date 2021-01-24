#=====================================================
#  I2C functional test
#=====================================================
import os
import sys
import time
import serial
import select

COM_PORT_ENG                = 'COM17'

#---- Application ---------------------------------------------------------
print "===================================="
print "* I2C test"
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

print "Configure I2C"
wro = ser.write("i2c configure 1, 2\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)
    
print "Scan I2C bus"
wro = ser.write("i2c scan 1\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)

print "Read EEPROM"
wro = ser.write("i2c read 1, 0x50,10\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)

# Close serial port
ser.close()
print "API test done" 

