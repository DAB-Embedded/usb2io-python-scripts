import os
import sys
import time
import serial
import select
import ctypes as ct
from usb2io import usb2io_sendcmd

COM_PORT_ENG                = 'COM132'

#---- Application ---------------------------------------------------------

local_com_port = sys.argv[1] if (len(sys.argv) > 1) else COM_PORT_ENG

# Open serial port
print("Open serial port " + local_com_port)
try:
    ser = serial.Serial(local_com_port, 115200, timeout=3)
    print("COM port OK")
except:
    print("Error COM port")
    sys.exit(0)

usb2io_sendcmd(ser, "hello\r\n")

# Set MDIO pinmux
usb2io_sendcmd(ser, "gpio configure 2, 11\r\n", silent = 1)
usb2io_sendcmd(ser, "gpio configure 3, 11\r\n", silent = 1)

# Set Ext voltage to 2.5V
usb2io_sendcmd(ser, "expv write 2500\r\n", silent = 1)

# Reset PHY and start autonegotiation
usb2io_sendcmd(ser, "mdio write 1,0,0x9200\r\n", silent = 1)

# Close serial port
ser.close()
print("MDIO test done")
