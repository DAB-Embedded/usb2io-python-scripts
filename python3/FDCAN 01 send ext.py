#=====================================================
#  FDCAN send ext message
#=====================================================
import os
import sys
import time
import serial
import select
from usb2io import usb2io_sendcmd

COM_PORT_ENG                = 'COM17'

#---- Application ---------------------------------------------------------
print ("====================================")
print ("* FDCAN send ext message")
print ("====================================")

local_com_port = sys.argv[1] if (len(sys.argv) > 1) else COM_PORT_ENG

# Open serial port
print ("Open serial port " + local_com_port)
try:
    ser = serial.Serial(local_com_port, 115200, timeout=3)
    print ("COM port OK" )
except:
    print ("Error COM port" )
    sys.exit(0)

usb2io_sendcmd(ser, "fdcan send ext 0x1BAC1234,  10 , 11, 12, 13, 14, 15, 16, 17\r\n")

input("Press Enter to exit ...")
