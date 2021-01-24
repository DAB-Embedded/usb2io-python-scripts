#=====================================================
#  I2C functional test
#=====================================================
import os
import sys
import time
import serial
import select
from usb2io import usb2io_sendcmd

COM_PORT_ENG                = 'COM17'
# port select. 1 - stm32, 2 - fpga
port = 1
#---- Application ---------------------------------------------------------
print ("====================================")
print ("* I2C scan")
print ("====================================")

local_com_port = sys.argv[1] if (len(sys.argv) > 1) else COM_PORT_ENG

# Open serial port
print ("Open serial port " + local_com_port)
try:
    ser = serial.Serial(local_com_port, 115200, timeout=3)
    print ("COM port OK" )
except:
    print ("Error COM port" )
    sys.exit(0)

print ("Scan I2C bus")
rrd = usb2io_sendcmd(ser, "i2c scan " + str(port) + "\r\n", 1)
print(rrd)

# Close serial port
ser.close()
input("Press Enter to exit ...")

