#=====================================================
#  XAP DAC Config 
#=====================================================
import os
import sys
import time
import serial
import select
from putbuffer import put_buffer

COM_PORT_ENG                = 'COM17'

#---- Application ---------------------------------------------------------
print "===================================="
print "* XAP DAC config saw"
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


wro = ser.write("hello\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)

# physical connection (USB2IO pin - DAC pcb JP2 pin)
# 3 - 3
# 5 - 1
# 6 - 4
# 1 - 2
# 20 - 5
  
print("Configuring 3 pins to SPI Master...")

wro = ser.write("gpio configure 2, 10\r\n")
time.sleep(0.1)
rrd = ser.readline()
if (rrd != 'OK\r\n'):
	print(rrd)


wro = ser.write("gpio configure 4, 10\r\n")
time.sleep(0.1)
rrd = ser.readline()
if (rrd != 'OK\r\n'):
	print(rrd)


wro = ser.write("gpio configure 5, 10\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)

print("Configuring pin 0 as LDAC...")
#LDAC = 0
wro = ser.write("gpio configure 0, 1\r\n")
time.sleep(0.1)
rrd = ser.readline()
if (rrd != 'OK\r\n'):
	print(rrd)


# configure spi master
# the configuration should be sent to uC with put_buffer command. See description of "spimaster configure" for config structure
sclk_period = 40
spi_rate = 1000
cycle_mode = 1
stop_when_empty = 0
bit_count = 16
sclk_polarity = 0
data_cnt = 10

data = bytearray(32 + data_cnt * 2)

data[0] = sclk_period & 0xFF     
data[1] = (sclk_period >> 8) & 0xFF
data[2] = (sclk_period >> 16) & 0xFF
data[3] = (sclk_period >> 24) & 0xFF

data[4] = spi_rate & 0xFF     
data[5] = (spi_rate >> 8) & 0xFF
data[6] = (spi_rate >> 16) & 0xFF
data[7] = (spi_rate >> 24) & 0xFF

data[8] = (cycle_mode & 0x01) | ((stop_when_empty & 0x01) << 1)
data[9] = (bit_count & 0x1F) | ((sclk_polarity & 0x01) << 7)
data[10] = 0
data[11] = 0

data[12] = data_cnt & 0xFF     
data[13] = (data_cnt >> 8) & 0xFF
data[14] = (data_cnt >> 16) & 0xFF
data[15] = (data_cnt >> 24) & 0xFF


# reserved fields are 0 
    
#the data
step = 16384 // data_cnt
for i in range(0, data_cnt):
	sample = i * step;
	if (sample > 16383):
		sample = 16383
	data[32 + i * 2] = sample & 0xFF
	data[32 + i * 2 + 1] = ((sample >> 8) & 0xFF) | 0xC0

# send to target
print("Sending buffer...")
if (put_buffer(ser, data) == 0):
	sys.exit(0)

print("Config spimaster...")
wro = ser.write("spimaster configure\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)

if (rrd != 'OK\r\n'):
	sys.exit(0)

print "Done\n\r"
raw_input("Press Enter to exit...")