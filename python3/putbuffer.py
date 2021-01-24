import os
import sys
import time
import serial
import select
import zlib

MAX_SEND_LEN = 1024 * 1024
ACK_TIMEOUT = 10000


#***********************************************************************************
#***********************************************************************************
# for interal use.
# transfers array over 'ser' using raw protocol
#***********************************************************************************
#***********************************************************************************	
def upload_buffer(ser, in_buffer):
	rrd = ser.readline().decode("utf-8")
	if (rrd != 'Ready\r\n'):
			print ("target not ready")
			return 0
	#print ("Target is ready")

	length = len(in_buffer)
	
	# header of  two uint32 values should be sent before payload:
	# data length (without header) + crc32 over payload
	data = bytearray(8 + length)
	data[8 : 8 + length] = in_buffer
	# Fill lenght
	data[0] = length & 0xFF
	data[1] = (length >> 8) & 0xFF
	data[2] = (length >> 16) & 0xFF
	data[3] = (length >> 24) & 0xFF
	# Calulate crc32
	buff = data[8:length]
	crc = zlib.crc32(buff) % 0x100000000
	# Fill the packet
	data[4] = crc & 0xFF
	data[5] = (crc >> 8) & 0xFF
	data[6] = (crc >> 16) & 0xFF
	data[7] = (crc >> 24) & 0xFF
	
	to_send_len = len(data)
	sent = 0
	
	while (sent < to_send_len):
		sent_len = to_send_len - sent
		if (sent_len > MAX_SEND_LEN):
			sent_len = MAX_SEND_LEN
		sendbuf = data[sent:sent_len]
		ser.write(sendbuf)
		sent += sent_len
	
	rrd = ""
	retry_cnt = 0
	start_time_ms = int(round(time.time() * 1000))
	while ((rrd == "") & (retry_cnt < 100)):
		retry_cnt = retry_cnt + 1
		rrd = ser.readline().decode("utf-8")
		if (rrd == ""):
			print(".\r\n")
			# check timeout
			if (int(round(time.time() * 1000)) - start_time_ms > ACK_TIMEOUT):
				break;

		#else:
		#	print(rrd)

	if (rrd != 'OK\r\n'):
		return 0
	return 1


#***********************************************************************************
#***********************************************************************************
# Uploads fpga image directly to fpga's sram, thus recongires it
# ser - serial port
# file_name - path to *.rbf file with fpga image
#***********************************************************************************
#***********************************************************************************

def put_fpga_image_raw(ser, file_name):

	#read file
	frawfile = open(file_name, 'rb')
	filesz = os.path.getsize(file_name)
	if not filesz:
		return False
	
	data = frawfile.read(filesz)
	
	if not data:
		return False

	#initialize buffer communication and wait for reply
	ser.write("fpga rawload\r\n".encode("utf-8"));
	return upload_buffer(ser, data)

#***********************************************************************************
#***********************************************************************************
# Uploads fpga image to qspi flash. The FPGA is NOT reconfigured.
# Info: qspi flash can store up to 16 fpga images. Each image has 'index' - a number from 0 to 15.
#	Each image is marked as "default" or "non-default". When USB2IO starts up, the default
#	image is loaded to fpga. Only one image can be marked as "default".
# ser - serial port
# file_name - path to *.rbf file with fpga image
# index - index of image (one of 16 locations in the qspi flash)
# is_default - when == 1, the image is marked as 'default' after storing to flash. If qspi flash already 
# 		   has 'default' image, the old one is marked as 'non-default'.
#***********************************************************************************
#***********************************************************************************

def put_fpga_image_qspi(ser, file_name, index, is_default):

	#read file
	frawfile = open(file_name, 'rb')
	filesz = os.path.getsize(file_name)
	if not filesz:
		return False
	
	data = frawfile.read(filesz)
	
	if not data:
		return False
	#initialize buffer communication and wait for reply
	tx_cmd = "fpga save image " + str(index) + ", " + str(is_default) +"\r\n"
	ser.write(tx_cmd.encode("utf-8"))
	return upload_buffer(ser, data)

#***********************************************************************************
#***********************************************************************************
# Puts 'in_buffer' array to SDRAM buffer in uC, starting from address 0
#***********************************************************************************
#***********************************************************************************
def put_buffer(ser, in_buffer):
	#initialize buffer communication and wait for reply
	ser.write("put buffer\r\n".encode("utf-8"))
	return upload_buffer(ser, in_buffer)
