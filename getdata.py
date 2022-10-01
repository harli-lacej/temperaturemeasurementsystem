from datetime import datetime
from datetime import date
import time
from mcp9808 import mcp9808 as MCP9808



sensor = MCP9808.MCP9808(0x18)
sensor2 = MCP9808.MCP9808(0x19)

sensor.begin()

while True:
    temp = sensor.readTempC()
    print("Device 1:",temp)

    temp = sensor2.readTempC()
    print("Device 2:",temp)
    print("-----------------")
    time.sleep(3)