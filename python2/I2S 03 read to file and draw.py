#=====================================================
#  I2S functional test
#  
#
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
samples_cnt = 3 * 22000; # for each channel
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
	#sampleR[i] = int(0x80000000 + 0x80000000 * math.sin(2 * 3.14 * i/samples_cnt))
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

	for i in range(0, samples_cnt):
		#print >> f, str(sampleL[i]) + " " + str(sampleR[i])
		print >> f, "0x{:08x}".format(sampleL[i]) + " " + "0x{:08x}".format(sampleR[i])


	f.close();