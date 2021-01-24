"""@package docstring
usb2io functions module.

"""
import os
import sys
import time
import serial
import select
import zlib

def usb2io_sendcmd(ser, cmd, silent =  0):

	#Send command and wait for reply
	ser.write(cmd);
	#time.sleep(0.05)
	rrd = ser.readline()
	if (silent == 0):
		print(rrd)

	return rrd


