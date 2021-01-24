#=====================================================
#  XAP DAC Send single
#=====================================================
import os
import sys
import time
import serial
import select

COM_PORT_ENG                = 'COM17'

#---- Application ---------------------------------------------------------
print "===================================="
print "* XAP DAC Send single"
print "===================================="

local_com_port = COM_PORT_ENG

if (len(sys.argv) < 2):
	print "Specify argument." 
	sys.exit(0)
# Open serial port
print "Open serial port " + local_com_port
try:
	ser = serial.Serial(local_com_port, 115200, timeout=3)
	print "COM port OK" 
except:
	print "Error COM port" 
	sys.exit(0)


print("Sending single...")
wro = ser.write("spimaster send single " + sys.argv[1] + "\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)

raw_input("Press Enter to exit...")