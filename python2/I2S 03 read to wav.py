#=====================================================
#  I2S functional test
#=====================================================
import os
import sys
import time
import serial
import select
import math
from putbuffer import put_buffer
from getbuffer import get_buffer
import numpy as np
import matplotlib.pyplot as plt
import Tkinter, tkFileDialog


COM_PORT_ENG                = 'COM17'
samples_cnt = 3 * 22000; # for both channels
save_to_file = 1
draw_plot = 1


#---- Application ---------------------------------------------------------
print "===================================="
print "* I2S read"
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

print("Requesting data...")


wro = ser.write("i2s readbuf 1, " + str(samples_cnt * 2) + "\r\n")
time.sleep(0.1)
rrd = ser.readline()
#if (rrd != 'OK\r\n'):
print(rrd)
#	sys.exit(0)                            
 
# get buffer
(status, data_out) = get_buffer(ser, samples_cnt * 8)

print "get_buffer return status: %r" % status
#print data_out.encode("hex")

data = bytearray(8 * samples_cnt)
data[0 : 8 * samples_cnt] = data_out

sampleR = [0] * samples_cnt
sampleL = [0] * samples_cnt


for i in range(0, samples_cnt):
	sampleR[i] = data[i * 8] | (data[i * 8 + 1] << 8) | (data[i * 8 + 2] << 16) | (data[i * 8 + 3] << 24);
	sampleR[i] ^= 0x80000000;
	sampleL[i] = data[i * 8 + 4] | (data[i * 8 + 5] << 8) | (data[i * 8 + 6] << 16) | (data[i * 8 + 7] << 24);
	sampleL[i] ^= 0x80000000;

if (draw_plot == 1):
	fig, ax = plt.subplots()
	ax.plot(sampleR, label="R")
	ax.plot(sampleL, label="L")
	ax.legend()
	plt.show()
	plt.close()

if (save_to_file == 1):
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
	Ns = samples_cnt # blocks
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

	for i in range(0, samples_cnt):
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