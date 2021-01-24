#=====================================================
#  I2S functional test
#=====================================================
import os
import sys
import time
import serial
import select
from putbuffer import put_buffer
from getbuffer import get_buffer
import math
from usb2io import usb2io_sendcmd
import numpy as np
import matplotlib.pyplot as plt
import Tkinter, tkFileDialog


COM_PORT_ENG                = 'COM17'
data_cnt = 90 * 22000 * 2 # seconds * samples rate * chan count
save_to_txt = 0
draw_plot = 1
save_to_wav = 1



#---- Application ---------------------------------------------------------
print "===================================="
print "* I2S write read"
print "===================================="

local_com_port = sys.argv[1] if (len(sys.argv) > 1) else COM_PORT_ENG

# Open serial port
print "Open serial port " + local_com_port
try:
    ser = serial.Serial(local_com_port, 115200, timeout=10)
    print "COM port OK" 
except:
    print "Error COM port" 
    sys.exit(0)

print "Preparing data..." 
data = bytearray(data_cnt * 8)
for i in range(0, data_cnt):
	sR = int(0x40000000 + 0x40000000 * math.sin(2 * 3.14 * i/44))
	sL = int(0x40000000 + 0x40000000 * math.sin(2 * 3.14 * i/11))
	#sampleR = 0
	#sampleR = 0

	data[i * 8 ] = sR & 0xFF
	data[i * 8 + 1] = (sR >> 8) & 0xFF
	data[i * 8 + 2] = (sR >> 16) & 0xFF
	data[i * 8 + 3] = (sR >> 24) & 0xFF

	data[i * 8 + 4] = sL & 0xFF
	data[i * 8 + 5] = (sL >> 8) & 0xFF
	data[i * 8 + 6] = (sL >> 16) & 0xFF
	data[i * 8 + 7] = (sL >> 24) & 0xFF


# send to target
print("Sending buffer...")
print("len = " + str(len(data)))

if (put_buffer(ser, data) == 0):
	sys.exit(0)


print("Starting...")
usb2io_sendcmd(ser, "i2s wreadbuf 1, " + str(data_cnt) + "\r\n")
print("Busy...")
done = 0;
while (done == 0):
	rrd = ser.readline()
	if (rrd != ''):
		print(rrd)
	else:
		print('.')
	if (rrd == 'OK\r\n'):
		done = 1;


# get buffer
print("Reading...")
(status, data_out) = get_buffer(ser, data_cnt * 4)

print "get_buffer return status: %r" % status
#print data_out.encode("hex")

rx_data = bytearray(4 * data_cnt)
rx_data[0 : 4 * data_cnt] = data_out

sampleR = [0] * (data_cnt >> 1)
sampleL = [0] * (data_cnt >> 1)

for i in range(0, data_cnt >> 1):
	sampleR[i] = rx_data[i * 8] | (rx_data[i * 8 + 1] << 8) | (rx_data[i * 8 + 2] << 16) | (rx_data[i * 8 + 3] << 24);
	sampleR[i] ^= 0x80000000;
	#sampleR[i] = int(0x80000000 + 0x80000000 * math.sin(2 * 3.14 * i/samples_cnt))
	sampleL[i] = rx_data[i * 8 + 4] | (rx_data[i * 8 + 5] << 8) | (rx_data[i * 8 + 6] << 16) | (rx_data[i * 8 + 7] << 24);
	sampleL[i] ^= 0x80000000;

if (draw_plot == 1):
	fig, ax = plt.subplots()
	ax.plot(sampleR, label="R")
	ax.plot(sampleL, label="L")
	ax.legend()
	plt.show()
	plt.close()

if (save_to_txt == 1):
	#save to file
	print "Save results"
	root = Tkinter.Tk()
	root.withdraw()
        
	file_opt = options = {}
	options['defaultextension'] = '.txt'
	options['filetypes'] = [('all files', '.*'), ('txt files', '.txt')]
	options['title'] = 'Save results'
 

	file_path = tkFileDialog.asksaveasfilename(**file_opt)
	if (not file_path):
		print "no file selected"
            	sys.exit(0)                            

	f = open(file_path, 'wb')

	if (f == None):
		print "can not open file."
		sys.exit(0)                            

	for i in range(0, data_cnt >> 1):
		#print >> f, str(sampleL[i]) + " " + str(sampleR[i])
		print >> f, "0x{:08x}".format(sampleL[i]) + " " + "0x{:08x}".format(sampleR[i])


	f.close();

if (save_to_wav == 1):
	#save to file
	print "Save results"
	root = Tkinter.Tk()
	root.withdraw()
        
	file_opt = options = {}
	options['defaultextension'] = '.wav'
	options['filetypes'] = [('all files', '.*'), ('wav files', '.wav')]
	options['title'] = 'Save results'
 

	file_path = tkFileDialog.asksaveasfilename(**file_opt)
	if (not file_path):
		print "no file selected"
            	sys.exit(0)                            

	f = open(file_path, 'wb')

	if (f == None):
		print "can not open file."
		sys.exit(0)                            

	Nc = 2 # channels
	Ns = data_cnt >> 1 # blocks
	Fr = 21870 # sample rate
	M = 4 # bytes in sample

	data = bytearray(4)
	
	f.write("RIFF");

	val = 44;	
	data[0] = val & 0xFF
	data[1] = (val >> 8) & 0xFF
	data[2] = (val >> 16) & 0xFF
	data[3] = (val >> 24) & 0xFF
	f.write(data);

	f.write("WAVE");
	f.write("fmt ");

	val = 16;	
	data[0] = val & 0xFF
	data[1] = (val >> 8) & 0xFF
	data[2] = (val >> 16) & 0xFF
	data[3] = (val >> 24) & 0xFF
	f.write(data);
	
	val = 1 | (Nc << 16)
	data[0] = val & 0xFF
	data[1] = (val >> 8) & 0xFF
	data[2] = (val >> 16) & 0xFF
	data[3] = (val >> 24) & 0xFF
	f.write(data);   

	val = Fr
	data[0] = val & 0xFF
	data[1] = (val >> 8) & 0xFF
	data[2] = (val >> 16) & 0xFF
	data[3] = (val >> 24) & 0xFF
	f.write(data);   

	val = Fr * M * Nc
	data[0] = val & 0xFF
	data[1] = (val >> 8) & 0xFF
	data[2] = (val >> 16) & 0xFF
	data[3] = (val >> 24) & 0xFF
	f.write(data);   
        	
	val = (M * Nc) | ((8 * M) << 16)
	data[0] = val & 0xFF
	data[1] = (val >> 8) & 0xFF
	data[2] = (val >> 16) & 0xFF
	data[3] = (val >> 24) & 0xFF
	f.write(data);   	

	f.write("data");

	val = M * Nc * Ns
	data[0] = val & 0xFF
	data[1] = (val >> 8) & 0xFF
	data[2] = (val >> 16) & 0xFF
	data[3] = (val >> 24) & 0xFF
	f.write(data);   	

	for i in range(0, data_cnt >> 1):
		val =  sampleL[i] >> 1
		data[0] = val & 0xFF
		data[1] = (val >> 8) & 0xFF
		data[2] = (val >> 16) & 0xFF
		data[3] = (val >> 24) & 0xFF
		f.write(data);   	

		val =  sampleR[i] >> 1
		data[0] = val & 0xFF
		data[1] = (val >> 8) & 0xFF
		data[2] = (val >> 16) & 0xFF
		data[3] = (val >> 24) & 0xFF
		f.write(data);   	

	f.close();
raw_input("Press Enter to exit ...")