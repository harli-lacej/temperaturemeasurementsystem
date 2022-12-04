__author__ = "Harli Lacej"
__copyright__ = "Copyright 2022, ecoSense Dipomarbeit"
__license__ = "MIT License"
__version__ = "1.2"
__email__ = "harlac17@htl-shkoder.com"

#importing MCP9808 sensor libary
from mcp9808 import mcp9808 as MCP9808  

#importing other libraries needed for the program
import mysql.connector
import supervisor
import time
import threading
import os
import subprocess
import re
from prettytable import PrettyTable


#function to create a connection to the database and insert data 
def insert_varibles_into_table(deviceID,temperature):
    #setting variables for the connection
    hostname="htl-projekt.com"
    username="harlilacej"
    passwd="!Insy_2021$"
    tcpip_port=33060 #port for remote access
    database_name="2023_EcoSense_DA"
    
    #trying to establish a connetion with the database uisng login data
    try:
        connection = mysql.connector.connect(
        host=hostname,
        user=username,
        password=passwd,
        port=tcpip_port,
        database=databasename
        )
        cursor = connection.cursor()
        #inserting values given in tha function as parameters
        mySql_insert_query = '''INSERT INTO temperature(deviceID,temperature) VALUES (%s,%s) '''

        record = (deviceID,temperature)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
    
    #will be executed if a error is detected in the connection
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    #closing the connection with the database
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


address_list=[]
def scan():
    p = subprocess.Popen(['i2cdetect', '-y','1'],stdout=subprocess.PIPE,)
    possible_address=["18","19","1A","1B","1C","1D","1E","1F"]

    for i in range(0,3):
        line = str(p.stdout.readline())
        for match in re.finditer(" [0-9]{2}", line):    
            sensor_address=match.group(0)
            if sensor_address not in address_list:
                address_list.append(sensor_address)
                
    return address_list

devices=scan()
print(address_list)
print("+----------+-------------+")
print("| DeviceID | Temperature |")
print("+----------+-------------+")
while True:
    new_list = scan()
    if devices != new_list:
        if new_list - devices:
            print("New devices:", new_list - devices)
        if devices - new_list:
            print("Gone devices:", devices - new_list)
        devices = new_list
        sys.exit()

    for i in range(0,len(new_list)):
        globals()[f'sensor{i}']=MCP9808.MCP9808(int(new_list[i],16))


    t = PrettyTable(['DeviceID', 'Temperature'])
    t.align['DeviceID'] = 'l'
    t.align['Temperature'] = 'r'
    t.hrules = 1

    if 'sensor0' in globals():
        sensor0.set_resolution(3)
        def get_data():
            i=0

            for i in range(2):

                if(sensor0.begin() == True):
                    temp = sensor0.get_temp()
                    time.sleep(1)
                    insert_varibles_into_table(1,temp)
                    t.add_row(['1',temp])
                    print( "\n".join(t.get_string().splitlines()[-2:]) )
    if 'sensor1' in globals():
        sensor1.set_resolution(3)
        def get_data2():
            a=0
            for a in range(2):

                if(sensor1.begin() == True):
                    temp1 = sensor1.get_temp()
                    time.sleep(1)
                    insert_varibles_into_table(2,temp1)
                    t.add_row(['2',temp1])
                    print( "\n".join(t.get_string().splitlines()[-2:]) )
    if 'sensor2' in globals():
        sensor2.set_resolution(3)
        def get_data3():
            a=0
            for a in range(2):

                if(sensor2.begin() == True):
                    temp2 = sensor2.get_temp()
                    time.sleep(1)
                    insert_varibles_into_table(3,temp2)
                    t.add_row(['3',temp2])
                    print( "\n".join(t.get_string().splitlines()[-2:]) )
    if 'sensor3' in globals():
        sensor3.set_resolution(3)
        def get_data4():
            a=0
            for a in range(2):

                if(sensor3.begin() == True):
                    temp3 = sensor3.get_temp()
                    time.sleep(1)
                    insert_varibles_into_table(4,temp3)
                    t.add_row(['4',temp4])
                    print( "\n".join(t.get_string().splitlines()[-2:]) )

    thread1 = threading.Thread(target=get_data, args=())
    thread1.start()
    thread2= threading.Thread(target=get_data2, args=())
    thread2.start()

    thread1.join()
    thread2.join()
