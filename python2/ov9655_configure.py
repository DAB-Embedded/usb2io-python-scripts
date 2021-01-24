#=====================================================
#  OV9655 functional test
#  
#
#=====================================================
import os
import sys
import time
import serial
import select
import struct
import zlib
import binascii
import rawx.base
import rawx.const
import rawx.error
import rawx.tools
import rawx.protocol.rawxt

from rawx.protocol.rawxt import *
from getbuffer import get_buffer

COM_PORT_ENG                = 'COM17'
allow_pre_init              = 1
allow_ov9655_init_qvga      = 0
allow_ov9655_init_vga       = 1
allow_ov9655_init_vga_min   = 0
allow_ov9655_dump_regs      = 0
allow_ov9655_test_mode      = 0
allow_ov9655_init_sxga	    = 0
#---- Application ---------------------------------------------------------
print ("====================================")
print ("* OV9655 test")
print ("====================================")

local_com_port = sys.argv[1] if (len(sys.argv) > 1) else COM_PORT_ENG

def ov9655_reg_write(ser, reg, value):
	strx = "i2c write 1, 0x30," + hex(reg & 0xFF) + "," + hex(value & 0xFF) + "\r\n"
	wro = ser.write(strx)
	time.sleep(0.02)
	rrd = ser.readline()

def ov9655_reg_read(ser, reg):
	strx = "i2c write 1, 0x30," + hex(reg & 0xFF) + "\r\n"
	wro = ser.write(strx)
	rrd = ser.readline()
	strx = "i2c read 1, 0x30,1\r\n"
	wro = ser.write(strx)
	rrd = ser.readline()
	print (rrd)
    
def ov9655_reg_read_ret(ser, reg):
	strx = "i2c write 1, 0x30," + hex(reg & 0xFF) + "\r\n"
	wro = ser.write(strx)
	rrd = ser.readline()
	strx = "i2c read 1, 0x30,1\r\n"
	wro = ser.write(strx)
	rrd = ser.readline()
	return (rrd)
    
def usb2io_command(ser, command):
	ser.write(command)
	time.sleep(0.01)
	rrd = ser.readline()
	print (rrd)
    
def usb2io_command_timeout(ser, command, tmo):
	ser.write(command)
	time.sleep(tmo)
	rrd = ser.readline()
	print (rrd)

def usb2io_command_noresp(ser, command):
	ser.write(command)
	time.sleep(0.01)
	ser.readline()

# Open serial port7
print ("Open serial port " + local_com_port)
try:
    ser = serial.Serial(local_com_port, 115200, timeout=3)
    print ("COM port OK")
except:
    print ("Error COM port")
    sys.exit(0)

    
if allow_pre_init :
    # Set Ext voltage to 0V
    print ("Configure EXT voltage to 0V")
    usb2io_command(ser, "expv write 0\r\n")
    # Wait for clock camera reset
    time.sleep(0.3)
    # Set Ext voltage to 3.3V
    print ("Configure EXT voltage to 3.3V")
    usb2io_command(ser, "expv write 3300\r\n")
    # Setup I2C clock
    print ("Configure I2C: Set 100KHz clock")
    usb2io_command(ser, "i2c configure 0\r\n")
    # for the setting , 24M Mlck input and 24M Plck output
    print ("Set PLL freq")
    usb2io_command(ser, "pll setfreq 48000000\r\n")
    # 0..14
    print ("Configure PINs for Camera")
    for i in range(0, 14):
        pinn = int(i)
        cmd_str = "gpio configure " + str(pinn) + ", 12\r\n"
        usb2io_command_noresp(ser, cmd_str)
    # 6 - PLL
    print ("Configure PIN15 - PLL")
    usb2io_command_noresp(ser, "gpio configure 15, 6\r\n")
    # Wait for clock stabilization
    time.sleep(0.5)



