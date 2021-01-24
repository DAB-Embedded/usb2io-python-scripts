#=====================================================
#  UART config
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
print "* UART4 config"
print "* pin connection:"
print "* GPIO2  - UART4 CTS"
print "* GPIO3  - UART4 Rx"
print "* GPIO4  - UART4 Tx"
print "* GPIO5  - UART4 RTS"
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



print("Configuring  pins...")

if usb2io_sendcmd(ser, "gpio configure 2, 8\r\n") != "OK\r\n":
	print "failed."
	sys.exit(0)


if usb2io_sendcmd(ser, "gpio configure 3, 8\r\n") != "OK\r\n":
	print "failed."
	sys.exit(0)

if usb2io_sendcmd(ser, "gpio configure 4, 8\r\n") != "OK\r\n":
	print "failed."
	sys.exit(0)

if usb2io_sendcmd(ser, "gpio configure 5, 8\r\n") != "OK\r\n":
	print "failed."
	sys.exit(0)

print("Configuring cntroller...")

#format: uart configure channel, baudrate, word_length, stop_bits, parity
if usb2io_sendcmd(ser, "uart configure 4, 50000, 8, 1, 0\r\n") != "OK\r\n":
	print "failed."
	sys.exit(0)

raw_input("Press Enter to exit ...")