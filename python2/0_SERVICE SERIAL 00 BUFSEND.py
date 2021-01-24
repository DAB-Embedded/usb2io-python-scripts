#=====================================================
#  Serial buffer send
#=====================================================
import os
import sys
import time
import serial
import select
from usb2io import usb2io_sendcmd
import Tkinter, tkFileDialog
from putbuffer import put_buffer

COM_PORT_ENG                = 'COM17'

#---- Application ---------------------------------------------------------
print "===================================="
print "* uart app"
print "===================================="

local_com_port = sys.argv[1] if (len(sys.argv) > 1) else COM_PORT_ENG

# Open serial port
print "Open serial port " + local_com_port
try:
    ser = serial.Serial(local_com_port, 115200, timeout=100)
    print "COM port OK"
except:
    print "Error COM port"
    sys.exit(0)

# open file
root = Tkinter.Tk()
root.withdraw()

file_opt = options = {}
options['defaultextension'] = '*.*'
options['filetypes'] = [('all files', '*.*')]
options['title'] = 'Select file'


file_path = tkFileDialog.askopenfilename(**file_opt)
if (not file_path):
	print "no file selected"
    	sys.exit(0)

file_size = os.path.getsize(file_path)
print ("file size = " + str(file_size))
if (file_size == 0):
	sys.exit(0)
if ((file_size & 0x01) != 0):
	print "WARNING! File size is odd. " + str(file_size + 1) + " bytes will be sent instead."


f = open(file_path, 'rb')

if (f == None):
	print "can not open file."
	sys.exit(0)


data = bytearray(f.read())
f.close();

if ((len(data) & 0x01) != 0):
	data.append(0x5A)

if (put_buffer(ser, data) == 0):
	sys.exit(0)

usb2io_sendcmd(ser, "service serial bufsend " + str(len(data) / 2) + "\r\n")

raw_input("Press Enter to exit...")
