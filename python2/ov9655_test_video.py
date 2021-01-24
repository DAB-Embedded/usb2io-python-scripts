#=====================================================
#  OV9655 video stream test
#  
#
#=====================================================
import os
import sys
import time
import serial
import select
import struct
import zlib
import binascii
import rawx.base
import rawx.const
import rawx.error
import rawx.tools
import rawx.protocol.rawxt
import numpy as np
import math
import cv2

from PIL import Image
from numpy import array
from rawx.protocol.rawxt import *
from getbuffer import get_buffer_fast


COM_PORT_ENG                = 'COM17'
fpga_filename               = "fpga_waveform.rbf"
allow_load_fpga             = 0
opencv2_show                = 1
store_to_bin_file           = 0

#---- Application ---------------------------------------------------------
print "===================================="
print "* OV9655 video stream test"
print "===================================="

local_com_port = sys.argv[1] if (len(sys.argv) > 1) else COM_PORT_ENG

def ov9655_reg_write(ser, reg, value):
	strx = "i2c write 1, 0x30," + hex(reg & 0xFF) + "," + hex(value & 0xFF) + "\r\n"
	wro = ser.write(strx)
	time.sleep(0.05)
	rrd = ser.readline()

def ov9655_reg_read(ser, reg):
	strx = "i2c write 1, 0x30," + hex(reg & 0xFF) + "\r\n"
	wro = ser.write(strx)
	rrd = ser.readline()
	strx = "i2c read 1, 0x30,1\r\n"
	wro = ser.write(strx)
	rrd = ser.readline()
	print (rrd)
    
def usb2io_command(ser, command):
	ser.write(command)
	time.sleep(0.05)
	rrd = ser.readline()
	print (rrd)

def usb2io_command_noresp(ser, command):
	ser.write(command)
	time.sleep(0.05)
	ser.readline()

# Open serial port
print "Open serial port " + local_com_port
try:
    ser = serial.Serial(local_com_port, 115200, timeout=3)
    print "COM port OK" 
except:
    print "Error COM port" 
    sys.exit(0)

# Hello command
#wro = ser.write("hello\r\n")
#time.sleep(0.1)
#rrd = ser.readline()
#print(rrd)

# Scan I2C bus
print "Scan I2C bus"
wro = ser.write("i2c scan\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)

print "Get OV9655 ID"
ov9655_reg_read(ser, 0x0A)
ov9655_reg_read(ser, 0x0B)

#for x in range(0, 0x80):
#    print hex(x) + " reg:"
#    ov9655_reg_read(ser, x)

time.sleep(0.5)

width      = 800 * 2
height     = (240 + 8)
width_pix  = width/2
height_pix = height

if opencv2_show :
    array_cv2 = np.zeros([height_pix, width_pix, 3], dtype=np.uint8)
    while 1:
        (status, data_out) = get_buffer_fast(ser, width*height)
        bav = bytearray(data_out)
        #print "get_buffer return status: %r" % status
        #print "get_buffer return size: %d" %  len(bav)
        # img_array = np.frombuffer(bytearray(bav), dtype=np.uint16)
        #im = np.reshape(img_array, (-1, width_pix))
        index = 0
        for y in range (0,height_pix):
            for x in range (0,width_pix):
                #invert byte order
                pixel = (bav[index] << 8) | (bav[index + 1])
                index += 2
                # Extract pixels
                array_cv2[y,x,0] = (pixel&0b0000000000011111) << 3 #Blue channel 
                array_cv2[y,x,1] = (pixel&0b0000011111100000) >> 3 #Green channel 
                array_cv2[y,x,2] = pixel >> 8 #Red channel 
        #vis2 = cv2.cvtColor(a, cv2.COLOR_BGR5652RGB)
        cv2.imshow('USB2IO Video', array_cv2 )
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == 27:
            break
    cv2.destroyAllWindows()             

if store_to_bin_file :
    (status, data_out) = get_buffer_fast(ser, width*height)
    frawfile = open("dump.raw", 'wb') 
    frawfile.write(data_out) 
    frawfile.close() 


# Stop camera
#print "Stop camera capture"
#usb2io_command(ser, "camera stop\r\n")

# Close serial port
ser.close()
print "Port closed" 