if allow_ov9655_init_qvga :
    print ("OV9655 initialize QVGA mode")
    ov9655_reg_write(ser, 0x12, 0x80)
    time.sleep(0.3)
    ov9655_reg_write(ser, 0x00, 0x00)
    ov9655_reg_write(ser, 0x01, 0x80)
    ov9655_reg_write(ser, 0x02, 0x80)
    ov9655_reg_write(ser, 0x03, 0x02)
    ov9655_reg_write(ser, 0x04, 0x00)
    ov9655_reg_write(ser, 0x09, 0x03)
    ov9655_reg_write(ser, 0x0b, 0x57)
    ov9655_reg_write(ser, 0x0e, 0x1)
    ov9655_reg_write(ser, 0x0f, 0xc0)
    ov9655_reg_write(ser, 0x10, 0x50)
    ov9655_reg_write(ser, 0x11, 0x81)
    ov9655_reg_write(ser, 0x12, 0x63)
    ov9655_reg_write(ser, 0x13, 0xef)
    ov9655_reg_write(ser, 0x14, 0x3a)
    ov9655_reg_write(ser, 0x15, 0x18)
    ov9655_reg_write(ser, 0x16, 0x24)
    ov9655_reg_write(ser, 0x17, 0x18)
    ov9655_reg_write(ser, 0x18, 0x04)
    ov9655_reg_write(ser, 0x19, 0x01)
    ov9655_reg_write(ser, 0x1a, 0x81)
    ov9655_reg_write(ser, 0x1e, 0x00) 					   
    ov9655_reg_write(ser, 0x24, 0x3c)
    ov9655_reg_write(ser, 0x25, 0x36)						   
    ov9655_reg_write(ser, 0x26, 0x72)							   
    ov9655_reg_write(ser, 0x27, 0x08)
    ov9655_reg_write(ser, 0x28, 0x08)
    ov9655_reg_write(ser, 0x29, 0x15)
    ov9655_reg_write(ser, 0x2a, 0x00)
    ov9655_reg_write(ser, 0x2b, 0x00)
    ov9655_reg_write(ser, 0x2c, 0x08)
    ov9655_reg_write(ser, 0x32, 0x12)
    ov9655_reg_write(ser, 0x33, 0x00)
    ov9655_reg_write(ser, 0x34, 0x3f)
    ov9655_reg_write(ser, 0x35, 0x00)
    ov9655_reg_write(ser, 0x36, 0x3a)
    ov9655_reg_write(ser, 0x38, 0x72)
    ov9655_reg_write(ser, 0x39, 0x57)
    ov9655_reg_write(ser, 0x3a, 0x4a) # - 2ns delay (orig 0xca)
    ov9655_reg_write(ser, 0x3b, 0x04)
    ov9655_reg_write(ser, 0x3c, 0x0c) #no HREF when VREF is low, Use average value of last frame as center value
    ov9655_reg_write(ser, 0x3d, 0x99)
    ov9655_reg_write(ser, 0x3e, 0x02) 
    ov9655_reg_write(ser, 0x3f, 0xc1)
    ov9655_reg_write(ser, 0x40, 0xd0) # Full range, RGB565
    ov9655_reg_write(ser, 0x41, 0x41)
    ov9655_reg_write(ser, 0x42, 0xc0)
    ov9655_reg_write(ser, 0x43, 0x0a)
    ov9655_reg_write(ser, 0x44, 0xf0)
    ov9655_reg_write(ser, 0x45, 0x46)
    ov9655_reg_write(ser, 0x46, 0x62)
    ov9655_reg_write(ser, 0x47, 0x2a)
    ov9655_reg_write(ser, 0x48, 0x3c)
    ov9655_reg_write(ser, 0x4a, 0xfc)
    ov9655_reg_write(ser, 0x4b, 0xfc)
    ov9655_reg_write(ser, 0x4c, 0x7f)
    ov9655_reg_write(ser, 0x4d, 0x7f)
    ov9655_reg_write(ser, 0x4e, 0x7f)
    ov9655_reg_write(ser, 0x4f, 0x98)
    ov9655_reg_write(ser, 0x50, 0x98)
    ov9655_reg_write(ser, 0x51, 0x00)
    ov9655_reg_write(ser, 0x52, 0x28)
    ov9655_reg_write(ser, 0x53, 0x70)
    ov9655_reg_write(ser, 0x54, 0x98)
    ov9655_reg_write(ser, 0x58, 0x1a)
    ov9655_reg_write(ser, 0x59, 0x85)
    ov9655_reg_write(ser, 0x5a, 0xa9)
    ov9655_reg_write(ser, 0x5b, 0x64)
    ov9655_reg_write(ser, 0x5c, 0x84)
    ov9655_reg_write(ser, 0x5d, 0x53)
    ov9655_reg_write(ser, 0x5e, 0x0e)
    ov9655_reg_write(ser, 0x5f, 0xf0)
    ov9655_reg_write(ser, 0x60, 0xf0)
    ov9655_reg_write(ser, 0x61, 0xf0)
    ov9655_reg_write(ser, 0x62, 0x00)
    ov9655_reg_write(ser, 0x63, 0x00)
    ov9655_reg_write(ser, 0x64, 0x02)
    ov9655_reg_write(ser, 0x65, 0x20)
    ov9655_reg_write(ser, 0x66, 0x00)
    ov9655_reg_write(ser, 0x69, 0x0a)
    ov9655_reg_write(ser, 0x6b, 0x0a)
    ov9655_reg_write(ser, 0x6c, 0x04)
    ov9655_reg_write(ser, 0x6d, 0x55)
    ov9655_reg_write(ser, 0x6e, 0x00)
    ov9655_reg_write(ser, 0x6f, 0x9d)
    ov9655_reg_write(ser, 0x70, 0x21)
    ov9655_reg_write(ser, 0x71, 0x78)  
    ov9655_reg_write(ser, 0x72, 0x11) 
    ov9655_reg_write(ser, 0x73, 0x01)
    ov9655_reg_write(ser, 0x74, 0x10) 
    ov9655_reg_write(ser, 0x75, 0x10) 
    ov9655_reg_write(ser, 0x76, 0x01)
    ov9655_reg_write(ser, 0x77, 0x02)
    ov9655_reg_write(ser, 0x7A, 0x12)
    ov9655_reg_write(ser, 0x7B, 0x08)
    ov9655_reg_write(ser, 0x7C, 0x16)
    ov9655_reg_write(ser, 0x7D, 0x30)
    ov9655_reg_write(ser, 0x7E, 0x5e)
    ov9655_reg_write(ser, 0x7F, 0x72)
    ov9655_reg_write(ser, 0x80, 0x82)
    ov9655_reg_write(ser, 0x81, 0x8e)
    ov9655_reg_write(ser, 0x82, 0x9a)
    ov9655_reg_write(ser, 0x83, 0xa4)
    ov9655_reg_write(ser, 0x84, 0xac)
    ov9655_reg_write(ser, 0x85, 0xb8)
    ov9655_reg_write(ser, 0x86, 0xc3)
    ov9655_reg_write(ser, 0x87, 0xd6)
    ov9655_reg_write(ser, 0x88, 0xe6)
    ov9655_reg_write(ser, 0x89, 0xf2)
    ov9655_reg_write(ser, 0x8a, 0x24)
    ov9655_reg_write(ser, 0x8c, 0x80)
    ov9655_reg_write(ser, 0x90, 0x7d)
    ov9655_reg_write(ser, 0x91, 0x7b)
    ov9655_reg_write(ser, 0x9d, 0x02)
    ov9655_reg_write(ser, 0x9e, 0x02)
    ov9655_reg_write(ser, 0x9f, 0x7a)
    ov9655_reg_write(ser, 0xa0, 0x79)
    ov9655_reg_write(ser, 0xa1, 0x1f)
    ov9655_reg_write(ser, 0xa4, 0x50)
    ov9655_reg_write(ser, 0xa5, 0x68)
    ov9655_reg_write(ser, 0xa6, 0x4a)
    ov9655_reg_write(ser, 0xa8, 0xc1)
    ov9655_reg_write(ser, 0xa9, 0xef)
    ov9655_reg_write(ser, 0xaa, 0x92)
    ov9655_reg_write(ser, 0xab, 0x04)
    ov9655_reg_write(ser, 0xac, 0x80)
    ov9655_reg_write(ser, 0xad, 0x80)
    ov9655_reg_write(ser, 0xae, 0x80)
    ov9655_reg_write(ser, 0xaf, 0x80)
    ov9655_reg_write(ser, 0xb2, 0xf2)
    ov9655_reg_write(ser, 0xb3, 0x20)
    ov9655_reg_write(ser, 0xb4, 0x20)
    ov9655_reg_write(ser, 0xb5, 0x00)
    ov9655_reg_write(ser, 0xb6, 0xaf)
    ov9655_reg_write(ser, 0xb6, 0xaf)
    ov9655_reg_write(ser, 0xbb, 0xae)
    ov9655_reg_write(ser, 0xbc, 0x7f)
    ov9655_reg_write(ser, 0xbd, 0x7f)
    ov9655_reg_write(ser, 0xbe, 0x7f)
    ov9655_reg_write(ser, 0xbf, 0x7f)
    ov9655_reg_write(ser, 0xbf, 0x7f)
    ov9655_reg_write(ser, 0xc0, 0xaa)
    ov9655_reg_write(ser, 0xc1, 0xc0)
    ov9655_reg_write(ser, 0xc2, 0x01)
    ov9655_reg_write(ser, 0xc3, 0x4e)
    ov9655_reg_write(ser, 0xc6, 0x05)
    ov9655_reg_write(ser, 0xc7, 0x81)
    ov9655_reg_write(ser, 0xc9, 0xe0)
    ov9655_reg_write(ser, 0xca, 0xe8)
    ov9655_reg_write(ser, 0xcb, 0xf0)
    ov9655_reg_write(ser, 0xcc, 0xd8)
    ov9655_reg_write(ser, 0xcd, 0x93)
    ov9655_reg_write(ser, 0x09, 0x03) # Outout drive capability 4x
    ov9655_reg_write(ser, 0x12, 0x63) # 30fps VGA, RGB
    ov9655_reg_write(ser, 0x15, 0x18) # HREF reverse, PCLK rev and no VSYNC reverse
    
