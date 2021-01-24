#=====================================================
#  RS485 config
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
print "* RS485 (over UART4) config"
print "* pin connection:"
print "* GPIO 2 -  #Re"
print "* GPIO 3 -  Rx"
print "* GPIO 4 -  Tx"
print "* GPIO 5 -  DE"
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

#if usb2io_sendcmd(ser, "gpio configure 2, 17\r\n") != "OK\r\n":

# static 0 to enable echo
if usb2io_sendcmd(ser, "gpio configure 2, 1\r\n") != "OK\r\n":
	print "failed."
	sys.exit(0)


if usb2io_sendcmd(ser, "gpio configure 3, 17\r\n") != "OK\r\n":
	print "failed."
	sys.exit(0)

if usb2io_sendcmd(ser, "gpio configure 4, 17\r\n") != "OK\r\n":
	print "failed."
	sys.exit(0)


if usb2io_sendcmd(ser, "gpio configure 5, 17\r\n") != "OK\r\n":
	print "failed."
	sys.exit(0)


print("Configuring cntroller...")

#format: rs485 configure channel, baudrate, word_length, stop_bits, parity
if usb2io_sendcmd(ser, "rs485 configure 4, 50000, 8, 1, 0\r\n") != "OK\r\n":
	print "failed."
	sys.exit(0)

raw_input("Press Enter to exit ...")