#=====================================================
#  AS7265x functional test
#  
#
#=====================================================
import os
import re
import sys
import time
import serial
import select
import rawx.base
import rawx.const
import rawx.error
import rawx.tools
import rawx.protocol.rawxt

from rawx.protocol.rawxt import *


# Constants
as7265x_saddr               = 0x49

AS7265X_STATUS_REG          = 0x00
AS7265X_WRITE_REG           = 0x01
AS7265X_READ_REG            = 0x02

AS7265X_TX_VALID            = 0x02
AS7265X_RX_VALID            = 0x01

AS7265X_HW_VERSION_HIGH     = 0x00
AS7265X_HW_VERSION_LOW      = 0x01

AS7265X_FW_VERSION_HIGH     = 0x02
AS7265X_FW_VERSION_LOW      = 0x03

AS7265X_CONFIG              = 0x04
AS7265X_INTERGRATION_TIME   = 0x05
AS7265X_DEVICE_TEMP         = 0x06
AS7265X_LED_CONFIG          = 0x07

AS7265X_R_G_A               = 0x08
AS7265X_S_H_B               = 0x0A
AS7265X_T_I_C               = 0x0C
AS7265X_U_J_D               = 0x0E
AS7265X_V_K_E               = 0x10
AS7265X_W_L_F               = 0x12

AS7265X_R_G_A_CAL           = 0x14
AS7265X_S_H_B_CAL           = 0x18
AS7265X_T_I_C_CAL           = 0x1C
AS7265X_U_J_D_CAL           = 0x20
AS7265X_V_K_E_CAL           = 0x24
AS7265X_W_L_F_CAL           = 0x28

AS7265X_DEV_SELECT_CONTROL  = 0x4F

AS7265X_COEF_DATA_0         = 0x50
AS7265X_COEF_DATA_1         = 0x51
AS7265X_COEF_DATA_2         = 0x52
AS7265X_COEF_DATA_3         = 0x53
AS7265X_COEF_DATA_READ      = 0x54
AS7265X_COEF_DATA_WRITE     = 0x55

AS7265X_POLLING_DELAY       = 0.05 # 5 mS


AS72651_NIR                 = 0x00
AS72652_VISIBLE             = 0x01
AS72653_UV                  = 0x02

AS7265x_LED_WHITE	        = 0x00
AS7265x_LED_IR	            = 0x01
AS7265x_LED_UV	            = 0x02

AS7265X_LED_CURRENT_LIMIT_12_5MA            = 0b00
AS7265X_LED_CURRENT_LIMIT_25MA              = 0b01
AS7265X_LED_CURRENT_LIMIT_50MA              = 0b10
AS7265X_LED_CURRENT_LIMIT_100MA             = 0b11

AS7265X_INDICATOR_CURRENT_LIMIT_1MA         = 0b00
AS7265X_INDICATOR_CURRENT_LIMIT_2MA         = 0b01
AS7265X_INDICATOR_CURRENT_LIMIT_4MA         = 0b10
AS7265X_INDICATOR_CURRENT_LIMIT_8MA         = 0b11

AS7265X_GAIN_1X                             = 0b00
AS7265X_GAIN_37X                            = 0b01
AS7265X_GAIN_16X                            = 0b10
AS7265X_GAIN_64X                            = 0b11

AS7265X_MEASUREMENT_MODE_4CHAN              = 0b00
AS7265X_MEASUREMENT_MODE_4CHAN_2            = 0b01
AS7265X_MEASUREMENT_MODE_6CHAN_CONTINUOUS   = 0b10
AS7265X_MEASUREMENT_MODE_6CHAN_ONE_SHOT     = 0b11

I2C_USB2IO_CMM_DELAY                        = 0.01

COM_PORT_ENG                                = 'COM148'
fpga_filename                               = "fpga_waveform.rbf"
allow_load_fpga                             = 0

def as7265x_reg_write(ser, reg, value):
	strx = "i2c write 1, " + hex(as7265x_saddr) + "," + hex(reg & 0xFF) + "," + hex(value & 0xFF) + "\r\n"
	wro = ser.write(strx)
	time.sleep(I2C_USB2IO_CMM_DELAY)
	rrd = ser.readline()
	if (rrd != 'OK\r\n'):
		print "[reg write] i2c write error"
		return False
	return True

