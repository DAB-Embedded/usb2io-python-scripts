from AS7265x import AS7265x
import os
import sys
import time
import serial
import select
from usb2io import usb2io_sendcmd

COM_PORT_ENG                = 'COM17'

#---- Application ---------------------------------------------------------
print "===================================="
print "* Sparkfun AS7265x Sersor example"
print "* GPIO0 - Reset                  "
print "* GPIO2 - Interrupt              "
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

print("Configuring  pins + reset..")

if usb2io_sendcmd(ser, "gpio configure 2, 0\r\n") != "OK\r\n":
	print "failed."
	sys.exit(0)
time.sleep(0.1)

if usb2io_sendcmd(ser, "gpio configure 0, 1\r\n") != "OK\r\n":
	print "failed."
	sys.exit(0)
time.sleep(0.1)

if usb2io_sendcmd(ser, "gpio configure 0, 2\r\n") != "OK\r\n":
	print "failed."
	sys.exit(0)
time.sleep(1)


device = AS7265x(ser)

# if you want some info, uncomment next lines
#print "Type = ";
#print device.getDeviceType()
#print "HW version = ";
#print device.getHardwareVersion()
#print "Major FW = ";
#print device.getMajorFirmwareVersion()
#print "Patch FW = ";
#print device.getPatchFirmwareVersion()
#print "Build FW = ";
#print device.getBuildFirmwareVersion()

print "Initialization..."
if (device.begin() != True):
    print "Failed"
print "Done."
