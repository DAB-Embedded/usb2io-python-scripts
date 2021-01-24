from usb2io import usb2io_sendcmd
import time
import struct



    
AS7265X_ADDR = 0x49 #7-bit unshifted default I2C Address

AS7265X_STATUS_REG  = 0x00
AS7265X_WRITE_REG = 0X01
AS7265X_READ_REG = 0x02

AS7265X_TX_VALID = 0x02
AS7265X_RX_VALID = 0x01

#Register addresses
AS7265X_HW_VERSION_HIGH = 0x00
AS7265X_HW_VERSION_LOW = 0x01

AS7265X_FW_VERSION_HIGH = 0x02
AS7265X_FW_VERSION_LOW = 0x03

AS7265X_CONFIG = 0x04
AS7265X_INTERGRATION_TIME = 0x05
AS7265X_DEVICE_TEMP = 0x06
AS7265X_LED_CONFIG = 0x07

#Raw channel registers
AS7265X_R_G_A = 0x08
AS7265X_S_H_B = 0x0A
AS7265X_T_I_C = 0x0C
AS7265X_U_J_D = 0x0E
AS7265X_V_K_E = 0x10
AS7265X_W_L_F = 0x12

#Calibrated channel registers
AS7265X_R_G_A_CAL = 0x14
AS7265X_S_H_B_CAL = 0x18
AS7265X_T_I_C_CAL = 0x1C
AS7265X_U_J_D_CAL = 0x20
AS7265X_V_K_E_CAL = 0x24
AS7265X_W_L_F_CAL = 0x28

AS7265X_DEV_SELECT_CONTROL = 0x4F

AS7265X_COEF_DATA_0 = 0x50
AS7265X_COEF_DATA_1 = 0x51
AS7265X_COEF_DATA_2 = 0x52
AS7265X_COEF_DATA_3 = 0x53
AS7265X_COEF_DATA_READ = 0x54
AS7265X_COEF_DATA_WRITE = 0x55

#Settings 

AS7265X_POLLING_DELAY = 0.005 #Amount of ms to wait between checking for virtual register changes

AS72651_NIR = 0x00
AS72652_VISIBLE = 0x01
AS72653_UV = 0x02

AS7265x_LED_WHITE = 0x00 #White LED is connected to x51
AS7265x_LED_IR = 0x01 #IR LED is connected to x52
AS7265x_LED_UV = 0x02 #UV LED is connected to x53

AS7265X_LED_CURRENT_LIMIT_12_5MA = 0x00
AS7265X_LED_CURRENT_LIMIT_25MA = 0x01
AS7265X_LED_CURRENT_LIMIT_50MA = 0x02
AS7265X_LED_CURRENT_LIMIT_100MA = 0x03

AS7265X_INDICATOR_CURRENT_LIMIT_1MA = 0x00
AS7265X_INDICATOR_CURRENT_LIMIT_2MA = 0x01
AS7265X_INDICATOR_CURRENT_LIMIT_4MA = 0x02
AS7265X_INDICATOR_CURRENT_LIMIT_8MA = 0x03

AS7265X_GAIN_1X = 0x00
AS7265X_GAIN_37X = 0x01
AS7265X_GAIN_16X = 0x02
AS7265X_GAIN_64X = 0x03

AS7265X_MEASUREMENT_MODE_4CHAN = 0x00
AS7265X_MEASUREMENT_MODE_4CHAN_2 = 0x01
AS7265X_MEASUREMENT_MODE_6CHAN_CONTINUOUS = 0x02
AS7265X_MEASUREMENT_MODE_6CHAN_ONE_SHOT = 0x03

