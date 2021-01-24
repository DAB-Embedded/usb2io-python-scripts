#=====================================================
#  Timer5 pwm
#=====================================================
import os
import sys
import time
import serial
import select
from usb2io import usb2io_sendcmd

COM_PORT_ENG                = 'COM17'
channel = 1
frequency = 10000
duty_cycle = 80

#---- Application ---------------------------------------------------------
print "===================================="
print "* Tim5 PWM start"
print "* pin connection:"
print "* GPIO 12 - channel 1"
print "* GPIO 13 - channel 2"
print "* GPIO 14 - channel 3"
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

# Configure gpio
print "gpio config..."
usb2io_sendcmd(ser, "gpio configure 12, 14\r\n")
usb2io_sendcmd(ser, "gpio configure 13, 14\r\n")
usb2io_sendcmd(ser, "gpio configure 14, 14\r\n")


print "starting pwm..."                            
#format: tim5 pwm start a, b, c
# a = channel
# b = frequency
# c = duty_cycle
usb2io_sendcmd(ser, "tim5 pwm start " + str(channel) + ", " + str(frequency) + ", " + str(duty_cycle) + "\r\n") 

raw_input("Press Enter to exit ...")