def as7265x_reg_read(ser, reg):
	strx = "i2c write 1, " + hex(as7265x_saddr) + "," + hex(reg & 0xFF) + "\r\n"
	wro = ser.write(strx)
	time.sleep(I2C_USB2IO_CMM_DELAY)
	rrd = ser.readline()
	if (rrd != 'OK\r\n'):
		print "[reg read] i2c write error"
		return (False, 0)
	strx = "i2c read 1, " + hex(as7265x_saddr) + ",1\r\n"
	wro = ser.write(strx)
	time.sleep(I2C_USB2IO_CMM_DELAY)
	rrd = ser.readline()
	if (rrd.find('OK') == -1):
		print "[reg read] i2c read error"
		return (False, 0)
	i2c_ret = re.split(r',', rrd)
	i2c_value = int(i2c_ret[1], 16)
	return (True, i2c_value)

def as7265x_virtual_reg_write(ser, reg, value):
	while (True):
		(status, val8) = as7265x_reg_read(ser, AS7265X_STATUS_REG)
		if (status != True):
			return False
		if (val8 & AS7265X_TX_VALID) == 0:
			break
		time.sleep(AS7265X_POLLING_DELAY)
		
	# Write address
	if (as7265x_reg_write(ser, AS7265X_WRITE_REG, reg | (1 << 7)) != True):
		return False
		
	while (True):
		(status, val8) = as7265x_reg_read(ser, AS7265X_STATUS_REG)
		if (status != True):
			return False    
		if (val8 & AS7265X_TX_VALID) == 0:
			break
		time.sleep(AS7265X_POLLING_DELAY)
		
	if (as7265x_reg_write(ser, AS7265X_WRITE_REG, value) != True):
		return False
	return True

def as7265x_virtual_reg_read(ser, reg):
	while (True):
		(status, val8) = as7265x_reg_read(ser, AS7265X_STATUS_REG)
		if (status != True):
			return (False, 0)
		if (val8 & AS7265X_TX_VALID) == 0:
			break
		time.sleep(AS7265X_POLLING_DELAY)
		
	# Write address
	if (as7265x_reg_write(ser, AS7265X_WRITE_REG, reg) != True):
		return (False, 0)
		
	while (True):
		(status, val8) = as7265x_reg_read(ser, AS7265X_STATUS_REG)
		if (status != True):
			return False    
		if (val8 & AS7265X_TX_VALID) == 0:
			break
		time.sleep(AS7265X_POLLING_DELAY)
		
	(status, val8) = as7265x_reg_read(ser, AS7265X_READ_REG)
	if (status != True):
		return (False, 0)
	return (True, val8)

def as7265x_soft_reset(ser):
	(status, val) = as7265x_virtual_reg_read(ser, AS7265X_CONFIG)
	if (status != True):
		return
	val |= (1 << 7)
	as7265x_virtual_reg_write(ser, AS7265X_CONFIG, val)

def as7265x_select_device(ser, device):
	as7265x_virtual_reg_write(ser, AS7265X_DEV_SELECT_CONTROL, device)

def as7265x_set_bulb_current(ser, current, device):
	as7265x_select_device(ser, device)
	if (current > 3):
		current = 3
	(status, val) = as7265x_virtual_reg_read(ser, AS7265X_LED_CONFIG)
	if (status != True):
		return
	val &= 0b11001111
	val |= (current << 4)
	as7265x_virtual_reg_write(ser, AS7265X_LED_CONFIG, val)

def as7265x_enable_bulb(ser, device):
	as7265x_select_device(ser, device)
	(status, val) = as7265x_virtual_reg_read(ser, AS7265X_LED_CONFIG)
	if (status != True):
		return
	val |= (1 << 3)
	as7265x_virtual_reg_write(ser, AS7265X_LED_CONFIG, val)

def as7265x_disable_bulb(ser, device):
	as7265x_select_device(ser, device)
	(status, val) = as7265x_virtual_reg_read(ser, AS7265X_LED_CONFIG)
	if (status != True):
		return
	val &= ~(1 << 3)
	as7265x_virtual_reg_write(ser, AS7265X_LED_CONFIG, val)

