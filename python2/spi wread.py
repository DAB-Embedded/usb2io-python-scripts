#=====================================================
#  SPI functional test
#  
#
#=====================================================
import os
import sys
import time
import serial
import select
from usb2io import usb2io_sendcmd

COM_PORT_ENG                = 'COM17'

#---- Application ---------------------------------------------------------
print "===================================="
print "* SPI test"
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

# pin 2..5 - SPI
print "Configure pins [2..5] to SPI mode"
usb2io_sendcmd(ser, "gpio configure 2,7\r\n")
usb2io_sendcmd(ser, "gpio configure 3,7\r\n")
usb2io_sendcmd(ser, "gpio configure 4,7\r\n")
usb2io_sendcmd(ser, "gpio configure 5,7\r\n")
    
# Set Ext voltage to 3.3V
print "Configure EXT voltage to 3.3V"
usb2io_sendcmd(ser, "expv write 3300\r\n")

#print "Configure SPI: Set 100KHz clock, Polarity low, CS active high, Phase 1st, MSB"
usb2io_sendcmd(ser, "spi configure 1,0,0,0,100000,0\r\n")
    

print "Write to SPI device 2 bytes and read back"
usb2io_sendcmd(ser, "spi wread 1,0x51,0x7a\r\n")

# Close serial port
ser.close()
print "API test done" 
raw_input("Press Enter to exit...")
