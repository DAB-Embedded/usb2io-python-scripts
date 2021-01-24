#=====================================================
#  LTC2500 start
#  
#
#=====================================================
import os
import sys
import time
import serial
import select
from usb2io import usb2io_sendcmd
from getbuffer import get_buffer
import matplotlib.pyplot as plt

COM_PORT_ENG                = 'COM17'

#---- Application ---------------------------------------------------------
print "===================================="
print "* LTC2500 start"
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


print("starting LTC2500...")


sample_rate = 1000 # nanoseconds
data_count = 10
trig_mode = 0 # 0 - sw, 1 - extR, 2 - extF


if (usb2io_sendcmd(ser, "ltc2500 start capture " + str(sample_rate) + ", " + str(data_count) + ", " + str(trig_mode) + "\r\n", 1) != "OK\r\n"):
	print "failed."
	sys.exit(0)

#wait until ready
print("waiting for completion...")
ready = 0
while (ready == 0):
	result = usb2io_sendcmd(ser, "ltc2500 getready\r\n", 1)
	print "..." + result
	if (result == "READY\r\n"):
		ready = 1
	else:
		if (result == "BUSY\r\n"):
			time.sleep(1)	
		else:
			print "failed."
			sys.exit(0)

print("getting results...")
# get results
if (usb2io_sendcmd(ser, "ltc2500 getdata\r\n", 1 ) != "OK\r\n"):
	print "failed."
	sys.exit(0)

#use get_buffer

(status, data_out) = get_buffer(ser, data_count * 4)

print "Done."

data = bytearray(data_count * 4) 
data[0 : data_count * 4] = data_out
samples = [0] * data_count

for i in range(0, data_count):
	samples[i] = data[i * 4] | (data[i * 4 + 1] << 8) | (data[i * 4 + 2] << 16) | (data[i * 4 + 3] << 24);

fig, ax = plt.subplots()
ax.plot(samples, label="adc codes")
ax.legend()
plt.show()
plt.close()

	
	





raw_input("Press Enter to exit ...")