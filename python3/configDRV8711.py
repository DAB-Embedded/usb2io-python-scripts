"""@package docstring
config8711 module.

Module for receiving data from device over USB.
"""
import os
import sys
import time
import serial
import select
import zlib
import re
import string

# mode
#0: Full-step, 71% current
#1: Half step
#2: 1/4 step
#3: 1/8 step
#4: 1/16 step
#5: 1/32 step
#6: 1/64 step
#7: 1/128 step
#8: 1/256 step

def configDRV8711(ser, mode):
	print("Configuring 4 pins to spi repeater...")

	wro = ser.write("gpio configure 2, 7\r\n".encode('utf-8'))
	time.sleep(0.1)
	rrd = ser.readline()
	print(rrd)

	wro = ser.write("gpio configure 3, 7\r\n".encode('utf-8'))
	time.sleep(0.1)
	rrd = ser.readline()
	print(rrd)

	wro = ser.write("gpio configure 4, 7\r\n".encode('utf-8'))
	time.sleep(0.1)
	rrd = ser.readline()
	print(rrd)

	wro = ser.write("gpio configure 5, 7\r\n".encode('utf-8'))
	time.sleep(0.1)
	rrd = ser.readline()
	print(rrd)

	# config spi
	wro = ser.write("spi configure 1, 1, 0, 0, 100000, 0\r\n".encode('utf-8'))
	time.sleep(0.1)
	rrd = ser.readline()
	print(rrd)

	#init registers
	#DRV8711_CTRL	F21
	controlReg = 0x0F00 | ((mode & 0x0F) << 3) ;
	txc = "spi write 1, 0x0F, " + str(controlReg & 0xFF) + "\r\n"
	wro = ser.write(txc.encode('utf-8'))
	time.sleep(0.1)
	rrd = ser.readline()
	print(rrd)


	#DRV8711_TORQUE	17B
	wro = ser.write("spi write 1, 0x11, 0x7B\r\n".encode('utf-8'))
	time.sleep(0.1)
	rrd = ser.readline()
	print(rrd)

	#DRV8711_OFF	000
	wro = ser.write("spi write 1, 0x20, 0x00\r\n".encode('utf-8'))
	time.sleep(0.1)
	rrd = ser.readline()
	print(rrd)

	#DRV8711_BLANK	000
	wro = ser.write("spi write 1, 0x30, 0x00\r\n".encode('utf-8'))
	time.sleep(0.1)
	rrd = ser.readline()
	print(rrd)

	#DRV8711_DECAY	000
	wro = ser.write("spi write 1, 0x40, 0x00\r\n".encode('utf-8'))
	time.sleep(0.1)
	rrd = ser.readline()
	print(rrd)

	#DRV8711_STALL	83C
	wro = ser.write("spi write 1, 0x58, 0x3C\r\n".encode('utf-8'))
	time.sleep(0.1)
	rrd = ser.readline()
	print(rrd)

	#DRV8711_DRIVE	0F0
	wro = ser.write("spi write 1, 0x60, 0xF0\r\n".encode('utf-8'))
	time.sleep(0.1)
	rrd = ser.readline()
	print(rrd)

	#DRV8711_STATUS	000
	wro = ser.write("spi write 1, 0x70, 0x00\r\n".encode('utf-8'))
	time.sleep(0.1)
	rrd = ser.readline()
	print(rrd)


	return (True)

def setCurrentDRV8711(ser, current):
	risense = 0.033
	vref = 2.75
	isgain = 40
	torque_f = current * 256 * isgain * risense / vref;
	torque_i = int(torque_f)
	txc = "spi write 1, 0x11, " + str(torque_i & 0xFF) + "\r\n"
	wro = ser.write(txc.encode('utf-8'))
	time.sleep(0.1)
	rrd = ser.readline()
	print(rrd)

	return (True)

def disableDRV8711(ser):

	#read current value of reg 0
	wro = ser.write("spi wread 1, 0x80, 0x00\r\n".encode('utf-8'))
	time.sleep(0.05)
	rrd = ser.readline()
	print (rrd)


	pat = re.compile("[,\r]")
	fields = pat.split(rrd)

	a = int(fields[1], 16)
	b = int(fields[2], 16)

	# write back with cleared LSB
	a &= 0x0F;
	b &= 0xFE;

	txc = "spi write 1, " + str(a) + ", "  + str(b) + "\r\n"
	wro = ser.write(txc.encode('utf-8'))
	time.sleep(0.1)
	rrd = ser.readline()
	print(rrd)

def enableDRV8711(ser):

	#read current value of reg 0
	wro = ser.write("spi wread 1, 0x80, 0x00\r\n".encode('utf-8'))
	time.sleep(0.05)
	rrd = ser.readline().decode("utf-8")
	print (rrd)

	ba1 = [int(i,16) for i in rrd.replace('OK,', '').split(',')]

	a = ba1[0]
	b = ba1[1]

	# write back with cleared LSB
	a &= 0x0F;
	b |= 0x01;

	txc = "spi write 1, " + str(a) + ", "  + str(b) + "\r\n"
	wro = ser.write(txc.encode('utf-8'))
	time.sleep(0.1)
	rrd = ser.readline()
	print(rrd)
