#=====================================================
#  I2C functional test
#
#
#=====================================================
import os
import sys
import time
import serial
import select
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from usb2io import usb2io_sendcmd

COM_PORT_ENG                = 'COM166'

APDS9960_I2C_ADDR       = 0x39

GESTURE_THRESHOLD_OUT   = 10
GESTURE_SENSITIVITY_1   = 50
GESTURE_SENSITIVITY_2   = 20

APDS9960_ERROR          = 0xFF

APDS9960_ID_1           = 0xAB
APDS9960_ID_2           = 0x9C

FIFO_PAUSE_TIME         = 30 # Wait period (ms) between FIFO reads

APDS9960_ENABLE         = 0x80
APDS9960_ATIME          = 0x81
APDS9960_WTIME          = 0x83
APDS9960_AILTL          = 0x84
APDS9960_AILTH          = 0x85
APDS9960_AIHTL          = 0x86
APDS9960_AIHTH          = 0x87
APDS9960_PILT           = 0x89
APDS9960_PIHT           = 0x8B
APDS9960_PERS           = 0x8C
APDS9960_CONFIG1        = 0x8D
APDS9960_PPULSE         = 0x8E
APDS9960_CONTROL        = 0x8F
APDS9960_CONFIG2        = 0x90
APDS9960_ID             = 0x92
APDS9960_STATUS         = 0x93
APDS9960_CDATAL         = 0x94
APDS9960_CDATAH         = 0x95
APDS9960_RDATAL         = 0x96
APDS9960_RDATAH         = 0x97
APDS9960_GDATAL         = 0x98
APDS9960_GDATAH         = 0x99
APDS9960_BDATAL         = 0x9A
APDS9960_BDATAH         = 0x9B
APDS9960_PDATA          = 0x9C
APDS9960_POFFSET_UR     = 0x9D
APDS9960_POFFSET_DL     = 0x9E
APDS9960_CONFIG3        = 0x9F
APDS9960_GPENTH         = 0xA0
APDS9960_GEXTH          = 0xA1
APDS9960_GCONF1         = 0xA2
APDS9960_GCONF2         = 0xA3
APDS9960_GOFFSET_U      = 0xA4
APDS9960_GOFFSET_D      = 0xA5
APDS9960_GOFFSET_L      = 0xA7
APDS9960_GOFFSET_R      = 0xA9
APDS9960_GPULSE         = 0xA6
APDS9960_GCONF3         = 0xAA
APDS9960_GCONF4         = 0xAB
APDS9960_GFLVL          = 0xAE
APDS9960_GSTATUS        = 0xAF
APDS9960_IFORCE         = 0xE4
APDS9960_PICLEAR        = 0xE5
APDS9960_CICLEAR        = 0xE6
APDS9960_AICLEAR        = 0xE7
APDS9960_GFIFO_U        = 0xFC
APDS9960_GFIFO_D        = 0xFD
APDS9960_GFIFO_L        = 0xFE
APDS9960_GFIFO_R        = 0xFF


APDS9960_PON            = 0b00000001
APDS9960_AEN            = 0b00000010
APDS9960_PEN            = 0b00000100
APDS9960_WEN            = 0b00001000
APSD9960_AIEN           = 0b00010000
APDS9960_PIEN           = 0b00100000
APDS9960_GEN            = 0b01000000
APDS9960_GVALID         = 0b00000001

#/* On/Off definitions */
APDS9960_OFF            = 0
APDS9960_ON             = 1

#/* Acceptable parameters for setMode */
APDS9960_POWER                   = 0
APDS9960_AMBIENT_LIGHT           = 1
APDS9960_PROXIMITY               = 2
APDS9960_WAIT                    = 3
APDS9960_AMBIENT_LIGHT_INT       = 4
APDS9960_PROXIMITY_INT           = 5
APDS9960_GESTURE                 = 6
APDS9960_ALL                     = 7

#/* LED Drive values */
LED_DRIVE_100MA         = 0
LED_DRIVE_50MA          = 1
LED_DRIVE_25MA          = 2
LED_DRIVE_12_5MA        = 3

