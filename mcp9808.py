import math
import Adafruit_GPIO.I2C as i2c

MCP9808_CONFIG = 0x01
MCP9808_T_UPPER = 0x02
MCP9808_T_LOWER = 0x03
MCP9808_T_CRIT = 0x04
MCP9808_T_AMBIENT = 0x05
MCP9808_MANIFACTURER_ID = 0x06
MCP9808_DEVICE_ID_REVISION = 0x07
MCP9808_RESOULTION = 0x08

MCP9808_SHUTDOWN = 0x0100
MCP9808_NO_T_CIRT = 0x0080
MCP9808_NO_T_UPPER_LOWER = 0x0040
MCP9808_CLEAR_INTERRUPT = 0x0020
MCP9808_ALERT_OUT_STATUS = 0x0010
MCP9808_ALERT_OUT_CONTROL = 0x0008
MCP9808_ALERT_OUT_SELECT = 0x0002
MCP9808_ALERT_OUT_POLARITY= 0x0002
MCP9808_ALERT_OUT_INTERRUPT = 0x0001

class MCP9808(object):
    """This is a conceptual class that represents a temperature sensor of the Microchip MCP9808 model with a board from Adafruit.
    """

    def __init__(self,address,**kwargs):
        """The **__init__** method represents the constructor method.
        """
        self.address=address
        self.sensor = i2c.get_i2c_device(address, **kwargs)

            
    def begin(self):
        """It checks if the sensor connected through the I2C bus system belongs to the MCP9808 model. 
        The register in which the manufacturer is located and the device ID register are read. 
        If the values correspond to the correct values, then the method returns True.

        :return: Returns True if the connection is correct and we have the right sensors connected.
        :rtype: boolean
        """
        manifacturer_id = self.sensor.readU16BE(MCP9808_MANIFACTURER_ID)
        device_id = self.sensor.readU16BE(MCP9808_DEVICE_ID_REVISION)

        return manifacturer_id == 0x0054 and device_id == 0x0400

    def get_temp(self):
        """
        Through this method, the current temperature value can be obtained in Celcuis degree units.
        The method has no arguments at the moment it is invoked.
        
        :return: A decimal value of the actual temperature measured by the sensor.
        :rtype: float
        """
        sensor_temp = self.sensor.readU16BE(MCP9808_T_AMBIENT)

        temp = (sensor_temp & 0x0FFF) / 16.0
        if sensor_temp & 0x1000:
            temp -= 256.0
        return temp

    def set_resolution(self,res_value):
        """Through this method, the resolution of the values that will be received from the temperature sensor can be set. 
        Based on the resolution, the speed of sending the values from the sensor also varies. 
        If the resolution is high, then the values sent in a certain time will are less.

        :param res_value: The value of the parameter must be a whole value between 0 and 3. Where the value 3 represents the highest possible resolution of the values.
        :type res_value: int
        """
        if(res_value==0):
            self.sensor.write8(MCP9808_RESOULTION,0x00)
        elif(res_value==1):
            self.sensor.write8(MCP9808_RESOULTION,0x01)
        elif(res_value==2):
            self.sensor.write8(MCP9808_RESOULTION,0x02)
        else:
            self.sensor.write8(MCP9808_RESOULTION,0x03)

    def get_resolution(self):
        """Through this method, the current resolution in a certain sensor can be obtained in the form of a string.
        The string returned after calling the method will show the resolution and the conversion time.

        :return: Shows the resolution and conversion time of a sensor.
        :rtype: string
        """
        res=self.sensor.readU8(MCP9808_RESOULTION)
        if(res==0):
            return "Resoultion: +0.5°C,Conversion time: 30 ms typical"
        elif(res==1):
            return "Resolution: +0.25°C,Conversion time: 65 ms typical"
        elif(res==2):
            return "Resolution: +0.125°C,Conversion time: 130 ms typical"
        else:
            return "Resolution: +0.0625°C,Conversion time:  250 ms typical"

    def low_power_mode(self,status):
        """Through this method, the sensor can be placed in low-power mode or shutdown mode. Through this method, all activities that consume energy stop functioning.

        :param status: It is decided whether the sensor should be in low-power mode or not, where True indicates that the device is in low-power mode and if it is set to false, it is in power-on mode.
        :type status: boolean
        """
        if(status==True):
            self.sensor.write16(MCP9808_CONFIG,MCP9808_SHUTDOWN)
        else:
            self.sensor.write16(MCP9808_CONFIG,0x0000)

    def get_status(self):
        """Through this method we can understand what is the current status of the sensor, so information can be obtained if the device is in low-power or in power-on mode.

        :return: The current status of the sensor is shown in a sentence.
        :rtype: string
        """
        status=self.sensor.readU16BE(MCP9808_CONFIG)
        if(status==1):
            return "Low power mode activated"
        else:
            return "Power on mode activated"

    def get_device_id(self):
        """Through this function we can get information about the Device ID of the temperature sensor. The value should be 0x04 and if it is not like that, you can understand that we are not dealing with an MCP9808 sensor.

        :return: Shows the Hex value of the DeviceID presented in a string.
        :rtype: string
        """
        device_id = self.sensor.readU16BE(MCP9808_DEVICE_ID_REVISION)
        return "Device ID: "+str(hex(device_id))

    def get_manifacturer_id(self):
        """Through this function we can get information about the Manifacturer ID of the temperature sensor. The value should be 0x0054 and if it is not like that, you can understand that we are not dealing with an Microchip device.

        :return: Shows the Hex value of the ManifacturerID presented in a string.
        :rtype: string
        """
        manifacturer_id = self.sensor.readU16BE(MCP9808_MANIFACTURER_ID)
        return "Manifacturer ID: "+str(hex(manifacturer_id))
