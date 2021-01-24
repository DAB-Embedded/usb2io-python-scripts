#=====================================================
#  Step motor controller config
#=====================================================
import os
import sys
import time
import serial
import select
from configDRV8711 import configDRV8711
from usb2io import usb2io_sendcmd

COM_PORT_ENG                = 'COM17'

#---- Application ---------------------------------------------------------
print "===================================="
print "* Step motor controller config"
print "* pin connection to DRV8711 EVM:"
print "* GPIO 0 - Step channel 1"
print "* GPIO 1 - Dir channel 1"
print "* GPIO 2 - SPI CS"
print "* GPIO 3 - SPI MISO"
print "* GPIO 4 - SPI SCK"
print "* GPIO 5 - SPI MOSI"
print "* GPIO 6 - Sleep = 1"
print "* GPIO 14 - Step channel 2"
print "* GPIO 15 - Dir channel 2"

print "* DRV8711EVB J2 A+ = Black"
print "* DRV8711EVB J2 A- = Green"
print "* DRV8711EVB J2 B+ = Red"
print "* DRV8711EVB J2 B- = Blue"
print "* DRV8711EVB using motor ACT-Motor 23HS8430, Vsupply = 12V, 5Amax"
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


usb2io_sendcmd(ser, "hello\r\n")

print("Configuring 4 pins to step motor controller...")

if usb2io_sendcmd(ser, "gpio configure 0, 13\r\n") != "OK\r\n":
	print "failed."
	sys.exit(0)


if usb2io_sendcmd(ser, "gpio configure 1, 13\r\n") != "OK\r\n":
	print "failed."
	sys.exit(0)

if usb2io_sendcmd(ser, "gpio configure 14, 16\r\n") != "OK\r\n":
	print "failed."
	sys.exit(0)

if usb2io_sendcmd(ser, "gpio configure 15, 16\r\n") != "OK\r\n":
	print "failed."
	sys.exit(0)

# Sleep = 1
if usb2io_sendcmd(ser, "gpio configure 6, 2\r\n") != "OK\r\n":
	print "failed."
	sys.exit(0)

mode = 3
configDRV8711(ser, mode)

min_speed_ch1 = "1000"
max_speed_ch1 = "7000"
acceleration_ch1 = "2000"
steps_count_ch1 = "80000"
direction_ch1 = "1"

print("Configuring cntroller 1...")

if usb2io_sendcmd(ser, "stepmotor configure 1, " + min_speed_ch1 + "," + max_speed_ch1 + "," + acceleration_ch1 + "," + steps_count_ch1 + "," +  direction_ch1 + "\r\n") != "OK\r\n":
	print "failed."
	sys.exit(0)

min_speed_ch2 = "1000"
max_speed_ch2 = "7000"
acceleration_ch2 = "2000"
steps_count_ch2 = "80000"
direction_ch2 = "1"

print("Configuring cntroller 2...")

if usb2io_sendcmd(ser, "stepmotor configure 2, " + min_speed_ch2 + "," + max_speed_ch2 + "," + acceleration_ch2 + "," + steps_count_ch2 + "," +  direction_ch2 + "\r\n") != "OK\r\n":
	print "failed."
	sys.exit(0)

# controller parameters

raw_input("Press Enter to exit ...")