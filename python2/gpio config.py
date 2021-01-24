#=====================================================
#  Gpio config
#=====================================================
import os
import sys
import time
import serial
import select

COM_PORT_ENG                = 'COM17'

#---- Application ---------------------------------------------------------
print "===================================="
print "* Gpio config"
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

wro = ser.write("expv write 3300\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)

print("Configuring:")
print("0 - 50 Mhz")
print("1 - Si570 output")
print("2,3 - '0'")
print("4,5 - '1'")
print("6-15 - GPOutput")


# 0 - 50 Mhz
wro = ser.write("gpio configure 0, 5\r\n")
time.sleep(0.1)
rrd = ser.readline()
if (rrd != 'OK\r\n'):
	print(rrd)

#1 - Si570
wro = ser.write("gpio configure 1, 6\r\n")
time.sleep(0.1)
rrd = ser.readline()
if (rrd != 'OK\r\n'):
	print(rrd)


#2, 3 = 0
wro = ser.write("gpio configure 2, 1\r\n")
time.sleep(0.1)
rrd = ser.readline()
if (rrd != 'OK\r\n'):
	print(rrd)

wro = ser.write("gpio configure 3, 2\r\n")
time.sleep(0.1)
rrd = ser.readline()
if (rrd != 'OK\r\n'):
	print(rrd)


#4,5 = 1
wro = ser.write("gpio configure 4, 3\r\n")
time.sleep(0.1)
rrd = ser.readline()
if (rrd != 'OK\r\n'):
	print(rrd)


wro = ser.write("gpio configure 5, 3\r\n")
time.sleep(0.1)
rrd = ser.readline()
if (rrd != 'OK\r\n'):
	print(rrd)


#6-16 = GP Out
wro = ser.write("gpio configure 6, 3\r\n")
time.sleep(0.1)
rrd = ser.readline()
if (rrd != 'OK\r\n'):
	print(rrd)

wro = ser.write("gpio configure 7, 3\r\n")
time.sleep(0.1)
rrd = ser.readline()
if (rrd != 'OK\r\n'):
	print(rrd)

wro = ser.write("gpio configure 8, 3\r\n")
time.sleep(0.1)
rrd = ser.readline()
if (rrd != 'OK\r\n'):
	print(rrd)

wro = ser.write("gpio configure 9, 3\r\n")
time.sleep(0.1)
rrd = ser.readline()
if (rrd != 'OK\r\n'):
	print(rrd)

wro = ser.write("gpio configure 10, 3\r\n")
time.sleep(0.1)
rrd = ser.readline()
if (rrd != 'OK\r\n'):
	print(rrd)

wro = ser.write("gpio configure 11, 3\r\n")
time.sleep(0.1)
rrd = ser.readline()
if (rrd != 'OK\r\n'):
	print(rrd)

wro = ser.write("gpio configure 12, 3\r\n")
time.sleep(0.1)
rrd = ser.readline()
if (rrd != 'OK\r\n'):
	print(rrd)

wro = ser.write("gpio configure 13, 3\r\n")
time.sleep(0.1)
rrd = ser.readline()
if (rrd != 'OK\r\n'):
	print(rrd)

wro = ser.write("gpio configure 14, 3\r\n")
time.sleep(0.1)
rrd = ser.readline()
if (rrd != 'OK\r\n'):
	print(rrd)

wro = ser.write("gpio configure 15, 3\r\n")
time.sleep(0.1)
rrd = ser.readline()
if (rrd != 'OK\r\n'):
	print(rrd)


raw_input("Press Enter to continue...")
print("Configuring All to WFG...")
wro = ser.write("gpio configure 255, 4\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)

raw_input("Press Enter to exit...")