def as7265x_enable_indicator(ser):
	(status, val) = as7265x_virtual_reg_read(ser, AS7265X_LED_CONFIG)
	if (status != True):
		return
	val |= (1 << 0)
	as7265x_virtual_reg_write(ser, AS7265X_LED_CONFIG, val)

def as7265x_disable_indicator(ser):
	(status, val) = as7265x_virtual_reg_read(ser, AS7265X_LED_CONFIG)
	if (status != True):
		return
	val &= ~(1 << 0)
	as7265x_virtual_reg_write(ser, AS7265X_LED_CONFIG, val)

def as7265x_set_indicator_current(ser, current):
	if (current > 3):
		current = 3
	(status, val) = as7265x_virtual_reg_read(ser, AS7265X_LED_CONFIG)
	if (status != True):
		return
	val &= 0b11111001
	val |= (current << 1)
	as7265x_select_device(ser, AS72651_NIR)
	as7265x_virtual_reg_write(ser, AS7265X_LED_CONFIG, val)

def as7265x_set_integration_cycles(ser, cycles):
	as7265x_virtual_reg_write(ser, AS7265X_INTERGRATION_TIME, cycles)

def as7265x_set_gain(ser, gain):
	if (gain > 3):
		gain = 3
	(status, val) = as7265x_virtual_reg_read(ser, AS7265X_CONFIG)
	if (status != True):
		return
	val &= 0b11001111
	val |= (gain << 4)
	as7265x_virtual_reg_write(ser, AS7265X_CONFIG, val)

def as7265x_set_measurement_mode(ser, mode):
	if (mode > 3):
		mode = 3
	(status, val) = as7265x_virtual_reg_read(ser, AS7265X_CONFIG)
	if (status != True):
		return
	val &= 0b11110011
	val |= (mode << 2)
	as7265x_virtual_reg_write(ser, AS7265X_CONFIG, val)

def as7265x_enable_interrupt(ser):
	(status, val) = as7265x_virtual_reg_read(ser, AS7265X_CONFIG)
	if (status != True):
		return
	val |= (1 << 6)
	as7265x_virtual_reg_write(ser, AS7265X_CONFIG, val)

def as7265x_disable_interrupt(ser):
	(status, val) = as7265x_virtual_reg_read(ser, AS7265X_CONFIG)
	if (status != True):
		return
	val &= ~(1 << 6)
	as7265x_virtual_reg_write(ser, AS7265X_CONFIG, val)

def as7265x_get_temperature(ser, device):
	as7265x_select_device(ser, device)
	(status, val) = as7265x_virtual_reg_read(ser, AS7265X_DEVICE_TEMP)
	return (status, val)

def as7265x_get_temperature_avg(ser):
	f_temp = 0.0
	for dev in range(0, 2):
		(status, temp_i) = as7265x_get_temperature(ser, dev)
		if (status != True):
			return (False, 0)
		f_temp += temp_i
	return (status, f_temp)

def as7265x_get_channel_val16(ser, channel_reg, device):
	as7265x_select_device(ser, device)
	(status, val) = as7265x_virtual_reg_read(ser, channel_reg)
	if (status != True):
		return (False, 0)
	val16 = val << 8
	(status, val) = as7265x_virtual_reg_read(ser, channel_reg + 1)
	if (status != True):
		return (False, 0)
	val16 |= val
	return (True, val16)

def as7265x_get_device_type(ser):
	(status, val) = as7265x_virtual_reg_read(ser, AS7265X_HW_VERSION_HIGH)
	if (status != True):
		return (False, 0)
	return (True, val)

def as7265x_get_hardware_version(ser):
	(status, val) = as7265x_virtual_reg_read(ser, AS7265X_HW_VERSION_LOW)
	if (status != True):
		return (False, 0)
	return (True, val)

def as7265x_get_major_firmware_version(ser):
	status = as7265x_virtual_reg_write(ser, AS7265X_FW_VERSION_HIGH, 0x01)
	if (status != True):
		return (False, 0)
	status = as7265x_virtual_reg_write(ser, AS7265X_FW_VERSION_LOW, 0x01)
	if (status != True):
		return (False, 0)
	(status, val) = as7265x_virtual_reg_read(ser, AS7265X_FW_VERSION_LOW)
	if (status != True):
		return (False, 0)
	return (True, val)

