#=====================================================
#  WFG functional test
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
print "* WFG test"
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

print("Configuring All to WFG...")
wro = ser.write("gpio configure 255, 4\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)

# configure wfg
# the configuration should be sent to uC with put_buffer command. See description of "waveform gen configure" for config structure
segment_size = 10000
sample_rate = 5
initial_state = 0
sync_mode = 0
cycle_mode = 0

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
    
#the waveform
for i in range(0, segment_size):
	#lower 8 bits are counter 
	data[32 + i * 2] = (i & 0xFF)

	#higher 8 bits will be filled later, so far they are 1
        data[32 + i * 2 + 1] = 0xFF

#add pulses to higher bits
data[33] = 0x00
data[35] = 0x01
data[37] = 0x03
data[39] = 0x07
data[41] = 0x0F
data[43] = 0x1F
data[45] = 0x3F
data[47] = 0x7F

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

print "Done\n\r"
raw_input("Press Enter to exit...")