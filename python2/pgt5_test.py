#=====================================================
#  PocketGeiger Type5 functional test
#  
#
#=====================================================
import os
import sys
import time
import serial
import select
import rawx.base
import rawx.const
import rawx.error
import rawx.tools
import rawx.protocol.rawxt
import re

from rawx.protocol.rawxt import *

COM_PORT_ENG                = 'COM17'

def usb2io_command(ser, command):
	ser.write(command)
	time.sleep(0.05)
	rrd = ser.readline()
	print (rrd)

#---- Application ---------------------------------------------------------
print "===================================="
print "* PGT5 test"
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

# Set Ext voltage to 3.3V
print "Configure EXT voltage to 3.3V"
ser.write("expv write 3300\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)

print("Timer 1 configuration...")
# tim1 capture init a,b,c,d
#   a - Timer channel (only 1 available)
#   b - input clock divider for internal timer (1,2,4)
#   c - prescaler for input clock (0..65535)
#   d - input detect edge (0 - Rising, 1 - Falling, 2 - Both)
#
#   Note: Base timer clock is 237.5 MHz. Based on current settings, result clk = 906 Hz
usb2io_command(ser, "tim1 capture init 1, 1, 1, 1\r\n")

print("Configuring 1 pin to GPIO15 (timer1 ch1 input)")
usb2io_command(ser, "gpio configure 15, 14\r\n")

print("Reset counter...")
#usb2io_command(ser, "tim1 capture reset\r\n")

print("Wait for 10 sec")
time.sleep(1)

print("Get capture value")
ser.write("tim1 capture get\r\n")
time.sleep(0.05)
rrd = ser.readline()
print rrd
res_i = [int(s) for s in re.findall(r'\b\d+\b', rrd)]

alpha = 53.032;
a = res_i[0] / 3.0

print("CPM %f, uSv/h %f\r\n" % (a, a/alpha))

print("Stop counter...")
#usb2io_command(ser, "tim1 capture stop\r\n")

# Close serial port
ser.close()
print "End" 
raw_input("Press Enter to exit...")
