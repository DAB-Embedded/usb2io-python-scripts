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
if (device.takeMeasurementsWithBulb() != True):
    print "Failed"
print "Done."

value = device.getA()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "A = 0x%x" %value[1]
       
value = device.getB()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "B = 0x%x" %value[1]

value = device.getC()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "C = 0x%x" %value[1]

value = device.getD()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "D = 0x%x" %value[1]

value = device.getE()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "E = 0x%x" %value[1]

value = device.getF()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "F = 0x%x" %value[1]

value = device.getG()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "G = 0x%x" %value[1]

value = device.getH()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "H = 0x%x" %value[1]

value = device.getI()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "I = 0x%x" %value[1]

value = device.getJ()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "J = 0x%x" %value[1]

value = device.getK()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "K = 0x%x" %value[1]

value = device.getL()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "L = 0x%x" %value[1]

value = device.getR()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "R = 0x%x" %value[1]

value = device.getS()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "S = 0x%x" %value[1]

value = device.getT()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "T = 0x%x" %value[1]

value = device.getU()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "U = 0x%x" %value[1]

value = device.getV()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "V = 0x%x" %value[1]

value = device.getW()
if (value[0] != True):
    print "Failed"
    sys.exit(0)
print "W = 0x%x" %value[1]

   