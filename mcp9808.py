import logging
import math
import Adafruit_GPIO.I2C as i2c


'''
    """Setting constant variables,the variables contain the values of the i2c address of the 
    MCP9808 sensors as hexadecimal values.
    """
'''

MCP9808_ADDRESS_1 = 0x18
MCP9808_ADDRESS_2 = 0x19
MCP9808_ADDRESS_3 = 0x1A
MCP9808_ADDRESS_4 = 0x1B

'''

    """Setting the values for the registers

    """
'''
MCP9808_CONFIG = 0x01
MCP9808_T_UPPER = 0x02
MCP9808_T_LOWER = 0x03
MCP9808_T_CRIT = 0x04
MCP9808_T_AMBIENT = 0x05
MCP9808_MANIFACTURER_ID = 0x06
MCP9808_DEVICE_ID_REVISION = 0x07
MCP9808_RESOULTION = 0x08

# Configuration register values.
MCP9808_SHUTDOWN = 0x0100
MCP9808_NO_T_CIRT = 0x0080
MCP9808_NO_T_UPPER_LOWER = 0x0040
MCP9808_CLEAR_INTERRUPT = 0x0020
MCP9808_ALERT_OUT_STATUS = 0x0010
MCP9808_ALERT_OUT_CONTROL = 0x0008
MCP9808_ALERT_OUT_SELECT = 0x0002
MCP9808_ALERT_OUT_POLARITY= 0x0002
MCP9808_ALERT_OUT_INTERRUPT = 0x0001
'''
    """Creating a class named MCP9808 to represent the temperature sensor MCP9808
    """

'''

class MCP9808(object):


    def __init__(self,address,**kwargs):
            self.address=address
            self.sensor = i2c.get_i2c_device(address, **kwargs)

            


    def begin(self):
        """Start taking temperature measurements. Returns True if the device is 
        intialized, False otherwise.
        """
        # Check manufacturer and device ID match expected values.
        mid1 = self.sensor.readU16BE(MCP9808_MANIFACTURER_ID)
        did1 = self.sensor.readU16BE(MCP9808_DEVICE_ID_REVISION)
        #self._logger.debug('Read manufacturer ID: {0:04X}'.format(mid1))
        #self._logger.debug('Read device ID: {0:04X}'.format(did1))
        return mid1 == 0x0054 and did1 == 0x0400

    def readTempC(self):
        """Read sensor and return its value in degrees celsius."""
        # Read temperature register value.
        tempFormDev1 = self.sensor.readU16BE(MCP9808_T_AMBIENT)
        #self._logger.debug('Device 1 temp: 0x{0:04X}'.format(tempFormDev1  & 0xFFFF))
        #self._logger.debug('Device 1 temp: 0x{0:04X}'.format(tempFormDev2  & 0xFFFF))
        # Scale and convert to signed value.
        temp = (tempFormDev1 & 0x0FFF) / 16.0
        if tempFormDev1 & 0x1000:
            temp -= 256.0
        return temp