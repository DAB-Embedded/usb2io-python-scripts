"""@package docstring
getbuffer module.

Module for receiving data from device over USB.
"""
import os
import sys
import time
import serial
import select
import zlib

def get_buffer(ser, length):

	#initialize buffer communication and wait for reply
	ser.write("get buffer\r\n");
	rrd = ser.readline()
	if (rrd != 'READY\r\n'):
			print "target not ready"
			return (False, "")

	print "Target is ready"
		
	# header of  two uint32 values should be sent before payload:
	# data length (without header) + crc32 over payload
           
	data = bytearray(8)

	data[0] = length & 0xFF
	data[1] = (length >> 8) & 0xFF
	data[2] = (length >> 16) & 0xFF
	data[3] = (length >> 24) & 0xFF

	#calulate crc32
	buff = buffer(data, 8, length)
	crc = zlib.crc32(buff) % 0x100000000 
	
	# fill the packet
	data[4] = crc & 0xFF
	data[5] = (crc >> 8) & 0xFF
	data[6] = (crc >> 16) & 0xFF
	data[7] = (crc >> 24) & 0xFF

	ser.flush()
	ser.write(data)

	out_buffer = ser.read(length)
	
	rrd = ser.readline()
	print(rrd)
	
	if (rrd != 'OK\r\n'):
		return (False, "")
	
	return (True, out_buffer)


def get_buffer_fast(ser, length):

	#initialize buffer communication and wait for reply
	ser.write("get buffer\r\n");
	rrd = ser.readline()
	if (rrd != 'READY\r\n'):
			print "target not ready"
			return (False, "")

	# header of  two uint32 values should be sent before payload:
	# data length (without header) + crc32 over payload
           
	data = bytearray(8)

	data[0] = length & 0xFF
	data[1] = (length >> 8) & 0xFF
	data[2] = (length >> 16) & 0xFF
	data[3] = (length >> 24) & 0xFF

	#calulate crc32
	buff = buffer(data, 8, length)
	crc = zlib.crc32(buff) % 0x100000000 
	
	# fill the packet
	data[4] = crc & 0xFF
	data[5] = (crc >> 8) & 0xFF
	data[6] = (crc >> 16) & 0xFF
	data[7] = (crc >> 24) & 0xFF

	ser.flush()
	ser.write(data)

	if length > (512 * 1024) :
		time.sleep(0.5)

	out_buffer = ser.read(length)
	
	rrd = ser.readline()
	if (rrd != 'OK\r\n'):
		return (False, "")
	
	return (True, out_buffer)

#************************************************************************
# get data fromm fpga buffer
# options:
#                 0 - send immediatelly
#                 1 - send when DCMI frame is ready
#************************************************************************
def get_fpga_buffer(ser, length, options):

	#initialize buffer communication and wait for reply
	ser.write("get fpga buffer " + str(length) + ", " + str(options) + "\r\n");
	rrd = ser.readline()
	if (rrd != 'READY\r\n'):
			print "target not ready"
			return (False, "")

	#print "Target is ready"
		
	out_buffer = ser.read(length)
      	#print "Got data"

	rrd = ser.readline()
	#print(rrd)
	
	if (rrd != 'OK\r\n'):
		return (False, "")
	
	return (True, out_buffer)
	
