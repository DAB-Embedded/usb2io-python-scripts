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

# Set up microphone gain and power up the microphone power supply: MGAIN2-0 bits = 010 PMMP bit = 0-1
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x02, 0x0A\r\n")
#usb2io_sendcmd(ser, "i2c write 0x12, 0x02, 0x0C\r\n")

# Set up input signal
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x03, 0x00\r\n")   #in1 - mems

# Set up the Timer: OVTM1-0, OVFL, ADRST1-0 bits (Addr = 09H)
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x09, 0x09\r\n")  

#Set up ALC Mode, (Addr = 0AH, 0BH)
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x0A, 0x4C\r\n")
#usb2io_sendcmd(ser, "i2c write 0x12, 0x0B, 0x2D\r\n")
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x0B, 0x0D\r\n") # alc off

# Set up REF value of ALC (Addtr = 0CH)
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x0C, 0xE1\r\n")
#usb2io_sendcmd(ser, "i2c write 0x12, 0x0C, 0x5\r\n")

#Set up IVOL value of ALC (Addr = 0DH)
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x0D, 0x70\r\n")
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x0E, 0x70\r\n")

# Set up Programmable Filter ON/OFF (Addr = 1BH, 1CH, 30H)
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x1B, 0x05\r\n")
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x1C, 0x00\r\n")
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x30, 0x00\r\n")

# Set up Programmable Filter Path: PFSDO bit = ADCPF bit = 1 (Addr = 1DH)
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x1D, 0x03\r\n")

# Set up Coefficient of the Programmable Filter (Addr: 1EH ~ 2FH, 32H ~ 4FH)

#Power up the microphone, ADC and Programmable Filter, DAC, HP amp:
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x00, 0xc7\r\n")
usb2io_sendcmd(ser, "i2c write 1, 0x12, 0x01, 0x34\r\n") # PMPLL bit changes from 0-1







# Close serial port
ser.close()
raw_input("Press Enter to exit...") 

