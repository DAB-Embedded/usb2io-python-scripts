#=====================================================
#  SPI functional test
#=====================================================
import os
import sys
import time
import serial
import select
from putbuffer import put_buffer
from usb2io import usb2io_sendcmd


COM_PORT_ENG                = 'COM17'
packet_len = 4
packets_cnt = 3
#---- Application ---------------------------------------------------------
print "===================================="
print "* SPI writebuffer"
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



data = bytearray(packet_len * packets_cnt)
for i in range (0, packets_cnt * packet_len):
	data[i] = i + 1


# send to target
print("Sending buffer...")
print("len = " + str(len(data)))

if (put_buffer(ser, data) == 0):
	sys.exit(0)


	
usb2io_sendcmd(ser, "spi writebuffer 1, " + str(packet_len) + ", " + str(packets_cnt) + "\r\n") 
raw_input("Press Enter to exit ...")