#/* Proximity Gain (PGAIN) values */
PGAIN_1X                = 0
PGAIN_2X                = 1
PGAIN_4X                = 2
PGAIN_8X                = 3

#/* ALS Gain (AGAIN) values */
AGAIN_1X                = 0
AGAIN_4X                = 1
AGAIN_16X               = 2
AGAIN_64X               = 3

#/* Gesture Gain (GGAIN) values */
GGAIN_1X                = 0
GGAIN_2X                = 1
GGAIN_4X                = 2
GGAIN_8X                = 3

#/* LED Boost values */
LED_BOOST_100           = 0
LED_BOOST_150           = 1
LED_BOOST_200           = 2
LED_BOOST_300           = 3

#/* Gesture wait time values */
GWTIME_0MS              = 0
GWTIME_2_8MS            = 1
GWTIME_5_6MS            = 2
GWTIME_8_4MS            = 3
GWTIME_14_0MS           = 4
GWTIME_22_4MS           = 5
GWTIME_30_8MS           = 6
GWTIME_39_2MS           = 7

#/* Default values */
DEFAULT_ATIME           = 219     #// 103ms
DEFAULT_WTIME           = 246     #// 2.78ms
DEFAULT_PROX_PPULSE     = 0x87    #// 16us, 8 pulses
DEFAULT_GESTURE_PPULSE  = 0x89    #// 32us, 3 pulses
DEFAULT_POFFSET_UR      = 0       #// 0 offset
DEFAULT_POFFSET_DL      = 0       #// 0 offset
DEFAULT_CONFIG1         = 0x60    #// No 12x wait (WTIME) factor
DEFAULT_LDRIVE          = LED_DRIVE_100MA
DEFAULT_PGAIN           = PGAIN_4X
DEFAULT_AGAIN           = AGAIN_4X
DEFAULT_PILT            = 0       #// Low proximity threshold
DEFAULT_PIHT            = 255     #// High proximity threshold 50
DEFAULT_AILT            = 0xFFFF  #// Force interrupt for calibration
DEFAULT_AIHT            = 0
DEFAULT_PERS            = 0x11    #// 2 consecutive prox or ALS for int.
DEFAULT_CONFIG2         = 0x01    #// No saturation interrupts or LED boost
DEFAULT_CONFIG3         = 0       #// Enable all photodiodes, no SAI
DEFAULT_GPENTH          = 55      #// Threshold for entering gesture mode 40
DEFAULT_GEXTH           = 30      #// Threshold for exiting gesture mode    30
DEFAULT_GCONF1          = 0x40    #// 4 gesture events for int., 1 for exit
DEFAULT_GGAIN           = GGAIN_4X
DEFAULT_GLDRIVE         = LED_DRIVE_100MA
DEFAULT_GWTIME          = GWTIME_2_8MS
DEFAULT_GOFFSET         = 0       #// No offset scaling for gesture mode
DEFAULT_GPULSE          = 0xC9    #// 32us, 10 pulses
DEFAULT_GCONF3          = 0       #// All photodiodes active during gesture
DEFAULT_GIEN            = 0       #// Disable gesture interrupts
DEFAULT_BOOSTLED        = LED_BOOST_300


def APDS9960_WrByte(ser, reg, data):
	strx = "i2c write 1,0x39," + hex(reg & 0xFF) + ","+ hex(data & 0xFF) + "\r\n"
	usb2io_sendcmd(ser,strx,1)

def APDS9960_WrWord(ser, reg, data):
	strx = "i2c write 1,0x39," + hex(reg & 0xFF) + ","+ hex((data >> 8) & 0xFF) + ","+ hex(data & 0xFF) + "\r\n"
	usb2io_sendcmd(ser,strx,1)

