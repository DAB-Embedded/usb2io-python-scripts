#=====================================================
# FDCAN recv signle message
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
print ("* FDCAN recv signle message")
print ("====================================")

local_com_port = sys.argv[1] if (len(sys.argv) > 1) else COM_PORT_ENG

# Open serial port
print ("Open serial port " + local_com_port)
try:
    ser = serial.Serial(local_com_port, 115200, timeout=3)
    print ("COM port OK")
except:
    print ("Error COM port")
    sys.exit(0)

c_time = time.time() * 1000.
while(1):
    rx_out = usb2io_sendcmd(ser, "fdcan recv single\r\n", 1)
    d_time = (time.time() * 1000.) - c_time
    c_time = time.time() * 1000.
    print("[%f] %s "% (d_time, rx_out))

input("Press Enter to exit ...")
