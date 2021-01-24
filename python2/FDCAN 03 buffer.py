#=====================================================
# send \ receive messages over FDCAN 
#=====================================================
import os
import sys
import time
import serial
import select
import modem.base
import modem.const
import modem.error
import modem.tools
import modem.protocol.ymodem
from modem.protocol.ymodem import *
from putbuffer import put_buffer
from getbuffer import get_buffer
from usb2io import usb2io_sendcmd
from StringIO import StringIO
import csv

#*************************************************************************
def serialize_messages(messages):
	# byte array should have following structure:
	# 0xC0 - start marker
	# 0x00 or 0x01 - type (0 - std, 1 - extended)
	# ID - identifier. 2 bytes for std, 4 bytes for ext
	# NN - data count
	# DT - payload
	array = bytearray()

	for i in range(len(messages)):

		array.append(0xC0)
		if (messages[i]["type"] == "std"):
			array.append(0x00)
			array.append(messages[i]["id"] & 0xFF)
			array.append((messages[i]["id"] >> 8) & 0x07)
	
		else:
			array.append(0x01) # ext
			array.append(messages[i]["id"] & 0xFF)
			array.append((messages[i]["id"] >> 8) & 0xFF)
			array.append((messages[i]["id"] >> 16) & 0xFF)
			array.append((messages[i]["id"] >> 24) & 0x1F)
		
		# parse message data
                f = StringIO((messages[i]["data"]))
		rdr = csv.reader(f, delimiter=',')
                row1 = next(rdr)
		data_cnt = len(row1)
		if (data_cnt > 64):
			print("Message %d is too long" %i)
			return None
		array.append(data_cnt & 0xFF)	         		
		for ch in row1:
			array.append(int(ch, 16) & 0xFF)
	return array
#*************************************************************************
def deserialize_messages(rx_data):
	# message structure:
	#[0] -Start marker (0xC0)
	#[4 : 1] - time stamp
	#[5] - ID type (0 - std, 1 - extended)
	#[7 : 6] or [9 : 6] - ID
	#[] data count
	#[] payload
	rx_messages = []
	ind = 0
	current_message = 0
	while (ind < len(rx_data)):
		# check start marker
		if (rx_data[ind] != 0xC0):
			print "Corrupted header, message %d" %current_message
			return (0, rx_messages)
		ind += 1
		if ind >= len(rx_data):
	                print "Bad packet length"
			return (0, rx_messages)

		time_stamp = rx_data[ind] | (rx_data[ind + 1] << 8) | (rx_data[ind + 2] << 16) | (rx_data[ind + 3] << 24)
		ind += 4
		if ind >= len(rx_data):
	                print "Bad packet length"
			return (0, rx_messages)



		# type & id
		if (rx_data[ind] == 0):
			id_type = "std"
			mess_id = rx_data[ind + 1] | (rx_data[ind + 2] << 8)
			ind += 3

		else:
			if (rx_data[ind] == 1):
				id_type = "ext"
				mess_id = rx_data[ind + 1] | (rx_data[ind + 2] << 8)  | (rx_data[ind + 3] << 16)  | (rx_data[ind + 4] << 24)
				ind += 5
				
			else:
			    print "Wrong type,  message %d" %current_message
			    return (0, rx_messages)
		if ind >= len(rx_data):
	                print "Bad packet length"
			return (0, rx_messages)


		# payload len
		data_count = rx_data[ind]
		if (data_count > 64):
  			print "Wrong data length,  message %d" %current_message
			return (0, rx_messages)
		ind += 1

		# payload
		if (ind + data_count) > len(rx_data):
	                print "Bad packet length pl"
			return (0, rx_messages)


		payload = str()
		for i in range(0, data_count):
			payload += ''.join(format(rx_data[ind + i], '02X')) 
			if (i != data_count - 1):
				payload += " "
				

		ind += data_count
		
		current_message += 1
		rx_messages.append({'timestamp': time_stamp, 'type': id_type, "id": format(mess_id, '02X'), "data": payload})

	return (1, rx_messages)


#*************************************************************************
COM_PORT_ENG                = 'COM17'

#---- Application ---------------------------------------------------------
print "===================================="
print "* FDCAN sends messages from buffer, and receives messages to buffer"
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

TRX_TIMEOUT = 300
# compose messages
tx_messages = []  
tx_messages.append({'type': "ext", "id": 0x1FE, "data": "0x00,0x01, 0x02"})
tx_messages.append({'type': "ext", "id": 0x12345678, "data": "0xBE, 0xEF, 0xCA, 0xFE"})
tx_messages.append({'type': "ext", "id": 0x1F7, "data": "0x03,0x04, 0x05"})
tx_messages.append({'type': "ext", "id": 0x12345678, "data": "0xBE, 0xEF, 0xCA, 0xFE"})
tx_array = serialize_messages(tx_messages)
if (tx_array == None):
	sys.exit(0)

#use put_buffer to send messages to uC
if (put_buffer(ser, tx_array) == 0):
	sys.exit(0)

# send messages from buffer and wait for RX_TIMEOUT for received messages
wro = ser.write("fdcan buffer " + str(len(tx_messages)) + ", " + str(TRX_TIMEOUT) +"\r\n")

#wait for finish
done = 0;
rrd = str()
while (done == 0):
	rrd = ser.readline()
	if (rrd != ''):
		print(rrd)
		done = 1
	else:
		print('.')
#verify result
if (rrd.find("OK.", 0, 3) != -1):
	#parse for received bytes count
	bytes_str = rrd[3:]
	rx_cnt = int(bytes_str, 10)

	if (rx_cnt > 0):
		#read bytes with get_buffer command
		(status, rx_data) = get_buffer(ser, rx_cnt)

		print "get_buffer return status: %r" % status
		rx_buffer = bytearray(rx_cnt)
		rx_buffer[0 : rx_cnt] = rx_data

		#convert to tuples
		(status, rx_messages) = deserialize_messages(rx_buffer)
		if (status == 1):
			for messa in rx_messages:
				print messa
raw_input("Press Enter to exit ...")