def as7265x_get_patch_firmware_version(ser):
	status = as7265x_virtual_reg_write(ser, AS7265X_FW_VERSION_HIGH, 0x02)
	if (status != True):
		return (False, 0)
	status = as7265x_virtual_reg_write(ser, AS7265X_FW_VERSION_LOW, 0x02)
	if (status != True):
		return (False, 0)
	(status, val) = as7265x_virtual_reg_read(ser, AS7265X_FW_VERSION_LOW)
	if (status != True):
		return (False, 0)
	return (True, val)

def as7265x_get_build_firmware_version(ser):
	status = as7265x_virtual_reg_write(ser, AS7265X_FW_VERSION_HIGH, 0x03)
	if (status != True):
		return (False, 0)
	status = as7265x_virtual_reg_write(ser, AS7265X_FW_VERSION_LOW, 0x03)
	if (status != True):
		return (False, 0)
	(status, val) = as7265x_virtual_reg_read(ser, AS7265X_FW_VERSION_LOW)
	if (status != True):
		return (False, 0)
	return (True, val)

def as7265x_is_data_available(ser):
	(status, val) = as7265x_virtual_reg_read(ser, AS7265X_CONFIG)
	val = ((val >> 1) & 0x01)
	return (status, val)

def as7265x_take_measurements(ser):
	as7265x_set_measurement_mode(ser, AS7265X_MEASUREMENT_MODE_6CHAN_ONE_SHOT)
	while (as7265x_is_data_available(ser) == False):
		time.sleep(AS7265X_POLLING_DELAY)

def as7265x_take_measurements_with_bulb(ser):
	as7265x_enable_bulb(ser, AS7265x_LED_WHITE)
	as7265x_enable_bulb(ser, AS7265x_LED_IR)
	as7265x_enable_bulb(ser, AS7265x_LED_UV)
	as7265x_take_measurements(ser)
	as7265x_disable_bulb(ser, AS7265x_LED_WHITE)
	as7265x_disable_bulb(ser, AS7265x_LED_IR)
	as7265x_disable_bulb(ser, AS7265x_LED_UV)

def as7265x_get_raw_g(ser):
	(status, val) = as7265x_get_channel_val16(ser, AS7265X_R_G_A, AS72652_VISIBLE)
	if (status != True):
		return (False, 0)
	return (True, val)

def as7265x_get_raw_h(ser):
	(status, val) = as7265x_get_channel_val16(ser, AS7265X_S_H_B, AS72652_VISIBLE)
	if (status != True):
		return (False, 0)
	return (True, val)

def as7265x_get_raw_i(ser):
	(status, val) = as7265x_get_channel_val16(ser, AS7265X_T_I_C, AS72652_VISIBLE)
	if (status != True):
		return (False, 0)
	return (True, val)

def as7265x_get_raw_j(ser):
	(status, val) = as7265x_get_channel_val16(ser, AS7265X_U_J_D, AS72652_VISIBLE)
	if (status != True):
		return (False, 0)
	return (True, val)

def as7265x_get_raw_k(ser):
	(status, val) = as7265x_get_channel_val16(ser, AS7265X_V_K_E, AS72652_VISIBLE)
	if (status != True):
		return (False, 0)
	return (True, val)

def as7265x_get_raw_l(ser):
	(status, val) = as7265x_get_channel_val16(ser, AS7265X_W_L_F, AS72652_VISIBLE)
	if (status != True):
		return (False, 0)
	return (True, val)

def as7265x_get_raw_r(ser):
	(status, val) = as7265x_get_channel_val16(ser, AS7265X_R_G_A, AS72651_NIR)
	if (status != True):
		return (False, 0)
	return (True, val)

def as7265x_get_raw_s(ser):
	(status, val) = as7265x_get_channel_val16(ser, AS7265X_S_H_B, AS72651_NIR)
	if (status != True):
		return (False, 0)
	return (True, val)

