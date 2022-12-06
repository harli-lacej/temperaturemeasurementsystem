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

#creating a list to store addresses found
address_list=[]
#defining a function to add new addresses found in a list 
def scan():
    #creating a subprocess that uses as argument a command to detect i2c addresses in a bus
    p = subprocess.Popen(['i2cdetect', '-y','1'],stdout=subprocess.PIPE,)
    #defining all possible address that MCP8908 use
    possible_address=["18","19","1A","1B","1C","1D","1E","1F"]

    #interating for 8 times,if all sensors are present in the bus
    for i in range(0,7):
        #taking the output of the subprocess
        line = str(p.stdout.readline())
        #using RegEx to filter addresses from the output
        for match in re.finditer(" [0-9]{2}", line):    
            sensor_address=match.group(0)
            if sensor_address not in address_list:
                #adding addresses in the list
                address_list.append(sensor_address)
                
    return address_list

#calling the function scan
devices=scan()
#Console output header section
print(address_list)
print("+----------+-------------+")
print("| DeviceID | Temperature |")
print("+----------+-------------+")

while True:
    new_list = scan()
    #checking if the first and second call of the scan function any differeces have
    if devices != new_list:
        if new_list - devices:
            print("New devices:", new_list - devices)
        if devices - new_list:
            print("Gone devices:", devices - new_list)
        devices = new_list
        #if defferences where present,the program terminates(rerun with help of a bash script)
        sys.exit()

    #creating for each sensor found a new object 
    for i in range(0,len(new_list)):
        globals()[f'sensor{i}']=MCP9808.MCP9808(int(new_list[i],16))

    #customizing the the output table using prettytable
    t = PrettyTable(['DeviceID', 'Temperature'])
    t.align['DeviceID'] = 'l'
    t.align['Temperature'] = 'r'
    t.hrules = 1

    #if a object called "sensor0" is created the code inside the if will be exectued
    if 'sensor0' in globals():
        #setting the resolution of temperature values
        sensor0.set_resolution(3)
        #defing a function to get data from the sensor,display them and insert in database
        def get_data():
            i=0
            for i in range(2):
                #checking if we are dealing with a MCP9808 sensor
                if(sensor0.begin() == True):
                    #getting the tempertature from the sensor
                    temp = sensor0.get_temp()
                    #delay of 10 seconds 
                    time.sleep(10)
                    #inserting the temperature and DeviceID in the database 
                    insert_varibles_into_table(1,temp)
                    #adding a new row to prettytable
                    t.add_row(['1',temp])
                    print( "\n".join(t.get_string().splitlines()[-2:]))
 
    #if a object called "sensor1" is created the code inside the if will be exectued                   
    if 'sensor1' in globals():
        #setting the resolution of temperature values
        sensor1.set_resolution(3)
        #defing a function to get data from the sensor,display them and insert in database
        def get_data2():
            a=0
            for a in range(2):
                #checking if we are dealing with a MCP9808 sensor
                if(sensor1.begin() == True):
                    #getting the tempertature from the sensor
                    temp1 = sensor1.get_temp()
                    #delay of 10 seconds 
                    time.sleep(10)
                    #inserting the temperature and DeviceID in the database 
                    insert_varibles_into_table(2,temp1)
                    #adding a new row to prettytable
                    t.add_row(['2',temp1])
                    print( "\n".join(t.get_string().splitlines()[-2:]))
                    
    #if a object called "sensor2" is created the code inside the if will be exectued                    
    if 'sensor2' in globals():
        #setting the resolution of temperature values
        sensor2.set_resolution(3)
        #defing a function to get data from the sensor,display them and insert in database
        def get_data3():
            b=0
            for b in range(2):
                #checking if we are dealing with a MCP9808 sensor
                if(sensor2.begin() == True):
                    #getting the tempertature from the sensor
                    temp2 = sensor2.get_temp()
                    #delay of 10 seconds 
                    time.sleep(10)
                    #inserting the temperature and DeviceID in the database 
                    insert_varibles_into_table(3,temp2)
                    #adding a new row to prettytable
                    t.add_row(['3',temp2])
                    print( "\n".join(t.get_string().splitlines()[-2:]))
                
    #if a object called "sensor3" is created the code inside the if will be exectued      
    if 'sensor3' in globals():
        #setting the resolution of temperature values
        sensor3.set_resolution(3)
        #defing a function to get data from the sensor,display them and insert in database
        def get_data4():
            c=0
            for c in range(2):
                #checking if we are dealing with a MCP9808 sensor
                if(sensor3.begin() == True):
                    #getting the tempertature from the sensor
                    temp3 = sensor3.get_temp()
                    #delay of 10 seconds 
                    time.sleep(10)
                    #inserting the temperature and DeviceID in the database 
                    insert_varibles_into_table(4,temp3)
                     #adding a new row to prettytable
                    t.add_row(['4',temp3])
                    print( "\n".join(t.get_string().splitlines()[-2:]))
                    
    #if a object called "sensor4" is created the code inside the if will be exectued  
    if 'sensor4' in globals():
    #setting the resolution of temperature values
    sensor4.set_resolution(3)
    #defing a function to get data from the sensor,display them and insert in database
    def get_data5():
        d=0
        for d in range(2):
            #checking if we are dealing with a MCP9808 sensor
            if(sensor4.begin() == True):
                #getting the tempertature from the sensor
                temp4 = sensor4.get_temp()
                #delay of 10 seconds 
                time.sleep(10)
                #inserting the temperature and DeviceID in the database 
                insert_varibles_into_table(5,temp4)
                #adding a new row to prettytable
                t.add_row(['5',temp4])
                print( "\n".join(t.get_string().splitlines()[-2:]))
            
    #if a object called "sensor5" is created the code inside the if will be exectued  
    if 'sensor5' in globals():
    #setting the resolution of temperature values
    sensor5.set_resolution(3)
    #defing a function to get data from the sensor,display them and insert in database
    def get_data6():
        e=0
        for e in range(2):
            #checking if we are dealing with a MCP9808 sensor
            if(sensor5.begin() == True):
                #getting the tempertature from the sensor
                temp5 = sensor5.get_temp()
                #delay of 10 seconds 
                time.sleep(10)
                #inserting the temperature and DeviceID in the database 
                insert_varibles_into_table(6,temp5)
                #adding a new row to prettytable
                t.add_row(['6',temp5])
                print( "\n".join(t.get_string().splitlines()[-2:]))
    
    #if a object called "sensor6" is created the code inside the if will be exectued  
    if 'sensor6' in globals():
    #setting the resolution of temperature values
    sensor6.set_resolution(3)
    #defing a function to get data from the sensor,display them and insert in database
    def get_data7():
        f=0
        for f in range(2):
            #checking if we are dealing with a MCP9808 sensor
            if(sensor6.begin() == True):
                #getting the tempertature from the sensor
                temp6 = sensor6.get_temp()
                #delay of 10 seconds 
                time.sleep(10)
                #inserting the temperature and DeviceID in the database 
                insert_varibles_into_table(7,temp6)
                #adding a new row to prettytable
                t.add_row(['7',temp6])
                print( "\n".join(t.get_string().splitlines()[-2:]))
                
    #if a object called "sensor7" is created the code inside the if will be exectued  
    if 'sensor7' in globals():
    #setting the resolution of temperature values
    sensor7.set_resolution(3)
    #defing a function to get data from the sensor,display them and insert in database
    def get_data8():
        g=0
        for g in range(2):
            #checking if we are dealing with a MCP9808 sensor
            if(sensor7.begin() == True):
                #getting the tempertature from the sensor
                temp7 = sensor7.get_temp()
                #delay of 10 seconds 
                time.sleep(10)
                #inserting the temperature and DeviceID in the database 
                insert_varibles_into_table(8,temp7)
                #adding a new row to prettytable
                t.add_row(['8',temp7])
                print( "\n".join(t.get_string().splitlines()[-2:]))
                
                

    thread1 = threading.Thread(target=get_data, args=())
    thread1.start()
    thread2= threading.Thread(target=get_data2, args=())
    thread2.start()
    thread1.join()
    thread2.join()
