#=====================================================
#  AK4954 Config
#  
#
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
print "* AK4954 Config"
print "===================================="

local_com_port = COM_PORT_ENG

# Open serial port
print "Open serial port " + local_com_port
try:
    ser = serial.Serial(local_com_port, 115200, timeout=3)
    print "COM port OK" 
except:
    print "Error COM port" 
    sys.exit(0)

usb2io_sendcmd(ser, "hello\r\n")

# physical connection (USB2IO pin - AK4954 pin)
# 1-8
# 3-10
# 4-11
# 5-12
# 6-13
# 17-7
# 18-9
# 19-18
# 20-1

print "Configure I2C"
usb2io_sendcmd(ser, "i2c configure 0\r\n")

print("Configuring 4 pins to spi repeater...")

usb2io_sendcmd(ser, "gpio configure 2, 7\r\n")
usb2io_sendcmd(ser, "gpio configure 3, 7\r\n")
usb2io_sendcmd(ser, "gpio configure 4, 7\r\n")
usb2io_sendcmd(ser, "gpio configure 5, 7\r\n")

print("Configuring pin 0 as reset")
# reset lo
usb2io_sendcmd(ser, "gpio configure 0, 1\r\n")
usb2io_sendcmd(ser, "gpio configure 0, 2\r\n")

print("Configuring I2S unit...")

# chan = 2
# Audio standard =   I2S_STANDARD_MSB (1)
# Data format = I2S_DATAFORMAT_32B(3)
# Audio frequency = 22K (3)
# Clock polarity = 0
# First bit = MSB (0)
# FrameSync inversion = DISABLE (0)
# 24bit frame alignment = LEFT (1)
usb2io_sendcmd(ser, "i2s configure 1, 1, 3, 3, 0, 0, 0, 1 \r\n")


#print "Scan I2C bus"
#usb2io_sendcmd(ser, "i2c scan\r\n")
# dummy
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x00, 0x00\r\n", 1)
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x00, 0x00\r\n", 1)

#PLL Slave Mode (BICK pin)

usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x05, 0x1E\r\n") # 32 MSB mode , PLL ref = Bick 64fs
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x06, 0x05\r\n") # 22 KHz

usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x00, 0x40\r\n") # Power Up VCOM: PMVCM bit = 0  -  1

usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x01, 0x04\r\n") # PMPLL bit changes from 0-1

# now pll should be locked


# Set up the digital output volume
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x13, 0x0C\r\n")

#Set up Programmable Filter Path: PFDAC, ADCPF and PFSDO bits (Addr = 1DH)
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x1D, 0x03\r\n")

#Power up DAC and Headphone Amplifier: 
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x00, 0x44\r\n") # PMPLL bit changes from 0-1
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x01, 0x34\r\n") # PMPLL bit changes from 0-1

# Close serial port
ser.close()
raw_input("Press Enter to exit...") 

