#=====================================================
#  I2S functional test
#=====================================================
import os
import sys
import time
import serial
import select

COM_PORT_ENG                = 'COM17'

#---- Application ---------------------------------------------------------
print "===================================="
print "* I2S config"
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


print("Configuring 4 pins to spi repeater...")

wro = ser.write("gpio configure 2, 7\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)

wro = ser.write("gpio configure 3, 7\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)

wro = ser.write("gpio configure 4, 7\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)

wro = ser.write("gpio configure 5, 7\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)

print("Configuring I2S unit...")

# chan = 2
# Audio standard =   I2S_STANDARD_MSB (1)
# Data format = I2S_DATAFORMAT_32B(3)
# Audio frequency = 22K (3)
# Clock polarity = 0
# First bit = MSB (0)
# FrameSync inversion = DISABLE (0)
# 24bit frame alignment = LEFT (1)
wro = ser.write("i2s configure 1, 1, 3, 3, 1, 0, 0, 1 \r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)


raw_input("Press Enter to exit ...")