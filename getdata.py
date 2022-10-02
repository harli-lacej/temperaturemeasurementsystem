from datetime import datetime
from datetime import date
import time
from mcp9808 import mcp9808 as MCP9808
import mysql.connector

sensor = MCP9808.MCP9808(0x18)
sensor2 = MCP9808.MCP9808(0x19)

def insert_varibles_into_table(deviceID,temperature):
    try:
        connection = mysql.connector.connect(
        host="htl-projekt.com",
        user="harlilacej",
        password="!Insy_2021$",
        port=33060,
        database="2023_5ay_harlilacej_ecoSense_tempeature"
        )
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO temperature (deviceID,temperature) 
                                VALUES (%s,%s) """

        record = (deviceID,temperature)
        cursor.execute(mySql_insert_query, record)
        connection.commit()

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



if(sensor.begin() == True and sensor2.begin() == True):
    while True:
        temp = sensor.read_temp()
        insert_varibles_into_table(1,temp)
        print("Device 1:",temp)

        temp2 = sensor2.read_temp()
        insert_varibles_into_table(2,temp2)
        print("Device 2:",temp2)
        print("-----------------")
        time.sleep(3)