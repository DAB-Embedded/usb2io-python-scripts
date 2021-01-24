#=====================================================
#  TMP116 functional test
#  
#
#=====================================================
import os
import sys
import time
import serial
import select
import ctypes as ct


COM_PORT_ENG                = 'COM17'

TMP117_SLAVE_ID             = 0x48

TMP117_TEMP_RESULT          = 0x00
TMP117_CONFIGURATION        = 0x01,
TMP117_T_HIGH_LIMIT         = 0X02,
TMP117_T_LOW_LIMIT          = 0X03,
TMP117_EEPROM_UL            = 0X04,
TMP117_EEPROM1              = 0X05,
TMP117_EEPROM2              = 0X06,
TMP117_TEMP_OFFSET          = 0X07,
TMP117_EEPROM3              = 0X08,
TMP117_DEVICE_ID            = 0X0F

#---- Application ---------------------------------------------------------
print "===================================="
print "* Temp Reading"
print "===================================="

local_com_port = sys.argv[1] if (len(sys.argv) > 1) else COM_PORT_ENG

def tmp117_reg_read(ser, reg):
	strx = "i2c write 1, " + hex(TMP117_SLAVE_ID) + "," + hex(reg & 0xFF) + "\r\n"
	wro = ser.write(strx)
	time.sleep(0.02)
	rrd = ser.readline()
	if (rrd.find('FAIL') != -1):
		return (rrd)
	strx = "i2c read 1, " + hex(TMP117_SLAVE_ID) + ",2\r\n"
	wro = ser.write(strx)
	time.sleep(0.02)
	rrd = ser.readline()    
	return (rrd)
    
def tmp117_reg_write(ser, reg, value):
	strx = "i2c write 1, " + hex(TMP117_SLAVE_ID) + "," + hex(reg & 0xFF) + "," + hex(reg >> 8) + "," + hex(reg & 0xFF) + "\r\n"
	wro = ser.write(strx)
	time.sleep(0.02)
	rrd = ser.readline()    
    
def tmp117_reg_temperature(ser):
	str_ret = tmp117_reg_read(ser, TMP117_TEMP_RESULT)
	if (str_ret.find('FAIL') != -1):
		return (0)
	ba1 = [int(i,16) for i in str_ret.replace('OK,', '').split(',')]
	dtemp = (ba1[0] << 8) | ba1[1]
	temp_res_d = ct.c_int16(dtemp)
	temp_res_f = float(temp_res_d.value) * 0.0078125
	return (temp_res_f)

# Open serial port
print "Open serial port " + local_com_port
try:
    ser = serial.Serial(local_com_port, 115200, timeout=3)
    print "COM port OK" 
except:
    print "Error COM port" 
    sys.exit(0)

print "Temp: "
print(tmp117_reg_temperature(ser))


# Close serial port
ser.close()