def APDS9960_WrDWord(ser, reg, data):
	strx = "i2c write 1,0x39," + hex(reg & 0xFF) + ","+ hex((data >> 24) & 0xFF) + ","+ hex((data >> 16) & 0xFF) + ","+ hex((data >> 8) & 0xFF) + ","+ hex(data & 0xFF) + "\r\n"
	usb2io_sendcmd(ser,strx,1)

def APDS9960_RdByte(ser, reg):
	strx = "i2c write 1,0x39," + hex(reg & 0xFF) + "\r\n"
	usb2io_sendcmd(ser,strx,1)
	strx = "i2c read 1,0x39,1\r\n"
	rrd = usb2io_sendcmd(ser,strx,1)
	if (rrd.find("OK,", 0, 3) != -1):
		bytes_str = rrd[3:]
		return (True, int(bytes_str, 16))
	return (False, 0)

def APDS9960_RdWord(ser, reg):
	strx = "i2c write 1,0x39," + hex(reg & 0xFF) + "\r\n"
	usb2io_sendcmd(ser,strx,1)
	strx = "i2c read 1,0x39,2\r\n"
	rrd = usb2io_sendcmd(ser,strx,1)
	if (rrd.find('FAIL') != -1):
		return (False, 0)
	ba1 = [int(i,16) for i in rrd.replace('OK,', '').split(',')]
	wval = (ba1[0] << 8) | ba1[1]
	return (True, wval)

def APDS9960_RdDWord(ser, reg):
	strx = "i2c write 1,0x39," + hex(reg & 0xFF) + "\r\n"
	rrd = usb2io_sendcmd(ser,strx,1)
	strx = "i2c read 1,0x39,4\r\n"
	rrd = usb2io_sendcmd(ser,strx,1)
	if (rrd.find('FAIL') != -1):
		return (False, 0)
	ba1 = [int(i,16) for i in rrd.replace('OK,', '').split(',')]
	dwval = (ba1[0] << 24) | (ba1[1] << 16) | (ba1[2] << 8) | ba1[3]
	return (True, dwval)

def APDS9960_ReadMulti(ser, reg, count):
	strx = "i2c write 1,0x39," + hex(reg & 0xFF) + "\r\n"
	usb2io_sendcmd(ser,strx,1)
	strx = "i2c read 1,0x39," + str(count) + "\r\n"
	rrd = usb2io_sendcmd(ser,strx,1)
	ba1 = [int(i,16) for i in rrd.replace('OK,', '').split(',')]
	return (ba1)

def APDS9960_getLEDDrive(ser):
	(status, val8) = APDS9960_RdByte(ser, APDS9960_CONTROL)
	val8 = (val8 >> 6) & 0x03
	return (status, val8)

def APDS9960_setLEDDrive(ser, drive):
	(status) = APDS9960_WrByte(ser, APDS9960_CONTROL, drive)
	val8 = (val8 >> 6) & 0x03
	return (status, val8)

def APDS9960_getMode(ser):
	(status, val8) = APDS9960_RdByte(ser, APDS9960_ENABLE)
	return (status, val8)

def APDS9960_setMode(ser, mode, enable):
	(status, val8) = APDS9960_getMode(ser)
	if (status != True):
		return False
	enable = enable & 0x01
	if ((mode >= 0) and (mode <= 6)):
		if (enable):
			val8 |= ( 1 << mode )
		else:
			val8 &= ~( 1 << mode )
	elif (mode == APDS9960_ALL):
		if (enable):
			val8 = 0x7F
		else:
			val8 = 0
	APDS9960_WrByte(ser, APDS9960_ENABLE, val8)
	return True

def APDS9960_setLEDBoost(ser, boost):
	(status, val8) = APDS9960_RdByte(ser, APDS9960_CONFIG2)
	if (status != True):
		return
	boost &= 0b00000011
	boost = boost << 4
	val8 &= 0b11001111
	val8 |= boost
	APDS9960_WrByte(ser, APDS9960_CONFIG2, val8)
	return

def APDS9960_getLEDBoost(ser, boost):
	(status, val8) = APDS9960_RdByte(ser, APDS9960_CONFIG2)
	if (status != True):
		return 0
	val8 = (val8 >> 4) & 0b00000011
	return val8