if allow_ov9655_init_vga :
    print ("OV9655 initialize VGA mode")
    ov9655_reg_write(ser, 0x12, 0x80)
    time.sleep(0.3)
    ov9655_reg_write(ser, 0x00, 0x00)
    ov9655_reg_write(ser, 0x01, 0x80)   
    ov9655_reg_write(ser, 0x02, 0x80)   
    ov9655_reg_write(ser, 0xb5, 0x00)   
    ov9655_reg_write(ser, 0x35, 0x00)   
    ov9655_reg_write(ser, 0xa8, 0xc1)   
    ov9655_reg_write(ser, 0x3a, 0xca) # - 6ns delay (orig 0xca)
    ov9655_reg_write(ser, 0x3d, 0x99)   
    ov9655_reg_write(ser, 0x77, 0x02)   
    ov9655_reg_write(ser, 0x13, 0xe7)   
    ov9655_reg_write(ser, 0x26, 0x72)   
    ov9655_reg_write(ser, 0x27, 0x08)   
    ov9655_reg_write(ser, 0x28, 0x08)   
    ov9655_reg_write(ser, 0x2c, 0x08)   
    ov9655_reg_write(ser, 0xab, 0x04)   
    ov9655_reg_write(ser, 0x6e, 0x00)   
    ov9655_reg_write(ser, 0x6d, 0x55)   
    ov9655_reg_write(ser, 0x00, 0x11)   
    ov9655_reg_write(ser, 0x10, 0x7b)   
    ov9655_reg_write(ser, 0xbb, 0xae)   
    ov9655_reg_write(ser, 0x11, 0x81) # pre-scaler /1
    ov9655_reg_write(ser, 0x72, 0x00)   
    ov9655_reg_write(ser, 0x3e, 0x0c)   
    ov9655_reg_write(ser, 0x74, 0x3a)   
    ov9655_reg_write(ser, 0x76, 0x01)   
    ov9655_reg_write(ser, 0x75, 0x35)   
    ov9655_reg_write(ser, 0x73, 0x00)   
    ov9655_reg_write(ser, 0xc7, 0x80)   
    ov9655_reg_write(ser, 0x62, 0x00)   
    ov9655_reg_write(ser, 0x63, 0x00)   
    ov9655_reg_write(ser, 0x64, 0x02)   
    ov9655_reg_write(ser, 0x65, 0x20)   
    ov9655_reg_write(ser, 0x66, 0x01)   
    ov9655_reg_write(ser, 0xc3, 0x4e)   
    ov9655_reg_write(ser, 0x33, 0x00)   
    ov9655_reg_write(ser, 0xa4, 0x50)   
    ov9655_reg_write(ser, 0xaa, 0x92)   
    ov9655_reg_write(ser, 0xc2, 0x01)   
    ov9655_reg_write(ser, 0xc1, 0xC8)
    ov9655_reg_write(ser, 0x1e, 0x04) # No mirror
    ov9655_reg_write(ser, 0xa9, 0xef)   
    ov9655_reg_write(ser, 0x0e, 0x61) # orig 0x61
    ov9655_reg_write(ser, 0x39, 0x57)   
    ov9655_reg_write(ser, 0x0f, 0xc8) # orig 0x48, enable bias for B/Gr/Gb/R
    ov9655_reg_write(ser, 0x24, 0x3c)   
    ov9655_reg_write(ser, 0x25, 0x36)   
    ov9655_reg_write(ser, 0x12, 0x63)   
    ov9655_reg_write(ser, 0x03, 0x12)   
    ov9655_reg_write(ser, 0x32, 0xff)   
    ov9655_reg_write(ser, 0x17, 0x16)   
    ov9655_reg_write(ser, 0x18, 0x02)   
    ov9655_reg_write(ser, 0x19, 0x01)   
    ov9655_reg_write(ser, 0x1a, 0x3d)   
    ov9655_reg_write(ser, 0x36, 0xfa)   
    ov9655_reg_write(ser, 0x69, 0x0a)   
    ov9655_reg_write(ser, 0x8c, 0x8d)   
    ov9655_reg_write(ser, 0xc0, 0xaa)   
    ov9655_reg_write(ser, 0x40, 0xd0) # Full range, RGB565
    ov9655_reg_write(ser, 0x43, 0x0a) # orig 0x0a
    ov9655_reg_write(ser, 0x44, 0xf0)   
    ov9655_reg_write(ser, 0x45, 0x46)   
    ov9655_reg_write(ser, 0x46, 0x62)   
    ov9655_reg_write(ser, 0x47, 0x2a)   
    ov9655_reg_write(ser, 0x48, 0x3c)   
    ov9655_reg_write(ser, 0x59, 0x85)   
    ov9655_reg_write(ser, 0x5a, 0xa9)   
    ov9655_reg_write(ser, 0x5b, 0x64)   
    ov9655_reg_write(ser, 0x5c, 0x84)   
    ov9655_reg_write(ser, 0x5d, 0x53)   
    ov9655_reg_write(ser, 0x5e, 0x0e)   
    ov9655_reg_write(ser, 0x6c, 0x0c) # orig 0x0c 
    ov9655_reg_write(ser, 0xc6, 0x85) # orig 0x85   
    ov9655_reg_write(ser, 0xcb, 0xf0)   
    ov9655_reg_write(ser, 0xcc, 0xd8)   
    ov9655_reg_write(ser, 0x71, 0x78)   
    ov9655_reg_write(ser, 0xa5, 0x68)   
    ov9655_reg_write(ser, 0x6f, 0x23) # orig 0x23 
    ov9655_reg_write(ser, 0x42, 0xc0)   
    ov9655_reg_write(ser, 0x3f, 0x82)   
    ov9655_reg_write(ser, 0x8a, 0x23) # orig 0x23
    ov9655_reg_write(ser, 0x14, 0x3a)   
    ov9655_reg_write(ser, 0x3b, 0xcc)   
    ov9655_reg_write(ser, 0x34, 0x3d)   
    ov9655_reg_write(ser, 0x41, 0x40)   
    ov9655_reg_write(ser, 0xc9, 0xe0)   
    ov9655_reg_write(ser, 0xca, 0xe8)   
    ov9655_reg_write(ser, 0xcd, 0x93)   
    ov9655_reg_write(ser, 0x7a, 0x20)   
    ov9655_reg_write(ser, 0x7b, 0x1c)   
    ov9655_reg_write(ser, 0x7c, 0x28)   
    ov9655_reg_write(ser, 0x7d, 0x3c)   
    ov9655_reg_write(ser, 0x7e, 0x5a)   
    ov9655_reg_write(ser, 0x7f, 0x68)   
    ov9655_reg_write(ser, 0x80, 0x76)   
    ov9655_reg_write(ser, 0x81, 0x80)   
    ov9655_reg_write(ser, 0x82, 0x88)   
    ov9655_reg_write(ser, 0x83, 0x8f)   
    ov9655_reg_write(ser, 0x84, 0x96)   
    ov9655_reg_write(ser, 0x85, 0xa3)   
    ov9655_reg_write(ser, 0x86, 0xaf)   
    ov9655_reg_write(ser, 0x87, 0xc4)   
    ov9655_reg_write(ser, 0x88, 0xd7)   
    ov9655_reg_write(ser, 0x89, 0xe8)   
    ov9655_reg_write(ser, 0x4f, 0x98)   
    ov9655_reg_write(ser, 0x50, 0x98)   
    ov9655_reg_write(ser, 0x51, 0x00)   
    ov9655_reg_write(ser, 0x52, 0x28)   
    ov9655_reg_write(ser, 0x53, 0x70)   
    ov9655_reg_write(ser, 0x54, 0x98)   
    ov9655_reg_write(ser, 0x58, 0x1a)   
    ov9655_reg_write(ser, 0x6b, 0x0a) # Not bypass int regulator DVDD, PLL 4x (0x4a)
    ov9655_reg_write(ser, 0x90, 0x92)   
    ov9655_reg_write(ser, 0x91, 0x92)   
    ov9655_reg_write(ser, 0x9f, 0x90)   
    ov9655_reg_write(ser, 0xa0, 0x90)   
    ov9655_reg_write(ser, 0x16, 0x24)   
    ov9655_reg_write(ser, 0x2a, 0x00)   
    ov9655_reg_write(ser, 0x2b, 0x00)   
    ov9655_reg_write(ser, 0xac, 0x80)   
    ov9655_reg_write(ser, 0xad, 0x80)   
    ov9655_reg_write(ser, 0xae, 0x80)   
    ov9655_reg_write(ser, 0xaf, 0x80)   
    ov9655_reg_write(ser, 0xb2, 0xf2)   
    ov9655_reg_write(ser, 0xb3, 0x20)   
    ov9655_reg_write(ser, 0xb4, 0x20)   
    ov9655_reg_write(ser, 0xb6, 0xaf)   
    ov9655_reg_write(ser, 0x29, 0x15)   
    ov9655_reg_write(ser, 0x9d, 0x02)   
    ov9655_reg_write(ser, 0x9e, 0x02)   
    ov9655_reg_write(ser, 0x9e, 0x02)   
    ov9655_reg_write(ser, 0x04, 0x03)
    ov9655_reg_write(ser, 0x05, 0x2e)   
    ov9655_reg_write(ser, 0x06, 0x2e)   
    ov9655_reg_write(ser, 0x07, 0x2e)   
    ov9655_reg_write(ser, 0x08, 0x2e)   
    ov9655_reg_write(ser, 0x2f, 0x2e)   
    ov9655_reg_write(ser, 0x4a, 0xe9)
    ov9655_reg_write(ser, 0x4b, 0xdd)   
    ov9655_reg_write(ser, 0x4c, 0xdd)   
    ov9655_reg_write(ser, 0x4d, 0xdd)   
    ov9655_reg_write(ser, 0x4e, 0xdd)   
    ov9655_reg_write(ser, 0x70, 0x06)   
    ov9655_reg_write(ser, 0xa6, 0x40)   
    ov9655_reg_write(ser, 0xbc, 0x02)   
    ov9655_reg_write(ser, 0xbd, 0x01)   
    ov9655_reg_write(ser, 0xbe, 0x02) 
    ov9655_reg_write(ser, 0xbf, 0x01)
    ov9655_reg_write(ser, 0x09, 0x03) # Outout drive capability 4x
    ov9655_reg_write(ser, 0x12, 0x63) # 30fps VGA, RGB
    ov9655_reg_write(ser, 0x15, 0x08) # HREF reverse, PCLK rev and no VSYNC reverse
    print ("OV9655 initialize VGA mode DONE")

