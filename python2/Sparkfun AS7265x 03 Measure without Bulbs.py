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


device = AS7265x(ser)
print "Measuring..."
if (device.takeMeasurements() != True):
    print "Failed"
print "Done."

value = device.getCalibratedA()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "A = %f" %value[1]
       
value = device.getCalibratedB()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "B = %f" %value[1]

value = device.getCalibratedC()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "C = %f" %value[1]

value = device.getCalibratedD()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "D = %f" %value[1]

value = device.getCalibratedE()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "E = %f" %value[1]

value = device.getCalibratedF()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "F = %f" %value[1]

value = device.getCalibratedG()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "G = %f" %value[1]

value = device.getCalibratedH()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "H = %f" %value[1]

value = device.getCalibratedI()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "I = %f" %value[1]

value = device.getCalibratedJ()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "J = %f" %value[1]

value = device.getCalibratedK()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "K = %f" %value[1]

value = device.getCalibratedL()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "L = %f" %value[1]

value = device.getCalibratedR()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "R = %f" %value[1]

value = device.getCalibratedS()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "S = %f" %value[1]

value = device.getCalibratedT()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "T = %f" %value[1]

value = device.getCalibratedU()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "U = %f" %value[1]

value = device.getCalibratedV()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "V = %f" %value[1]

value = device.getCalibratedW()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "W = %f" %value[1]

   