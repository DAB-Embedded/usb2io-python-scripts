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
CANFD_TIMEOUT               = 20000 #In MS

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

print("Waiting for CAN frames for %d seconds" % (CANFD_TIMEOUT/1000))

tx_str = "fdcan recv single timeout " + str(CANFD_TIMEOUT) + "\r\n"
wro = ser.write(tx_str.encode('utf-8'))

done = 0
inx_rx = 0
while (done == 0):
    rrd = ser.readline().decode("utf-8")
    if (rrd != ''):
        if (rrd.find("DONE") == 0):
            done = 1
            print('Done')
        else:
            inx_rx = inx_rx + 1
            print("[INX%d] %s" % (inx_rx, rrd))
    else:
        print('.')

input("Press Enter to exit ...")