def as7265x_get_raw_t(ser):
	(status, val) = as7265x_get_channel_val16(ser, AS7265X_T_I_C, AS72651_NIR)
	if (status != True):
		return (False, 0)
	return (True, val)

def as7265x_get_raw_u(ser):
	(status, val) = as7265x_get_channel_val16(ser, AS7265X_U_J_D, AS72651_NIR)
	if (status != True):
		return (False, 0)
	return (True, val)

def as7265x_get_raw_v(ser):
	(status, val) = as7265x_get_channel_val16(ser, AS7265X_V_K_E, AS72651_NIR)
	if (status != True):
		return (False, 0)
	return (True, val)

def as7265x_get_raw_w(ser):
	(status, val) = as7265x_get_channel_val16(ser, AS7265X_W_L_F, AS72651_NIR)
	if (status != True):
		return (False, 0)
	return (True, val)

def as7265x_get_raw_a(ser):
	(status, val) = as7265x_get_channel_val16(ser, AS7265X_R_G_A, AS72653_UV)
	if (status != True):
		return (False, 0)
	return (True, val)

def as7265x_get_raw_b(ser):
	(status, val) = as7265x_get_channel_val16(ser, AS7265X_S_H_B, AS72653_UV)
	if (status != True):
		return (False, 0)
	return (True, val)

def as7265x_get_raw_c(ser):
	(status, val) = as7265x_get_channel_val16(ser, AS7265X_T_I_C, AS72653_UV)
	if (status != True):
		return (False, 0)
	return (True, val)

def as7265x_get_raw_d(ser):
	(status, val) = as7265x_get_channel_val16(ser, AS7265X_U_J_D, AS72653_UV)
	if (status != True):
		return (False, 0)
	return (True, val)

def as7265x_get_raw_e(ser):
	(status, val) = as7265x_get_channel_val16(ser, AS7265X_V_K_E, AS72653_UV)
	if (status != True):
		return (False, 0)
	return (True, val)

def as7265x_get_raw_f(ser):
	(status, val) = as7265x_get_channel_val16(ser, AS7265X_W_L_F, AS72653_UV)
	if (status != True):
		return (False, 0)
	return (True, val)

def as7265x_initialize(ser):
	as7265x_set_bulb_current(ser, AS7265X_LED_CURRENT_LIMIT_12_5MA, AS7265x_LED_WHITE)
	as7265x_set_bulb_current(ser, AS7265X_LED_CURRENT_LIMIT_12_5MA, AS7265x_LED_IR)
	as7265x_set_bulb_current(ser, AS7265X_LED_CURRENT_LIMIT_12_5MA, AS7265x_LED_UV)
	as7265x_disable_bulb(ser, AS7265x_LED_WHITE)
	as7265x_disable_bulb(ser, AS7265x_LED_IR)
	as7265x_disable_bulb(ser, AS7265x_LED_UV)
	as7265x_set_indicator_current(ser, AS7265X_INDICATOR_CURRENT_LIMIT_8MA)
	as7265x_enable_indicator(ser)
	as7265x_set_integration_cycles(ser, 49) # 50 * 2.8ms = 140ms. 0 to 255 is valid. 
	as7265x_set_gain(ser, AS7265X_GAIN_64X)
	as7265x_set_measurement_mode(ser, AS7265X_MEASUREMENT_MODE_6CHAN_ONE_SHOT)
	as7265x_enable_interrupt(ser)

def usb2io_command(ser, command):
	ser.write(command)
	time.sleep(0.05)
	rrd = ser.readline()
	print (rrd)

#---- Application ---------------------------------------------------------
print "===================================="
print "* AS7265x test"
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

if allow_load_fpga :
    # Transfer FPGA image to board
    print "Update FPGA image using RAWX protocol"
    wro = ser.write("fpga rawload\r\n")
    time.sleep(0.1)
    rrd = ser.readline()
    print(rrd)
    rawstream = RAWXT()
    rawstream.send_raw_file(fpga_filename, ser)
    time.sleep(0.1)
    rrd = ser.readline()
    print(rrd)

# Set Ext voltage to 3.3V
print "Configure EXT voltage to 3.3V"
usb2io_command(ser, "expv write 3300\r\n")

print "Configure I2C: Set 100KHz clock"
usb2io_command(ser, "i2c configure 0\r\n")
    