def APDS9960_setProximityGain(ser, drive):
	(status, val8) = APDS9960_RdByte(ser, APDS9960_CONTROL)
	if (status != True):
		return
	drive &= 0b00000011
	drive = drive << 2
	val8 &= 0b11110011
	val8 |= drive
	APDS9960_WrByte(ser, APDS9960_CONTROL, val8)
	return

def APDS9960_setAmbientLightGain(ser, drive):
	(status, val8) = APDS9960_RdByte(ser, APDS9960_CONTROL)
	if (status != True):
		return
	drive &= 0b00000011
	val8 &= 0b11111100
	val8 |= drive
	APDS9960_WrByte(ser, APDS9960_CONTROL, val8)
	return

def APDS9960_setProxIntLowThresh(ser, threshold):
	APDS9960_WrByte(ser, APDS9960_PILT, threshold)
	return

def APDS9960_setProxIntHighThresh(ser, threshold):
	APDS9960_WrByte(ser, APDS9960_PIHT, threshold)
	return

def APDS9960_setGestureEnterThresh(ser, threshold):
	APDS9960_WrByte(ser, APDS9960_GPENTH, threshold)
	return

def APDS9960_setGestureExitThresh(ser, threshold):
	APDS9960_WrByte(ser, APDS9960_GEXTH, threshold)
	return

def APDS9960_setLightIntLowThreshold(ser, threshold):
	val_low = threshold & 0x00FF
	val_high = (threshold & 0xFF00) >> 8
	APDS9960_WrByte(ser, APDS9960_AILTL, val_low)
	APDS9960_WrByte(ser, APDS9960_AILTH, val_high)
	return

def APDS9960_setLightIntHighThreshold(ser, threshold):
	val_low = threshold & 0x00FF
	val_high = (threshold & 0xFF00) >> 8
	APDS9960_WrByte(ser, APDS9960_AIHTL, val_low)
	APDS9960_WrByte(ser, APDS9960_AIHTH, val_high)
	return

def APDS9960_setGestureGain(ser, gain):
	(status, val8) = APDS9960_RdByte(ser, APDS9960_GCONF2)
	if (status != True):
		return
	gain &= 0b00000011
	gain = gain << 5
	val8 &= 0b10011111
	val8 |= gain
	APDS9960_WrByte(ser, APDS9960_GCONF2, val8)
	return

def APDS9960_setGestureLEDDrive(ser, drive):
	(status, val8) = APDS9960_RdByte(ser, APDS9960_GCONF2)
	if (status != True):
		return
	drive &= 0b00000011
	drive = drive << 3
	val8 &= 0b11100111
	val8 |= drive
	APDS9960_WrByte(ser, APDS9960_GCONF2, val8)
	return

def APDS9960_setGestureWaitTime(ser, time):
	(status, val8) = APDS9960_RdByte(ser, APDS9960_GCONF2)
	if (status != True):
		return
	time &= 0b00000111
	val8 &= 0b11111000
	val8 |= time
	APDS9960_WrByte(ser, APDS9960_GCONF2, val8)
	return

def APDS9960_setGestureIntEnable(ser, enable):
	(status, val8) = APDS9960_RdByte(ser, APDS9960_GCONF4)
	if (status != True):
		return
	enable &= 0b00000001
	enable = enable << 1
	val8 &= 0b11111101
	val8 |= enable
	APDS9960_WrByte(ser, APDS9960_GCONF4, val8)
	return

def APDS9960_setGestureMode(ser, mode):
	(status, val8) = APDS9960_RdByte(ser, APDS9960_GCONF4)
	if (status != True):
		return
	mode &= 0b00000001
	val8 &= 0b11111110
	val8 |= mode
	APDS9960_WrByte(ser, APDS9960_GCONF4, val8)
	return

def APDS9960_setProxIntLowThresh(ser, threshold):
	APDS9960_setMode(ser, APDS9960_PILT, threshold)
	return

