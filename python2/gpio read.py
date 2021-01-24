#=====================================================
#  GPIO read
#=====================================================
import os
import sys
import time
import serial
import select

COM_PORT_ENG                = 'COM17'


#---- Application ---------------------------------------------------------
print "===================================="
print "* Gpio read"
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

print("Configuring All to function GP Output...")
wro = ser.write("gpio configure 255, 3\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)

print("Write All '0'...")
wro = ser.write("gpio write 0\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)

wro = ser.write("gpio read\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)


raw_input("Press Enter to continue...")

print("Write All '1'...")
wro = ser.write("gpio write 0xFFFF\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)

wro = ser.write("gpio read\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)


raw_input("Press Enter to continue...")


print("Write odd '0', even '1'...")
wro = ser.write("gpio write 0x5555\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)

wro = ser.write("gpio read\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)


raw_input("Press Enter to continue...")

print("Write 8 lower to '1', higher to '0'...")
wro = ser.write("gpio write 0x00FF\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)

wro = ser.write("gpio read\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)


raw_input("Press Enter to exit...")