print "Scan I2C bus"
usb2io_command(ser, "i2c scan\r\n")

print "Reset AMS device"
as7265x_soft_reset(ser)
time.sleep(1.4)

print "Initialize AMS device"
as7265x_initialize(ser)

(status, val) = as7265x_get_device_type(ser)
if (status == True):
    print "AMS Device Type: " + hex(val)
else:
    print "Fail to communicate"

(status, val) = as7265x_get_major_firmware_version(ser)
if (status == True):
    print "AMS Major Firmware Version: " + hex(val)
else:
    print "Fail to communicate"

(status, val) = as7265x_get_patch_firmware_version(ser)
if (status == True):
    print "AMS Patch Firmware Version: " + hex(val)
else:
    print "Fail to communicate"

(status, val) = as7265x_get_build_firmware_version(ser)
if (status == True):
    print "AMS Build Firmware Version: " + hex(val)
else:
    print "Fail to communicate"

(status, val) = as7265x_get_temperature(ser, 0)
if (status == True):
    print "Main IC temp: " + str(val)
else:
    print "Fail to communicate"

(status, val) = as7265x_get_temperature_avg(ser)
if (status == True):
    print "Average IC temp: " + str(val)
else:
    print "Fail to communicate"

print "Disable indicator"
as7265x_disable_indicator(ser)

print "Take measurements"
as7265x_take_measurements_with_bulb(ser)

(status, val) = as7265x_get_raw_a(ser)
if (status == True):
    print "Raw A value: " + str(val)
else:
    print "Fail to communicate"

(status, val) = as7265x_get_raw_b(ser)
if (status == True):
    print "Raw B value: " + str(val)
else:
    print "Fail to communicate"

(status, val) = as7265x_get_raw_c(ser)
if (status == True):
    print "Raw C value: " + str(val)
else:
    print "Fail to communicate"

(status, val) = as7265x_get_raw_d(ser)
if (status == True):
    print "Raw D value: " + str(val)
else:
    print "Fail to communicate"

(status, val) = as7265x_get_raw_e(ser)
if (status == True):
    print "Raw E value: " + str(val)
else:
    print "Fail to communicate"

(status, val) = as7265x_get_raw_f(ser)
if (status == True):
    print "Raw F value: " + str(val)
else:
    print "Fail to communicate"

(status, val) = as7265x_get_raw_g(ser)
if (status == True):
    print "Raw G value: " + str(val)
else:
    print "Fail to communicate"

(status, val) = as7265x_get_raw_h(ser)
if (status == True):
    print "Raw H value: " + str(val)
else:
    print "Fail to communicate"

(status, val) = as7265x_get_raw_i(ser)
if (status == True):
    print "Raw I value: " + str(val)
else:
    print "Fail to communicate"

(status, val) = as7265x_get_raw_j(ser)
if (status == True):
    print "Raw J value: " + str(val)
else:
    print "Fail to communicate"

(status, val) = as7265x_get_raw_k(ser)
if (status == True):
    print "Raw K value: " + str(val)
else:
    print "Fail to communicate"

(status, val) = as7265x_get_raw_l(ser)
if (status == True):
    print "Raw L value: " + str(val)
else:
    print "Fail to communicate"

(status, val) = as7265x_get_raw_r(ser)
if (status == True):
    print "Raw R value: " + str(val)
else:
    print "Fail to communicate"

(status, val) = as7265x_get_raw_s(ser)
if (status == True):
    print "Raw S value: " + str(val)
else:
    print "Fail to communicate"

(status, val) = as7265x_get_raw_t(ser)
if (status == True):
    print "Raw T value: " + str(val)
else:
    print "Fail to communicate"

(status, val) = as7265x_get_raw_u(ser)
if (status == True):
    print "Raw U value: " + str(val)
else:
    print "Fail to communicate"

(status, val) = as7265x_get_raw_v(ser)
if (status == True):
    print "Raw V value: " + str(val)
else:
    print "Fail to communicate"

(status, val) = as7265x_get_raw_w(ser)
if (status == True):
    print "Raw W value: " + str(val)
else:
    print "Fail to communicate"

# Close serial port
ser.close()
print "API test done" 