def APDS9960_enablePower(ser):
	APDS9960_setMode(ser, APDS9960_POWER, 1)
	return

def APDS9960_init(ser):
	print ("APDS9960_init+")
	APDS9960_setMode(ser, APDS9960_ALL, APDS9960_OFF)
	APDS9960_WrByte(ser, APDS9960_ATIME, DEFAULT_ATIME)
	APDS9960_WrByte(ser, APDS9960_WTIME, DEFAULT_WTIME)
	APDS9960_WrByte(ser, APDS9960_PPULSE, DEFAULT_PROX_PPULSE)
	APDS9960_WrByte(ser, APDS9960_POFFSET_UR, DEFAULT_POFFSET_UR)
	APDS9960_WrByte(ser, APDS9960_POFFSET_DL, DEFAULT_POFFSET_DL)
	APDS9960_WrByte(ser, APDS9960_CONFIG1, DEFAULT_CONFIG1)
	APDS9960_setLEDBoost(ser, DEFAULT_LDRIVE)
	APDS9960_setProximityGain(ser, DEFAULT_PGAIN)
	APDS9960_setAmbientLightGain(ser, DEFAULT_AGAIN)
	APDS9960_setProxIntLowThresh(ser, DEFAULT_PILT)
	APDS9960_setProxIntHighThresh(ser, DEFAULT_PIHT)
	APDS9960_setLightIntLowThreshold(ser, DEFAULT_AILT)
	APDS9960_setLightIntHighThreshold(ser, DEFAULT_AIHT)
	APDS9960_WrByte(ser, APDS9960_PERS, DEFAULT_PERS)
	APDS9960_WrByte(ser, APDS9960_CONFIG2, DEFAULT_CONFIG2)
	APDS9960_WrByte(ser, APDS9960_CONFIG3, DEFAULT_CONFIG3)
	APDS9960_setGestureEnterThresh(ser, DEFAULT_GPENTH)
	APDS9960_setGestureExitThresh(ser, DEFAULT_GEXTH)
	APDS9960_WrByte(ser, APDS9960_GCONF1, DEFAULT_GCONF1)
	APDS9960_setGestureGain(ser, DEFAULT_GGAIN)
	APDS9960_setGestureLEDDrive(ser, DEFAULT_GLDRIVE)
	APDS9960_setGestureWaitTime(ser, DEFAULT_GWTIME)
	APDS9960_WrByte(ser, APDS9960_GOFFSET_U, DEFAULT_GOFFSET)
	APDS9960_WrByte(ser, APDS9960_GOFFSET_D, 0b10001111)
	APDS9960_WrByte(ser, APDS9960_GOFFSET_L, 0b10001111)
	APDS9960_WrByte(ser, APDS9960_GOFFSET_R, DEFAULT_GOFFSET)
	APDS9960_WrByte(ser, APDS9960_GPULSE, DEFAULT_GPULSE)
	APDS9960_WrByte(ser, APDS9960_GCONF3, DEFAULT_GCONF3)
	APDS9960_setGestureIntEnable(ser, DEFAULT_GIEN)
	print ("APDS9960_init-" )