class AS7265x:
	#----------------------------------------------------------------------
	# constructor
    def __init__(self, ser):
        self.ser = ser  # set serial port
    #----------------------------------------------------------------------
    # Write a value to a spot in the AS726x
    def writeRegister(self, addr, val):
        if (usb2io_sendcmd(self.ser, "i2c write 1, " + str(AS7265X_ADDR) + ", " + str(addr) + ", " + str(val) + "\r\n", 1) == "OK\r\n"):
            return True
        return False
   
    #---------------------------------------------------------------------- 
    # Reads from a give location from the AS726x
    def readRegister(self, addr):
        # first set address
        if (usb2io_sendcmd(self.ser, "i2c write 1, " + str(AS7265X_ADDR) + ", " + str(addr) + "\r\n", 1) != "OK\r\n"):
            return False, 0
        rrd = usb2io_sendcmd(self.ser, "i2c read 1, " + str(AS7265X_ADDR) +", 1\r\n", 1)
        if (rrd.find("OK,", 0, 3) != -1):
		    # parse result
            bytes_str = rrd[3:]
            return True, int(bytes_str, 16) 		     
        return False, 0

    #---------------------------------------------------------------------- 
    #Write to a virtual register in the AS726x
    def virtualWriteRegister(self, virtualAddr, dataToWrite):
        
        #Wait for WRITE register to be empty
        while (1):  
            status = self.readRegister(AS7265X_STATUS_REG);
            if (status[0] != True):
                return False
            if ((status[1] & AS7265X_TX_VALID) == 0):
                break; # No inbound TX pending at slave. Okay to write now.
            time.sleep(AS7265X_POLLING_DELAY);
  
        # Send the virtual register address (setting bit 7 to indicate we are writing to a register).
        if (self.writeRegister(AS7265X_WRITE_REG, (virtualAddr | 1 << 7)) != True):
            return False

        #Wait for WRITE register to be empty
        while (1):
            status = self.readRegister(AS7265X_STATUS_REG);
            if (status[0] != True):
                return False
            if ((status[1] & AS7265X_TX_VALID) == 0):
                break; # No inbound TX pending at slave. Okay to write now.
            time.sleep(AS7265X_POLLING_DELAY);
        
        #Send the data to complete the operation.
        return self.writeRegister(AS7265X_WRITE_REG, dataToWrite)

    #---------------------------------------------------------------------- 
    # Read a virtual register from the AS7265x
    def virtualReadRegister(self, virtualAddr):

        #Do a prelim check of the read register
        status = self.readRegister(AS7265X_STATUS_REG);
        if (status[0] != True):
            return False, 0
        
        if ((status[1] & AS7265X_RX_VALID) != 0): #There is data to be read
            incoming = self.readRegister(AS7265X_READ_REG); #Read the byte but do nothing with it
        
        #Wait for WRITE flag to clear
        while (1):
            status = self.readRegister(AS7265X_STATUS_REG);
            if (status[0] != True):
                return False, 0
            if ((status[1] & AS7265X_TX_VALID) == 0):
                break; # If TX bit is clear, it is ok to write
            time.sleep(AS7265X_POLLING_DELAY);
        
        #Send the virtual register address (bit 7 should be 0 to indicate we are reading a register).
        if (self.writeRegister(AS7265X_WRITE_REG, virtualAddr) != True):
            return False, 0

        #Wait for READ flag to be set
        while (1):
            status = self.readRegister(AS7265X_STATUS_REG);
            if (status[0] != True):
                return False, 0

            if ((status[1] & AS7265X_RX_VALID) != 0):
                break; # Read data is ready.
            time.sleep(AS7265X_POLLING_DELAY);
        
        return self.readRegister(AS7265X_READ_REG);
      
    #----------------------------------------------------------------------   
    #As we read various registers we have to point at the master or first/second slave
    def selectDevice(self, device):
        #Set the bits 0:1. Just overwrite whatever is there because masking in the correct value doesn't work.
        virtualWriteRegister(AS7265X_DEV_SELECT_CONTROL, device)

    #----------------------------------------------------------------------   
    # get info
    def getDeviceType(self):
        return self.virtualReadRegister(AS7265X_HW_VERSION_HIGH)
    
    def getHardwareVersion(self):
        return self.virtualReadRegister(AS7265X_HW_VERSION_LOW)
    
    def getMajorFirmwareVersion(self):
        self.virtualWriteRegister(AS7265X_FW_VERSION_HIGH, 0x01) #Set to 0x01 for Major
        self.virtualWriteRegister(AS7265X_FW_VERSION_LOW, 0x01) #Set to 0x01 for Major  
        return self.virtualReadRegister(AS7265X_FW_VERSION_LOW)
    
    def getPatchFirmwareVersion(self):
    
        self.virtualWriteRegister(AS7265X_FW_VERSION_HIGH, 0x02)#Set to 0x02 for Patch
        self.virtualWriteRegister(AS7265X_FW_VERSION_LOW, 0x02) #Set to 0x02 for Patch
  
        return self.virtualReadRegister(AS7265X_FW_VERSION_LOW);
        
    def getBuildFirmwareVersion(self):
        self.virtualWriteRegister(AS7265X_FW_VERSION_HIGH, 0x03); #Set to 0x03 for Build
        self.virtualWriteRegister(AS7265X_FW_VERSION_LOW, 0x03); #Set to 0x03 for Build
        return self.virtualReadRegister(AS7265X_FW_VERSION_LOW)
    
    #----------------------------------------------------------------------   
    # Initializes the sensor with basic settings
    # Returns false if sensor is not detected
    def begin(self):
        
        #Check to see if both slaves are detected
        print('.')
        value = self.virtualReadRegister(AS7265X_DEV_SELECT_CONTROL);
        if (value[0] != True):
            return False
        print('.')
        if ( (value[1] & 0b00110000) == 0):
            return False #Test if Slave1 and 2 are detected. If not, bail.
        print('.')
        if (self.setBulbCurrent(AS7265X_LED_CURRENT_LIMIT_12_5MA, AS7265x_LED_WHITE) != True):
            return False
        print('.')
        if (self.setBulbCurrent(AS7265X_LED_CURRENT_LIMIT_12_5MA, AS7265x_LED_IR) != True):
            return False
        print('.')
        if (self.setBulbCurrent(AS7265X_LED_CURRENT_LIMIT_12_5MA, AS7265x_LED_UV) != True):
            return False
        print('.')
        if (self.disableBulb(AS7265x_LED_WHITE) != True):
            return False #Turn off bulb to avoid heating sensor
        print('.')
        if (self.disableBulb(AS7265x_LED_IR) != True):
            return False
        print('.')
        if (self.disableBulb(AS7265x_LED_UV) != True):
            return False
        print('.')
        if (self.setIndicatorCurrent(AS7265X_INDICATOR_CURRENT_LIMIT_8MA) != True):
            return False #Set to 8mA (maximum)
        print('.')
        if (self.enableIndicator() != True):
            return False
        print('.')
        if (self.setIntegrationCycles(49) != True):
            return False #50 * 2.8ms = 140ms. 0 to 255 is valid.
        #If you use Mode 2 or 3 (all the colors) then integration time is double. 140*2 = 280ms between readings.
        print('.')
        if (self.setGain(AS7265X_GAIN_64X) != True):
            return False #Set gain to 64x
        print('.')
        if (self.setMeasurementMode(AS7265X_MEASUREMENT_MODE_6CHAN_ONE_SHOT) != True):
            return False #One-shot reading of VBGYOR
        print('.')
        if (self.enableInterrupt() != True):
            return False
        print('.')
        return True #We're all setup!

    #----------------------------------------------------------------------   
    # Set the current limit of bulb/LED.
    # Current 0: 12.5mA
    # Current 1: 25mA
    # Current 2: 50mA
    # Current 3: 100mA
    def setBulbCurrent(self, current, device):
        self.selectDevice(device);
        # set the current
        if (current > 0b11):
             current = 0b11; #Limit to two bits
        value = self.virtualReadRegister(AS7265X_LED_CONFIG); #Read
        if (value[0] != True):
            return False
        val = value[1]
        val &= 0b11001111 #Clear ICL_DRV bits
        val |= (current << 4) #Set ICL_DRV bits with user's choice
        return self.virtualWriteRegister(AS7265X_LED_CONFIG, val) #Write
        
    #----------------------------------------------------------------------   
    #As we read various registers we have to point at the master or first/second slave
    def selectDevice(self, device):
        #Set the bits 0:1. Just overwrite whatever is there because masking in the correct value doesn't work.
        return self.virtualWriteRegister(AS7265X_DEV_SELECT_CONTROL, device)
          
    #----------------------------------------------------------------------   
    # Disable the LED or bulb on a given device
    def disableBulb(self, device):
        
        if (self.selectDevice(device) != True):
            return False
        #Read, mask/set, write
        value = self.virtualReadRegister(AS7265X_LED_CONFIG);
        if (value[0] != True):
            return False
        val = value[1]
        val &= ~(1 << 3); #Clear the bit
        return self.virtualWriteRegister(AS7265X_LED_CONFIG, val);
        
    #----------------------------------------------------------------------   
    #Set the current limit of onboard LED. Default is max 8mA = 0b11.
    def setIndicatorCurrent(self, current):
        
        if (current > 0b11):
            current = 0b11;
        #Read, mask/set, write
        value = self.virtualReadRegister(AS7265X_LED_CONFIG); #Read
        if (value[0] != True):
            return False
        val = value[1]
        val &= 0b11111001; #Clear ICL_IND bits
        val |= (current << 1); #Set ICL_IND bits with user's choice

        if (self.selectDevice(AS72651_NIR) != True):
            return False
        return self.virtualWriteRegister(AS7265X_LED_CONFIG, val); #Write
        
    #----------------------------------------------------------------------   
    # Sets the integration cycle amount
    # Give this function a byte from 0 to 255.
    # Time will be 2.8ms * [integration cycles + 1]
    def setIntegrationCycles(self, cycleValue):
        return self.virtualWriteRegister(AS7265X_INTERGRATION_TIME, cycleValue);#Write

    #----------------------------------------------------------------------   
    # Enable the onboard indicator LED
    def enableIndicator(self):
        #Read, mask/set, write
        value = self.virtualReadRegister(AS7265X_LED_CONFIG);
        if (value[0] != True):
            return False
        val = value[1]
        val |= (1 << 0); #Set the bit

        if (self.selectDevice(AS72651_NIR) != True):
            return False
        return self.virtualWriteRegister(AS7265X_LED_CONFIG, val);
        
    #----------------------------------------------------------------------   

    # Sets the gain value
    # Gain 0: 1x (power-on default)
    # Gain 1: 3.7x
    # Gain 2: 16x
    # Gain 3: 64x
    def setGain(self, gain):
        
        if (gain > 0b11):
             gain = 0b11;

        #Read, mask/set, write
        value = self.virtualReadRegister(AS7265X_CONFIG); #Read
        if (value[0] != True):
            return False
        val = value[1]
        val &= 0b11001111; #Clear GAIN bits
        val |= (gain << 4); #Set GAIN bits with user's choice
        return self.virtualWriteRegister(AS7265X_CONFIG, val); #Write
        
    #----------------------------------------------------------------------   

    # Mode 0: 4 channels out of 6 (see datasheet)
    # Mode 1: Different 4 channels out of 6 (see datasheet)
    # Mode 2: All 6 channels continuously
    # Mode 3: One-shot reading of all channels
    def setMeasurementMode(self, mode):
        
        if (mode > 0b11):
            mode = 0b11; #Error check

        # Read, mask/set, write
        value = self.virtualReadRegister(AS7265X_CONFIG); #Read
        if (value[0] != True):
            return False
        val = value[1]
        val &= 0b11110011; #Clear BANK bits
        val |= (mode << 2); #Set BANK bits with user's choice
        return self.virtualWriteRegister(AS7265X_CONFIG, val); #Write
        
    #----------------------------------------------------------------------   
    def enableInterrupt(self):
        #Read, mask/set, write
        value = self.virtualReadRegister(AS7265X_CONFIG); #Read
        if (value[0] != True):
            return False
        val = value[1]
        val |= (1 << 6); #Set INT bit
        return self.virtualWriteRegister(AS7265X_CONFIG, val); #Write
        

    #----------------------------------------------------------------------   
    # Tells IC to take all channel measurements and polls for data ready flag
    def takeMeasurements(self):
        
        if (self.setMeasurementMode(AS7265X_MEASUREMENT_MODE_6CHAN_ONE_SHOT) != True): #Set mode to all 6-channels, one-shot
            return False
        #Wait for data to be ready
        while (1):
            value = self.dataAvailable();
            if (value[0] == False):
                return False
            if (value[1] == 0):
                time.sleep(AS7265X_POLLING_DELAY)
            else:
                break

        #Readings can now be accessed via getCalibratedA(), getJ(), etc
        return True
    #----------------------------------------------------------------------  
    # Turns on all bulbs, takes measurements of all channels, turns off all bulbs
    def takeMeasurementsWithBulb(self):
        if (self.enableBulb(AS7265x_LED_WHITE) != True):
            return False
        if (self.enableBulb(AS7265x_LED_IR) != True):
            return False
        if (self.enableBulb(AS7265x_LED_UV) != True):
            return False

        if (self.takeMeasurements() != True):
            return False

        if (self.disableBulb(AS7265x_LED_WHITE) != True):
            return False #Turn off bulb to avoid heating sensor
        if (self.disableBulb(AS7265x_LED_IR) != True):
            return False
        if (self.disableBulb(AS7265x_LED_UV) != True):
            return False
        
        return True
    #----------------------------------------------------------------------   
    # Checks to see if DRDY flag is set in the control setup register
    def dataAvailable(self):
        value = self.virtualReadRegister(AS7265X_CONFIG);
        if (value[0] != True):
            return False, 0
        return True, (value[1] & (1 << 1)) #Bit 1 is DATA_RDY

    #----------------------------------------------------------------------  
    # Enable the LED or bulb on a given device
    def enableBulb(self, device):
        if (self.selectDevice(device) != True):
            return False

        #Read, mask/set, write
        value = self.virtualReadRegister(AS7265X_LED_CONFIG);
        if (value[0] != True):
            return False
        val = value[1]
        val |= (1 << 3); #Set the bit
        return self.virtualWriteRegister(AS7265X_LED_CONFIG, val);

    #----------------------------------------------------------------------  
    # Get the various color readings
    def getG(self):
        return self.getChannel(AS7265X_R_G_A, AS72652_VISIBLE)
        
    def getH(self):
        return self.getChannel(AS7265X_S_H_B, AS72652_VISIBLE)
        
    def getI(self):
        return self.getChannel(AS7265X_T_I_C, AS72652_VISIBLE)
        
    def getJ(self):
        return self.getChannel(AS7265X_U_J_D, AS72652_VISIBLE)
        
    def getK(self):
        return self.getChannel(AS7265X_V_K_E, AS72652_VISIBLE)
        
    def getL(self): 
        return self.getChannel(AS7265X_W_L_F, AS72652_VISIBLE)
        

    # Get the various NIR readings
    def getR(self):
        return self.getChannel(AS7265X_R_G_A, AS72651_NIR)
        
    def getS(self):
        return self.getChannel(AS7265X_S_H_B, AS72651_NIR)
        
    def getT(self):
        return self.getChannel(AS7265X_T_I_C, AS72651_NIR)
        
    def getU(self):
        return self.getChannel(AS7265X_U_J_D, AS72651_NIR)
        
    def getV(self):
        return self.getChannel(AS7265X_V_K_E, AS72651_NIR)
        
    def getW(self):
        return self.getChannel(AS7265X_W_L_F, AS72651_NIR)
       
    def getA(self):
        return self.getChannel(AS7265X_R_G_A, AS72653_UV)

    def getB(self):
        return self.getChannel(AS7265X_S_H_B, AS72653_UV)
        
    def getC(self):
        return self.getChannel(AS7265X_T_I_C, AS72653_UV)
        
    def getD(self):
        return self.getChannel(AS7265X_U_J_D, AS72653_UV)
        
    def getE(self):
        return self.getChannel(AS7265X_V_K_E, AS72653_UV)
        
    def getF(self):
        return self.getChannel(AS7265X_W_L_F, AS72653_UV)
        
    #----------------------------------------------------------------------   
    # A the 16-bit value stored in a given channel registerReturns
    def getChannel(self, channelRegister, device):
        
        if (self.selectDevice(device) != True):
            return False, 0
        colorData = self.virtualReadRegister(channelRegister)
        if (colorData[0] == False):
            return False, 0
        cd = colorData[1] << 8 #High uint8_t
        colorData = self.virtualReadRegister(channelRegister + 1); #Low uint8_t
        if (colorData[0] == False):
            return False, 0
        cd |= colorData[1]        
        return True, cd
        
    
    #----------------------------------------------------------------------   
    #Returns the various calibration data
    def getCalibratedA(self):
        return self.getCalibratedValue(AS7265X_R_G_A_CAL, AS72653_UV)
        
    def getCalibratedB(self):
        return self.getCalibratedValue(AS7265X_S_H_B_CAL, AS72653_UV)
        
    def getCalibratedC(self):
        return self.getCalibratedValue(AS7265X_T_I_C_CAL, AS72653_UV)
        
    def getCalibratedD(self):
        return self.getCalibratedValue(AS7265X_U_J_D_CAL, AS72653_UV)
        
    def getCalibratedE(self):
        return self.getCalibratedValue(AS7265X_V_K_E_CAL, AS72653_UV)
        
    def getCalibratedF(self):
        return self.getCalibratedValue(AS7265X_W_L_F_CAL, AS72653_UV)
        
    def getCalibratedG(self):
        return self.getCalibratedValue(AS7265X_R_G_A_CAL, AS72652_VISIBLE)
        
    def getCalibratedH(self):
        return self.getCalibratedValue(AS7265X_S_H_B_CAL, AS72652_VISIBLE)
        
    def getCalibratedI(self):
        return self.getCalibratedValue(AS7265X_T_I_C_CAL, AS72652_VISIBLE)
        
    def getCalibratedJ(self):
        return self.getCalibratedValue(AS7265X_U_J_D_CAL, AS72652_VISIBLE)
        
    def getCalibratedK(self):
        return self.getCalibratedValue(AS7265X_V_K_E_CAL, AS72652_VISIBLE)
        
    def getCalibratedL(self):
        return self.getCalibratedValue(AS7265X_W_L_F_CAL, AS72652_VISIBLE)
        
    def getCalibratedR(self):
        return self.getCalibratedValue(AS7265X_R_G_A_CAL, AS72651_NIR)
        
    def getCalibratedS(self):
        return self.getCalibratedValue(AS7265X_S_H_B_CAL, AS72651_NIR)
        
    def getCalibratedT(self):
        return self.getCalibratedValue(AS7265X_T_I_C_CAL, AS72651_NIR)
        
    def getCalibratedU(self):
        return self.getCalibratedValue(AS7265X_U_J_D_CAL, AS72651_NIR)
        
    def getCalibratedV(self):
        return self.getCalibratedValue(AS7265X_V_K_E_CAL, AS72651_NIR)
        
    def getCalibratedW(self):
        return self.getCalibratedValue(AS7265X_W_L_F_CAL, AS72651_NIR)
  
    #----------------------------------------------------------------------    
    #Given an address, read four bytes and return the floating point calibrated value
    def getCalibratedValue(self, calAddress, device):
        if (self.selectDevice(device)  != True):
            return False, 0
        

        value = self.virtualReadRegister(calAddress + 0);
        if (value[0] != True):
            return False, 0
        b0 = value[1] & 0xFF
        value = self.virtualReadRegister(calAddress + 1);
        if (value[0] != True):
            return False, 0
        b1= value[1] & 0xFF
        value = self.virtualReadRegister(calAddress + 2);
        if (value[0] != True):
            return False, 0
        b2 = value[1] & 0xFF
        value = self.virtualReadRegister(calAddress + 3);
        if (value[0] != True):
            return False, 0
        b3 = value[1] & 0xFF
        
        #Channel calibrated values are stored big-endian
        calBytes = 0;
        calBytes |= (b0 << (8 * 3))
        calBytes |= (b1 << (8 * 2))
        calBytes |= (b2 << (8 * 1))
        calBytes |= (b3 << (8 * 0))

        return True, self.convertBytesToFloat(calBytes)
        
    #----------------------------------------------------------------------   
    # Given 4 bytes returns the floating point value
    def convertBytesToFloat(self, myLong):
        ba = bytearray(4) 
        ba[0] = myLong & 0xFF;
        ba[1] = (myLong >> 8) & 0xFF;
        ba[2] = (myLong >> 16) & 0xFF;
        ba[3] = (myLong >> 24) & 0xFF;
        return struct.unpack('<f', ba)[0]
       
    #----------------------------------------------------------------------   
    # Returns the temperature of a given device in C
    def getTemperature(self, deviceNumber):

        if (self.selectDevice(deviceNumber) != True):
            return False, 0
        return self.virtualReadRegister(AS7265X_DEVICE_TEMP)
