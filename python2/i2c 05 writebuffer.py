#=====================================================
#  I2C functional test
#=====================================================
import os
import sys
import time
import serial
import select
from putbuffer import put_buffer
from usb2io import usb2io_sendcmd


COM_PORT_ENG                = 'COM17'
packet_len = 3
packets_cnt = 15
# port select. 1 - stm32, 2 - fpga
port = 1
#---- Application ---------------------------------------------------------
print "===================================="
print "* I2C writebuffer"
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

data = bytearray(packet_len * packets_cnt)
ind = 0

data[ind : ind + packet_len] = bytearray(b'\x12\x00\x00')
ind += packet_len

data[ind : ind + packet_len] = bytearray(b'\x12\x00\x00')
ind += packet_len

data[ind : ind + packet_len] = bytearray(b'\x12\x05\x1F')
ind += packet_len

data[ind : ind + packet_len] = bytearray(b'\x12\x06\x05')
ind += packet_len

data[ind : ind + packet_len] = bytearray(b'\x12\x00\x40')
ind += packet_len

data[ind : ind + packet_len] = bytearray(b'\x12\x01\x04')
ind += packet_len

data[ind : ind + packet_len] = bytearray(b'\x12\x12\x00')
ind += packet_len

data[ind : ind + packet_len] = bytearray(b'\x12\x15\x02')
ind += packet_len

data[ind : ind + packet_len] = bytearray(b'\x12\x16\x1F')
ind += packet_len

data[ind : ind + packet_len] = bytearray(b'\x12\x17\x1F')
ind += packet_len

data[ind : ind + packet_len] = bytearray(b'\x12\x18\x02')
ind += packet_len

data[ind : ind + packet_len] = bytearray(b'\x12\x19\x00')
ind += packet_len

data[ind : ind + packet_len] = bytearray(b'\x12\x01\x34')
ind += packet_len

data[ind : ind + packet_len] = bytearray(b'\x12\x00\x60')
ind += packet_len

data[ind : ind + packet_len] = bytearray(b'\x12\x19\x80')
ind += packet_len


# send to target
print("Sending buffer...")
print("len = " + str(len(data)))

if (put_buffer(ser, data) == 0):
	sys.exit(0)

usb2io_sendcmd(ser, "i2c writebuffer " + str(port) + ", "+ str(packet_len) + ", " + str(packets_cnt) + "\r\n") 
raw_input("Press Enter to exit ...")