def APDS9960_enableGestureSensor(ser, interrupts):
	print ("APDS9960_enableGestureSensor+" )
	# Enable gesture mode
	# Set ENABLE to 0 (power off)
	# Set WTIME to 0xFF
	# Set AUX to LED_BOOST_300
	# Enable PON, WEN, PEN, GEN in ENABLE
	APDS9960_WrByte(ser, APDS9960_WTIME, 0xFF)
	APDS9960_WrByte(ser, APDS9960_PPULSE, DEFAULT_GESTURE_PPULSE)
	APDS9960_setLEDBoost(ser, DEFAULT_BOOSTLED)
	if (interrupts):
		APDS9960_setGestureIntEnable(ser, 1)
	else:
		APDS9960_setGestureIntEnable(ser, 0)
	APDS9960_setGestureMode(ser, 1)
	APDS9960_enablePower(ser)
	APDS9960_setMode(ser, APDS9960_WAIT, 1)
	APDS9960_setMode(ser, APDS9960_PROXIMITY, 1)
	APDS9960_setMode(ser, APDS9960_GESTURE, 1)
	print ("APDS9960_enableGestureSensor-" )
	return True

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
	#Aquire and parse data from TOF sensor
	(status, gstatus) = APDS9960_RdByte(ser, APDS9960_GSTATUS)
	if ( (gstatus & APDS9960_GVALID) == APDS9960_GVALID ):
		(status, fifo_level) = APDS9960_RdByte(ser, APDS9960_GFLVL)
		if ( fifo_level > 0 ):
			if (fifo_level > 8):
				fifo_level = 8
			ba = APDS9960_ReadMulti(ser, APDS9960_GFIFO_U, fifo_level * 4)
			print ("Fifo: " + str(fifo_level))
			for x in range(fifo_level):
				print (hex(ba[(x * 4) + 0]) + "," + hex(ba[(x * 4) + 1]) + "," + hex(ba[(x * 4) + 2]) + "," + hex(ba[(x * 4) + 3]))
				img = np.array(ba)
				img.shape = (fifo_level, 4)
#				c = ax.clear()
				c = ax.pcolormesh(img)

#---- Application ---------------------------------------------------------
print ("====================================")
print ("* I2C APDS9960 test")
print ("====================================")

local_com_port = sys.argv[1] if (len(sys.argv) > 1) else COM_PORT_ENG

# Open serial port
print ("Open serial port " + local_com_port)
try:
    ser = serial.Serial(local_com_port, 115200, timeout=3)
    print ("COM port OK" )
except:
    print ("Error COM port" )
    sys.exit(0)

#wro = ser.write("hello\r\n")
#time.sleep(0.1)
#rrd = ser.readline()
#print(rrd)

# Set Ext voltage to 0V
print ("Configure EXT voltage to 0V")
usb2io_sendcmd(ser, "expv write 0\r\n")
time.sleep(0.3)

# Set Ext voltage to 3.3V
print ("Configure EXT voltage to 3.3V")
usb2io_sendcmd(ser, "expv write 3300\r\n")

print ("Configure I2C: Set 400KHz clock")
usb2io_sendcmd(ser, "i2c configure 1,1\r\n")

#print "Scan I2C bus"
#wro = ser.write("i2c scan 1\r\n")
#time.sleep(0.1)
#rrd = ser.readline()
#print(rrd)

print ("Read version data")
(status, byteData) = APDS9960_RdByte(ser, APDS9960_ID)
print("APDS9960X Model_ID: " + hex(byteData) + "\r\n")

APDS9960_init(ser)
APDS9960_enableGestureSensor(ser, 1)

# Create figure for plotting
#fig = plt.figure()
#ax = fig.add_subplot(1, 1, 1)
#xs = []
#ys = []
#y2s = []
#y3s = []
#y4s = []
lsc_p0 = 0
while (False):
	(status, gstatus) = APDS9960_RdByte(ser, APDS9960_GSTATUS)
	if ( (gstatus & APDS9960_GVALID) == APDS9960_GVALID ):
		(status, fifo_level) = APDS9960_RdByte(ser, APDS9960_GFLVL)
		if ( fifo_level > 0 ):
			ba = APDS9960_ReadMulti(ser, APDS9960_GFIFO_U, fifo_level * 4)
			if (lsc_p0 != 0):
				lsc_p0 = 0
				print ("---")
			#print ("Fifo: " + str(fifo_level))
			for x in range(fifo_level):
				stro = hex(ba[(x * 4) + 0]) + "," + hex(ba[(x * 4) + 1]) + "," + hex(ba[(x * 4) + 2]) + "," + hex(ba[(x * 4) + 3])
				print (stro.replace('0x',''))
	else:
		lsc_p0 = 1

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []
print ("Start process")

fig.tight_layout()
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1)
plt.show()

# Close serial port
ser.close()
print ("App exit" )
