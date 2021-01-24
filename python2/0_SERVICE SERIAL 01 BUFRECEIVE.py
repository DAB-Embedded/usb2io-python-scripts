#=====================================================
#  rebooot
#=====================================================
import os
import sys
import time
import serial
import select
from usb2io import usb2io_sendcmd
import Tkinter, tkFileDialog
from getbuffer import get_buffer

COM_PORT_ENG                = 'COM17'

#---- Application ---------------------------------------------------------
print "===================================="
print "* uart app"
print "===================================="

local_com_port = sys.argv[1] if (len(sys.argv) > 1) else COM_PORT_ENG

# Open serial port
print "Open serial port " + local_com_port
try:
    ser = serial.Serial(local_com_port, 115200, timeout=30)
    print "COM port OK" 
except:
    print "Error COM port" 
    sys.exit(0)

ready = 0
rx_cnt = 0
while (ready == 0):
	ser.write("service serial bufreceive\r\n");
	time.sleep(0.05)
	rrd = ser.readline()
        print rrd
	if (rrd.find("READY") != -1):
		ready = 1
		# parse result
		bytes_str = rrd[17:]
		rx_cnt = int(bytes_str, 10) 
		break;
	
	if (rrd.find("BUSY") != -1):
		continue
	
	break;
if (rx_cnt != 0):
	#get data
	(status, data_out) = get_buffer(ser, rx_cnt)

	print "get_buffer return status: %r" % status
	
	#save to file
	print "Save results"
	root = Tkinter.Tk()
	root.withdraw()
        
	file_opt = options = {}
	options['defaultextension'] = '*.*'
	options['filetypes'] = [('all files', '*.*')]
	options['title'] = 'Save results'
 

	file_path = tkFileDialog.asksaveasfilename(**file_opt)
	if (not file_path):
		print "no file selected"
            	sys.exit(0)                            

	f = open(file_path, 'wb')

	if (f == None):
		print "can not open file."
		sys.exit(0)                            

	# write to file
	newFileByteArray = bytearray(data_out)
	f.write(newFileByteArray)	

	f.close();
raw_input("Press Enter to exit...")
