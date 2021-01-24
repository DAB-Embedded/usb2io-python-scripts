#=====================================================
# send \ receive messages over FDCAN 
#=====================================================
import os
import io
import sys
import time
import serial
import select
from putbuffer import put_buffer
from getbuffer import get_buffer
from usb2io import usb2io_sendcmd
import csv

#*************************************************************************
def serialize_messages(messages):
    # byte array should have following structure:
    # 0xC0 - start marker
    # 0x00 or 0x01 - type (0 - std, 1 - extended)
    # ID - identifier. 2 bytes for std, 4 bytes for ext
    # NN - data count
    # DT - payload
    array = bytearray()
    for i in range(len(messages)):
        array.append(0xC0)
        if (messages[i]["type"] == "std"):
            array.append(0x00)
            array.append(messages[i]["id"] & 0xFF)
            array.append((messages[i]["id"] >> 8) & 0x07)
        else:
            array.append(0x01) # ext
            array.append(messages[i]["id"] & 0xFF)
            array.append((messages[i]["id"] >> 8) & 0xFF)
            array.append((messages[i]["id"] >> 16) & 0xFF)
            array.append((messages[i]["id"] >> 24) & 0x1F)
        # parse message data
        f = io.StringIO((messages[i]["data"]))
        rdr = csv.reader(f, delimiter=',')
        row1 = next(rdr)
        data_cnt = len(row1)
        if (data_cnt > 64):
            print("Message %d is too long" %i)
            return None
        array.append(data_cnt & 0xFF)
        for ch in row1:
            array.append(int(ch, 16) & 0xFF)
    return array


#*************************************************************************
COM_PORT_ENG                = 'COM17'

#wfg   - 1Hz @ gpio[0]
segment_size = 20
sample_rate = 50000000
initial_state = 0
sync_mode = 0
cycle_mode = 0

# can
packet_size = 2
packets_count = 2
trigger_timeout = 10000
#---- Application ---------------------------------------------------------
print "===================================="
print "* FDCAN sends messages from buffer in sync packets"
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

TRX_TIMEOUT = 300

print "Configure pin [0] to WFG mode"
usb2io_sendcmd(ser, "gpio configure 0,4\r\n")
    

print ("Configure WFG")
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

for i in range (4, segment_size):
    data[40 + i] = 0;

# send to target
print("Sending buffer...")
if (put_buffer(ser, data) == 0):
    sys.exit(0)

print("Config wfg...")
rrd = usb2io_sendcmd(ser, "waveform gen configure\r\n")

if (rrd != 'OK\r\n'):
    sys.exit(0)


print("Starting wfg...")
wro = ser.write("waveform gen start\r\n")
time.sleep(0.1)
rrd = ser.readline()
print(rrd)

print "Configure trigger"
usb2io_sendcmd(ser, "trigger configure 1\r\n") 



# compose messages
tx_messages = []  
tx_messages.append({'type': "ext", "id": 0x1FE, "data": "0x00,0x01, 0x02"})
tx_messages.append({'type': "ext", "id": 0x12345678, "data": "0xBE, 0xEF, 0xCA, 0xFE"})
tx_messages.append({'type': "ext", "id": 0x1F7, "data": "0x03,0x04, 0x05"})
tx_messages.append({'type': "ext", "id": 0x12345679, "data": "0xBE, 0xEF, 0xCA, 0xFE"})
tx_array = serialize_messages(tx_messages)
if (tx_array == None):
    sys.exit(0)

#use put_buffer to send messages to uC
if (put_buffer(ser, tx_array) == 0):
    sys.exit(0)

# send messages from buffer and wait for RX_TIMEOUT for received messages
tx_str = "fdcan writebuffersync " + str(packet_size) + ", "  + str(packets_count) + ", "+ str(trigger_timeout) +"\r\n"
wro = ser.write(tx_str.encode('utf-8'))

#wait for finish
done = 0;
rrd = str()
while (done == 0):
    rrd = ser.readline()
    if (rrd != ''):
        print(rrd)
        done = 1
    else:
        print('.')
input("Press Enter to exit ...")