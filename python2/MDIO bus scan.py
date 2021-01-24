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

phy_found = 0
phy_addr_found = 32
# Looking for valid PHY
for addr in range(0, 31):
    # Read reg 2 (ID), if not 0xFFFF - valid PHY
    str_tx = "mdio read " + hex(addr) + ",0x2\r\n"
    regv = usb2io_sendcmd(ser, str_tx, silent = 1)
    regvc = regv.replace('OK,','').replace('\r\n','')
    temp_val = int(regvc, 16)
    if (temp_val != 0xFFFF):
        phy_found = 1
        phy_addr_found = addr
        print("PHY found at addres: " + str(addr))
        break

if (phy_found):
    print("List PHY (address " + str(phy_addr_found) + ") registers")
    for regi in range(0, 15):
        str_tx = "mdio read " + hex(phy_addr_found) + "," + hex(regi) + "\r\n"
        regv = usb2io_sendcmd(ser, str_tx, silent = 1)
        regvc = regv.replace('OK,','').replace('\r\n','')
        temp_val = int(regvc, 16)
        print("PHY ID%02d, register %02d : %04x" %(phy_addr_found, regi, temp_val))

# Close serial port
ser.close()
print("API test done")
