#=====================================================
#  SPI functional test
#=====================================================
import os
import sys
import time
import serial
import select
from putbuffer import put_buffer
from usb2io import usb2io_sendcmd


COM_PORT_ENG                = 'COM17'

#wfg
segment_size = 4
sample_rate = 1000000
initial_state = 0
sync_mode = 0
cycle_mode = 0

#spi
packet_len = 4
packets_cnt = 3
trigger_timeout = 1000



#---- Application ---------------------------------------------------------
print "===================================="
print "* SPI writebuffer sync"
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

# pin 2..5 - SPI
print "Configure pins [2..5] to SPI mode"
usb2io_sendcmd(ser, "gpio configure 2,7\r\n")
usb2io_sendcmd(ser, "gpio configure 3,7\r\n")
usb2io_sendcmd(ser, "gpio configure 4,7\r\n")
usb2io_sendcmd(ser, "gpio configure 5,7\r\n")

print "Configure pin [0] to WFG mode"
usb2io_sendcmd(ser, "gpio configure 0,4\r\n")
    
# Set Ext voltage to 3.3V
print "Configure EXT voltage to 3.3V"
usb2io_sendcmd(ser, "expv write 3300\r\n")


print "Configure WFG"
# configure wfg
# the configuration should be sent to uC with put_buffer command. See description of "waveform gen configure" for config structure

data = bytearray(32 + segment_size * 2)

data[0] = sample_rate & 0xFF;     
data[1] = (sample_rate >> 8) & 0xFF;
data[2] = (sample_rate >> 16) & 0xFF;
data[3] = (sample_rate >> 24) & 0xFF;

data[4] = segment_size & 0xFF;     
data[5] = (segment_size >> 8) & 0xFF;
data[6] = (segment_size >> 16) & 0xFF;
data[7] = (segment_size >> 24) & 0xFF;

data[8] = (sync_mode & 0x03) | ((cycle_mode & 0x01) << 2)
data[9] = 0
data[10] = 0
data[11] = 0

data[12] = initial_state & 0xFF;     
data[13] = (initial_state >> 8) & 0xFF;
data[14] = 0
data[15] = 0

# reserved fields are 0 
    
#the waveform, bit[0] matters
data[32] = 0;
data[33] = 0;

data[34] = 0;
data[35] = 0;

data[36] = 1;
data[37] = 0;

data[38] = 1;
data[39] = 0;


# send to target
print("Sending buffer...")
if (put_buffer(ser, data) == 0):
	sys.exit(0)

print("Config wfg...")
wro = ser.write("waveform gen configure\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)

if (rrd != 'OK\r\n'):
	sys.exit(0)


print("Starting wfg...")
wro = ser.write("waveform gen start\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)

print "Configure trigger"
usb2io_sendcmd(ser, "trigger configure 1\r\n") 

#print "Configure SPI: Set 100KHz clock, Polarity low, CS active high, Phase 1st, MSB"
usb2io_sendcmd(ser, "spi configure 1,0,0,0,100000,0\r\n")



spidata = bytearray(packet_len * packets_cnt)
for i in range (0, packets_cnt * packet_len):
	spidata[i] = i + 1


# send to target
print("Sending buffer...")
print("len = " + str(len(data)))

if (put_buffer(ser, spidata) == 0):
	sys.exit(0)


	
usb2io_sendcmd(ser, "spi writebuffersync 1, " + str(packet_len) + ", " + str(packets_cnt) + ", " + str(trigger_timeout) + "\r\n") 
raw_input("Press Enter to exit ...")
