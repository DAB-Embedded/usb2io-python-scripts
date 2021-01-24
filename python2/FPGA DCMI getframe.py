#=====================================================
#  DCMI camera fpga test
#=====================================================
import os
import sys
import time
import serial
import select
import struct
from usb2io import usb2io_sendcmd
from getbuffer import get_fpga_buffer
from PIL import Image
from numpy import array
import numpy as np
import cv2
import Tkinter, tkFileDialog

COM_PORT_ENG                = 'COM17'

# IMPORTANT!!!
# actual resolution should be obtained by "fpga camera resolution" command


image_width = 1920	
image_height = 1080
save_to_file = 0
#---- Application ---------------------------------------------------------
print "===================================="
print "* DCMI camera fpga test *"
print "===================================="

local_com_port = sys.argv[1] if (len(sys.argv) > 1) else COM_PORT_ENG

# Open serial port7
print "Open serial port " + local_com_port
try:
    ser = serial.Serial(local_com_port, 115200, timeout=3)
    print "COM port OK" 
except:
    print "Error COM port" 
    sys.exit(0)

array_cv2 = np.zeros([image_height, image_width, 3], dtype=np.uint8)


while (1):
	(status, data_out) = get_fpga_buffer(ser, image_height * image_width * 2, 1)
	if (status != True):
		print "Get frame failed"
		sys.exit(0)

	bav = bytearray(data_out)
	#print data_out[:100].encode("hex")
	index = 0
	for y in range (0,image_height):
	    for x in range (0,image_width):
    
		pixel = (bav[index + 1] << 8) | (bav[index])

        	# Extract pixels
       
		array_cv2[y,x,0] = (pixel&0b0000000000011111) << 3 #Blue channel 
        	array_cv2[y,x,1] = (pixel&0b0000011111100000) >> 3 #Green channel 
	        array_cv2[y,x,2] = (pixel >> 8) & 0xF8 #Red channel 
		#array_cv2[y,x,0] = bav[index + 1]
        	#array_cv2[y,x,1] = bav[index + 1]
	        #array_cv2[y,x,2] = bav[index + 1]

	        index += 2

	cv2.imshow('USB2IO Video', array_cv2 )
	key = cv2.waitKey(1) & 0xFF

	if (save_to_file == 1):
		save_to_file = 0
		#save to file
		print "Save results"
		root = Tkinter.Tk()
		root.withdraw()
        
		file_opt = options = {}
		options['defaultextension'] = '.422'
		options['filetypes'] = [('all files', '.*'), ('422 files', '.422')]
		options['title'] = 'Save results'
 

		file_path = tkFileDialog.asksaveasfilename(**file_opt)
		if (not file_path):
			print "no file selected"
            		sys.exit(0)                            

		f = open(file_path, 'wb')

		if (f == None):
			print "can not open file."
			sys.exit(0)                            
                f.write(bav);
                 
		f.close();
# Close serial port
ser.close()
raw_input("Press Enter to exit ...")

