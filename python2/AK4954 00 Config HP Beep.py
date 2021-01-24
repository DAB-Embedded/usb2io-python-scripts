#=====================================================
#  AK4954 Config
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
usb2io_sendcmd(ser, "i2s configure 1, 1, 3, 3, 1, 0, 0, 1 \r\n")


#print "Scan I2C bus"
#usb2io_sendcmd(ser, "i2c scan\r\n")
# dummy
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x00, 0x00\r\n", 1)
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x00, 0x00\r\n", 1)

#PLL Slave Mode (BICK pin)

usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x05, 0x1F\r\n") # 32 MSB mode , PLL ref = Bick 64fs
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x06, 0x05\r\n") # 22 KHz

usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x00, 0x40\r\n") # Power Up VCOM: PMVCM bit = 0  -  1

usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x01, 0x04\r\n") # PMPLL bit changes from 0-1

# now pll should be locked

#Beep Signal Output from Headphone Amplifier
#HPZ = 0
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x12, 0x00\r\n")

#Set up BEEP Generator (Addr: 15H ~ 19H) (When repeat output time: BPCNT bit = 0)
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x15, 0x02\r\n") # 1.3 KHz, 3 times
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x16, 0x1F\r\n") # beep on time
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x17, 0x1F\r\n") # beep off time
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x18, 0x02\r\n") # beep repeat count
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x19, 0x00\r\n") # beep volume 0 dB

#Power up Headphone Amplifier: PMHPL bit or PMHPR bit = 0-1
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x01, 0x34\r\n")

#Power up BEEP-Generator: PMBP bit = 0-1
#Charge pump circuit is powered-up. The power-up time of Headphone Amplifier block is 30ms (max).
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x00, 0x60\r\n") # Power Up VCOM: PMVCM bit = 0-1


#(4) BEEP output: BPOUT bit= 0-1
#After outputting data particular set times, BPOUT bit automatically goes to 0
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x19, 0x80\r\n") 


# Close serial port
ser.close()
raw_input("Press Enter to exit...") 