if allow_ov9655_init_sxga:
    print ("OV9655 initialize SXGA mode")
    ov9655_reg_write(ser, 0x12, 0x80)
    time.sleep(0.3)
    ov9655_reg_write(ser, 0x00, 0x00)
    ov9655_reg_write(ser, 0x01, 0x80)   
    ov9655_reg_write(ser, 0x02, 0x80)   
    ov9655_reg_write(ser, 0xb5, 0x00)   
    ov9655_reg_write(ser, 0x35, 0x00)   
    ov9655_reg_write(ser, 0xa8, 0xc1)   
    ov9655_reg_write(ser, 0x3a, 0xca) # - 6ns delay (orig 0xca)
    ov9655_reg_write(ser, 0x3d, 0x99)   
    ov9655_reg_write(ser, 0x77, 0x02)   
    ov9655_reg_write(ser, 0x13, 0xe7)  # enable automation
#    ov9655_reg_write(ser, 0x13, 0x60)  # disable automation
    ov9655_reg_write(ser, 0x26, 0x72)   
    ov9655_reg_write(ser, 0x27, 0x08)   
    ov9655_reg_write(ser, 0x28, 0x08)   
    ov9655_reg_write(ser, 0x2c, 0x08)   
    ov9655_reg_write(ser, 0xab, 0x04)   
    ov9655_reg_write(ser, 0x6e, 0x00)   
    ov9655_reg_write(ser, 0x6d, 0x55)   
    ov9655_reg_write(ser, 0x00, 0x11)   
    ov9655_reg_write(ser, 0x10, 0x7b) # agc [9 : 2]   
    ov9655_reg_write(ser, 0xbb, 0xae)   
    ov9655_reg_write(ser, 0x11, 0x81) # pre-scaler /1
    ov9655_reg_write(ser, 0x72, 0x00)   
    ov9655_reg_write(ser, 0x3e, 0x0c)   
    ov9655_reg_write(ser, 0x74, 0x3a)   
    ov9655_reg_write(ser, 0x76, 0x01)   
    ov9655_reg_write(ser, 0x75, 0x35)   
    ov9655_reg_write(ser, 0x73, 0x00)   
    ov9655_reg_write(ser, 0xc7, 0x80)   
    ov9655_reg_write(ser, 0x62, 0x00)   
    ov9655_reg_write(ser, 0x63, 0x00)   
    ov9655_reg_write(ser, 0x64, 0x02)   
    ov9655_reg_write(ser, 0x65, 0x20)   
    ov9655_reg_write(ser, 0x66, 0x01)   
    ov9655_reg_write(ser, 0xc3, 0x4e)   
    ov9655_reg_write(ser, 0x33, 0x00)   
    ov9655_reg_write(ser, 0xa4, 0x50)   
    ov9655_reg_write(ser, 0xaa, 0x92)   
    ov9655_reg_write(ser, 0xc2, 0x01)   
    ov9655_reg_write(ser, 0xc1, 0xC8)
    ov9655_reg_write(ser, 0x1e, 0x04) # No mirror
    ov9655_reg_write(ser, 0xa9, 0xef)   
    ov9655_reg_write(ser, 0x0e, 0x61) # orig 0x61
    ov9655_reg_write(ser, 0x39, 0x57)   
    ov9655_reg_write(ser, 0x0f, 0xc8) # orig 0x48, enable bias for B/Gr/Gb/R
    ov9655_reg_write(ser, 0x24, 0x3c)   
    ov9655_reg_write(ser, 0x25, 0x36)   
    ov9655_reg_write(ser, 0x12, 0x03)   
    ov9655_reg_write(ser, 0x03, 0x12)   
    ov9655_reg_write(ser, 0x32, 0xff)   
    #ov9655_reg_write(ser, 0x17, 0x16)   
    #ov9655_reg_write(ser, 0x18, 0x02)   
    #ov9655_reg_write(ser, 0x19, 0x01)   
    #ov9655_reg_write(ser, 0x1a, 0x3d)   
    ov9655_reg_write(ser, 0x36, 0xfa)   
    ov9655_reg_write(ser, 0x69, 0x0a)   
    ov9655_reg_write(ser, 0x8c, 0x8d)   
    ov9655_reg_write(ser, 0xc0, 0xaa)   
    ov9655_reg_write(ser, 0x40, 0xd0) # Full range, RGB565
    ov9655_reg_write(ser, 0x43, 0x0a) # orig 0x0a
    ov9655_reg_write(ser, 0x44, 0xf0)   
    ov9655_reg_write(ser, 0x45, 0x46)   
    ov9655_reg_write(ser, 0x46, 0x62)   
    ov9655_reg_write(ser, 0x47, 0x2a)   
    ov9655_reg_write(ser, 0x48, 0x3c)   
    ov9655_reg_write(ser, 0x59, 0x85)   
    ov9655_reg_write(ser, 0x5a, 0xa9)   
    ov9655_reg_write(ser, 0x5b, 0x64)   
    ov9655_reg_write(ser, 0x5c, 0x84)   
    ov9655_reg_write(ser, 0x5d, 0x53)   
    ov9655_reg_write(ser, 0x5e, 0x0e)   
    ov9655_reg_write(ser, 0x6c, 0x0c) # orig 0x0c 
    ov9655_reg_write(ser, 0xc6, 0x85) # orig 0x85   
    ov9655_reg_write(ser, 0xcb, 0xf0)   
    ov9655_reg_write(ser, 0xcc, 0xd8)   
    ov9655_reg_write(ser, 0x71, 0x78)   
    ov9655_reg_write(ser, 0xa5, 0x68)   
    ov9655_reg_write(ser, 0x6f, 0x23) # orig 0x23 
    ov9655_reg_write(ser, 0x42, 0xc0)   
    ov9655_reg_write(ser, 0x3f, 0x82)   
    ov9655_reg_write(ser, 0x8a, 0x23) # orig 0x23
    ov9655_reg_write(ser, 0x14, 0x3a)   
    ov9655_reg_write(ser, 0x3b, 0xcc)   
    ov9655_reg_write(ser, 0x34, 0x3d)   
    ov9655_reg_write(ser, 0x41, 0x40)   
    ov9655_reg_write(ser, 0xc9, 0xe0)   
    ov9655_reg_write(ser, 0xca, 0xe8)   
    ov9655_reg_write(ser, 0xcd, 0x93)   
    ov9655_reg_write(ser, 0x7a, 0x20)   
    ov9655_reg_write(ser, 0x7b, 0x1c)   
    ov9655_reg_write(ser, 0x7c, 0x28)   
    ov9655_reg_write(ser, 0x7d, 0x3c)   
    ov9655_reg_write(ser, 0x7e, 0x5a)   
    ov9655_reg_write(ser, 0x7f, 0x68)   
    ov9655_reg_write(ser, 0x80, 0x76)   
    ov9655_reg_write(ser, 0x81, 0x80)   
    ov9655_reg_write(ser, 0x82, 0x88)   
    ov9655_reg_write(ser, 0x83, 0x8f)   
    ov9655_reg_write(ser, 0x84, 0x96)   
    ov9655_reg_write(ser, 0x85, 0xa3)   
    ov9655_reg_write(ser, 0x86, 0xaf)   
    ov9655_reg_write(ser, 0x87, 0xc4)   
    ov9655_reg_write(ser, 0x88, 0xd7)   
    ov9655_reg_write(ser, 0x89, 0xe8)   
    ov9655_reg_write(ser, 0x4f, 0x98)   
    ov9655_reg_write(ser, 0x50, 0x98)   
    ov9655_reg_write(ser, 0x51, 0x00)   
    ov9655_reg_write(ser, 0x52, 0x28)   
    ov9655_reg_write(ser, 0x53, 0x70)   
    ov9655_reg_write(ser, 0x54, 0x98)   
    ov9655_reg_write(ser, 0x58, 0x1a)   
    ov9655_reg_write(ser, 0x6b, 0x0a) # Not bypass int regulator DVDD, PLL 4x (0x4a)
    ov9655_reg_write(ser, 0x90, 0x92)   
    ov9655_reg_write(ser, 0x91, 0x92)   
    ov9655_reg_write(ser, 0x9f, 0x90)   
    ov9655_reg_write(ser, 0xa0, 0x90)   
    ov9655_reg_write(ser, 0x16, 0x24)   
    ov9655_reg_write(ser, 0x2a, 0x00)   
    ov9655_reg_write(ser, 0x2b, 0x00)   
    ov9655_reg_write(ser, 0xac, 0x80)   
    ov9655_reg_write(ser, 0xad, 0x80)   
    ov9655_reg_write(ser, 0xae, 0x80)   
    ov9655_reg_write(ser, 0xaf, 0x80)   
    ov9655_reg_write(ser, 0xb2, 0xf2)   
    ov9655_reg_write(ser, 0xb3, 0x20)   
    ov9655_reg_write(ser, 0xb4, 0x20)   
    ov9655_reg_write(ser, 0xb6, 0xaf)   
    ov9655_reg_write(ser, 0x29, 0x15)   
    ov9655_reg_write(ser, 0x9d, 0x02)   
    ov9655_reg_write(ser, 0x9e, 0x02)   
    ov9655_reg_write(ser, 0x9e, 0x02)   
    ov9655_reg_write(ser, 0x04, 0x03)
    ov9655_reg_write(ser, 0x05, 0x2e)   
    ov9655_reg_write(ser, 0x06, 0x2e)   
    ov9655_reg_write(ser, 0x07, 0x2e)   
    ov9655_reg_write(ser, 0x08, 0x2e)   
    ov9655_reg_write(ser, 0x2f, 0x2e)   
    ov9655_reg_write(ser, 0x4a, 0xe9)
    ov9655_reg_write(ser, 0x4b, 0xdd)   
    ov9655_reg_write(ser, 0x4c, 0xdd)   
    ov9655_reg_write(ser, 0x4d, 0xdd)   
    ov9655_reg_write(ser, 0x4e, 0xdd)   
    ov9655_reg_write(ser, 0x70, 0x06)   
    ov9655_reg_write(ser, 0xa6, 0x40)   
    ov9655_reg_write(ser, 0xbc, 0x02)   
    ov9655_reg_write(ser, 0xbd, 0x01)   
    ov9655_reg_write(ser, 0xbe, 0x02) 
    ov9655_reg_write(ser, 0xbf, 0x01)
    ov9655_reg_write(ser, 0x09, 0x03) # Outout drive capability 4x
    ov9655_reg_write(ser, 0x12, 0x03) # 15fps SXGA, RGB
    ov9655_reg_write(ser, 0x15, 0x18) # HREF reverse, PCLK rev and no VSYNC reverse
    print ("OV9655 initialize SXGA mode DONE")

if allow_ov9655_init_vga_min :
    ov9655_reg_write(ser, 0x40, 0xd0) # Full range, RGB565
    ov9655_reg_write(ser, 0x09, 0x03) # Outout drive capability 4x
    ov9655_reg_write(ser, 0x12, 0x63) # 30fps VGA, RGB
    ov9655_reg_write(ser, 0x15, 0x18) # HREF reverse, PCLK rev and no VSYNC reverse

if allow_ov9655_dump_regs :
    for i in range(0, 0xC7):
        rega = int(i)
        regv = ov9655_reg_read_ret(ser, rega)
        regvc = regv.replace('OK,','').replace('\r\n','')
        print "Reg " + hex(rega) + " val: " + str(regvc)

if allow_ov9655_test_mode :
    ov9655_reg_write(ser, 0x8d, 0x10)
    ov9655_reg_write(ser, 0x0c, 0x80)


# Close serial port
ser.close()
print ("API test done" )
raw_input("Press Enter to exit ...")
