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
    """_summary_

    :param object: _description_
    :type object: _type_
    """

    def __init__(self,address,**kwargs):
        """The **__init__** method represents the constructor method.
        """
        self.address=address
        self.sensor = i2c.get_i2c_device(address, **kwargs)

            
    def begin(self):
        manifacturer_id = self.sensor.readU16BE(MCP9808_MANIFACTURER_ID)
        device_id = self.sensor.readU16BE(MCP9808_DEVICE_ID_REVISION)

        return manifacturer_id == 0x0054 and device_id == 0x0400

    def get_temp(self):
        sensor_temp = self.sensor.readU16BE(MCP9808_T_AMBIENT)

        temp = (sensor_temp & 0x0FFF) / 16.0
        if sensor_temp & 0x1000:
            temp -= 256.0
        return temp

    def set_resolution(self,res_value):
        if(res_value==0):
            self.sensor.write8(MCP9808_RESOULTION,0x00)
        elif(res_value==1):
            self.sensor.write8(MCP9808_RESOULTION,0x01)
        elif(res_value==2):
            self.sensor.write8(MCP9808_RESOULTION,0x02)
        else:
            self.sensor.write8(MCP9808_RESOULTION,0x03)

    def get_resolution(self):
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
        if(status==True):
            self.sensor.write16(MCP9808_CONFIG,MCP9808_SHUTDOWN)
        else:
            self.sensor.write16(MCP9808_CONFIG,0x0000)

    def get_status(self):
        status=self.sensor.readU16BE(MCP9808_CONFIG)
        if(status==1):
            return "Low power mode activated"
        else:
            return "Power on mode activated"

    def get_device_id(self):
        device_id = self.sensor.readU16BE(MCP9808_DEVICE_ID_REVISION)
        return "Device ID: "+str(hex(device_id))

    def get_manifacturer_id(self):
        manifacturer_id = self.sensor.readU16BE(MCP9808_MANIFACTURER_ID)
        return "Manifacturer ID: "+str(hex(manifacturer_id))
