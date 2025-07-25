__author__ = "Harli Lacej"
__copyright__ = "Copyright 2023, ecoSense Dipomarbeit"
__license__ = "MIT License"
__version__ = "1.3"
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
import requests
import ipinfo
import functools

#function to create a connection to the database and insert data 
def insert_varibles_into_table(deviceID,temperature,product_id,location):
    #setting variables for the connection
    #set your own values here
    hostname="x"
    username="x"
    passwd="ohh...thats a secret but try to guess"
    tcpip_port=33060 #port for remote access
    database_name="x"
    
    #trying to establish a connetion with the database uisng login data
    try:
        connection = mysql.connector.connect(
        host=hostname,
        user=username,
        password=passwd,
        port=tcpip_port,
        database=database_name
        )
        cursor = connection.cursor()
        #inserting values given in tha function as parameters
        mySql_insert_query = '''INSERT INTO Temperatur(deviceID,temperature,product_id,location) VALUES (%s,%s,%s,%s) '''

        record = (deviceID,temperature,product_id,location)
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

#defining a function to add new addresses found in a list 
def scan():
    #creating a list to store addresses found
    address_list=[]
    #creating a subprocess that uses as argument a command to detect i2c addresses in a bus
    p = subprocess.Popen(['i2cdetect', '-y','1'],stdout=subprocess.PIPE,)
    #defining all possible address that MCP8908 use
    possible_address=["18","19","1a","1b","1c","1d","1e","1f"]

    #interating for 8 times,if all sensors are present in the bus
    for i in range(0,7):
        #taking the output of the subprocess
        line = str(p.stdout.readline())
        #using RegEx to filter addresses from the output
        for match in re.finditer(" (?<!-)[0-9a-fA-F]{2}(?=\s)", line):    
            sensor_address=match.group(0)
            if sensor_address not in address_list:
                #adding addresses in the list
                address_list.append(sensor_address)
                
    return address_list

#defining a function to get the ip address
def get_ip():
    #saving the response in a variable
    api_response = requests.get('https://api64.ipify.org?format=json').json()
    return api_response["ip"]

#saving api call result in cache
@functools.lru_cache()
#defining a function to get the location of the found ip address
def get_location():
    #using a library to access the location finder API
    access_token = '457461b96183e9'
    handler = ipinfo.getHandler(access_token)
    ip_address = get_ip()
    details = handler.getDetails(ip_address)
    return details.city+","+details.country


#calling the function scan
device=scan()
#Console output header section
print(device)

#getting the serial number of the Raspberry Pi to use as Product ID(unique Indetifier)
serial_number = os.popen("cat /proc/cpuinfo | grep Serial | awk '{print $3}'").read().strip()
    
#saving the function return in the variable
#result=get_location()
#saving the Location of the IP-Address as a string contraining city and country
ip_location=get_location()
print("+----------+-------------+")
print("| DeviceID | Temperature |")
print("+----------+-------------+")


# creating a dictionary
devices = {}
while True:

    # delay for one second each loop
    time.sleep(1)

    # save the result of the function scan () in a set
    addresses = set(scan())
    # looking up for new addresses ( elements )
    to_add = addresses - devices.keys()
    # checking if anything doesnt appear anymore in scan () result
    to_remove = devices.keys() - addresses

    for address in to_add:
        # creating new objects with the addresses stored in the set
        devices[address] = MCP9808.MCP9808(int(address, 16))
        # printing an output
        print(f"Added new device {address}")

    for address in to_remove:
        # deleting the objects with the keys stored the set
        del devices[address]
        # printing an output
        print(f"Removed device {address}. It was not found while scanning.")
    
    #customizing the the output table using prettytable
    t = PrettyTable(['DeviceID', 'Temperature'])
    t.align['DeviceID'] = 'l'
    t.align['Temperature'] = 'r'
    t.hrules = 1

    #if a object called " 18" is created the code inside the if will be exectued
    if ' 18' in devices:
        #setting the resolution of temperature values
        #sensor0.set_resolution(3)
        #defing a function to get data from the sensor,display them and insert in database
        def get_data():
            device1 = devices[' 18']
            #checking if we are dealing with a MCP9808 sensor
            if(device1.begin() == True):
                #getting the tempertature from the sensor
                temp = device1.get_temp()
                #delay of 10 seconds 
                time.sleep(10)
                #inserting the temperature and DeviceID in the database 
                insert_varibles_into_table(1,temp,serial_number,ip_location)
                #adding a new row to prettytable
                t.add_row(['1',temp])
                print( "\n".join(t.get_string().splitlines()[-2:]))
 
    #if a object called " 19" is created the code inside the if will be exectued                   
    if ' 19' in devices:
        device2 = devices[' 19']
        #setting the resolution of temperature values
        device2.set_resolution(3)
        #defing a function to get data from the sensor,display them and insert in database
        def get_data2():
            #checking if we are dealing with a MCP9808 sensor
            if(device2.begin() == True):
                #getting the tempertature from the sensor
                temp1 = device2.get_temp()
                #delay of 10 seconds 
                time.sleep(10)
                #inserting the temperature and DeviceID in the database 
                insert_varibles_into_table(2,temp1,serial_number,ip_location)
                #adding a new row to prettytable
                t.add_row(['2',temp1])
                print( "\n".join(t.get_string().splitlines()[-2:]))
                    
    #if a object called " 1A" is created the code inside the if will be exectued                    
    if ' 1a' in devices:
        device3=devices[' 1a']
        #setting the resolution of temperature values
        device3.set_resolution(3)
        #defing a function to get data from the sensor,display them and insert in database
        def get_data3():
            #checking if we are dealing with a MCP9808 sensor
            if(device3.begin() == True):
                #getting the tempertature from the sensor
                temp2 = device3.get_temp()
                #delay of 10 seconds 
                time.sleep(10)
                #inserting the temperature and DeviceID in the database 
                insert_varibles_into_table(3,temp2,serial_number,ip_location)
                #adding a new row to prettytable
                t.add_row(['3',temp2])
                print( "\n".join(t.get_string().splitlines()[-2:]))
                
    #if a object called " 1B" is created the code inside the if will be exectued      
    if ' 1b' in devices:
        device4=devices[' 1b']
        #setting the resolution of temperature values
        device4.set_resolution(3)
        #defing a function to get data from the sensor,display them and insert in database
        def get_data4():
            #checking if we are dealing with a MCP9808 sensor
            if(device4.begin() == True):
                #getting the tempertature from the sensor
                temp3 = device4.get_temp()
                #delay of 10 seconds 
                time.sleep(10)
                #inserting the temperature and DeviceID in the database 
                insert_varibles_into_table(4,temp3,serial_number,ip_location)
                    #adding a new row to prettytable
                t.add_row(['4',temp3])
                print( "\n".join(t.get_string().splitlines()[-2:]))
                    
    #if a object called " 1C" is created the code inside the if will be exectued  
    if ' 1c' in devices:
        device5=devices[' 1c']
        #setting the resolution of temperature values
        device5.set_resolution(3)
        #defing a function to get data from the sensor,display them and insert in database
        def get_data5():
            #checking if we are dealing with a MCP9808 sensor
            if(device5.begin() == True):
                #getting the tempertature from the sensor
                temp4 = device5.get_temp()
                #delay of 10 seconds 
                time.sleep(10)
                #inserting the temperature and DeviceID in the database 
                insert_varibles_into_table(5,temp4,serial_number,ip_location)
                #adding a new row to prettytable
                t.add_row(['5',temp4])
                print( "\n".join(t.get_string().splitlines()[-2:]))
            
    #if a object called " 1D" is created the code inside the if will be exectued  
    if ' 1d' in devices:
        device6=devices[' 1d']
        #setting the resolution of temperature values
        device6.set_resolution(3)
        #defing a function to get data from the sensor,display them and insert in database
        def get_data6():
            #checking if we are dealing with a MCP9808 sensor
            if(device6.begin() == True):
                #getting the tempertature from the sensor
                temp5 = device6.get_temp()
                #delay of 10 seconds 
                time.sleep(10)
                #inserting the temperature and DeviceID in the database 
                insert_varibles_into_table(6,temp5,serial_number,ip_location)
                #adding a new row to prettytable
                t.add_row(['6',temp5])
                print( "\n".join(t.get_string().splitlines()[-2:]))
    
    #if a object called " 1E" is created the code inside the if will be exectued  
    if ' 1e' in devices:
        device7=devices[' 1e']
        #setting the resolution of temperature values
        device7.set_resolution(3)
        #defing a function to get data from the sensor,display them and insert in database
        def get_data7():
            #checking if we are dealing with a MCP9808 sensor
            if(device7.begin() == True):
                #getting the tempertature from the sensor
                temp6 = device7.get_temp()
                #delay of 10 seconds 
                time.sleep(10)
                #inserting the temperature and DeviceID in the database 
                insert_varibles_into_table(7,temp6,serial_number,ip_location)
                #adding a new row to prettytable
                t.add_row(['7',temp6])
                print( "\n".join(t.get_string().splitlines()[-2:]))
                    
    #if a object called " 1F" is created the code inside the if will be exectued  
    if ' 1f' in devices:
        device8=devices[' 1f']
        #setting the resolution of temperature values
        device8.set_resolution(3)
        #defing a function to get data from the sensor,display them and insert in database
        def get_data8():
            #checking if we are dealing with a MCP9808 sensor
            if(device8.begin() == True):
                #getting the tempertature from the sensor
                temp7 = device8.get_temp()
                #delay of 10 seconds 
                time.sleep(10)
                #inserting the temperature and DeviceID in the database 
                insert_varibles_into_table(8,temp7,serial_number,ip_location)
                #adding a new row to prettytable
                t.add_row(['8',temp7])
                print( "\n".join(t.get_string().splitlines()[-2:]))
                
    #creating a thread which have as target the methods created
    #the thread is created only if the object exist
    if ' 18' in devices:
        thread1 = threading.Thread(target=get_data, args=())
        thread1.start()
    if ' 19' in devices:
        thread2= threading.Thread(target=get_data2, args=())
        thread2.start()
    if ' 1a' in devices:
        thread3= threading.Thread(target=get_data3, args=())
        thread3.start()
    if ' 1b' in devices:
        thread4= threading.Thread(target=get_data4, args=())
        thread4.start()
    if ' 1c' in devices:
        thread5= threading.Thread(target=get_data5, args=())
        thread5.start()
    if ' 1d' in devices:
        thread6= threading.Thread(target=get_data6, args=())
        thread6.start()
    if ' 1e' in devices:
        thread7= threading.Thread(target=get_data7, args=())
        thread7.start()
    if ' 1f' in devices:
        thread8= threading.Thread(target=get_data8, args=())
        thread8.start()
        

    try:
        #joining the threads(threads that dont exist will rise a Exception)
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        thread5.join()
        thread6.join()
        thread7.join()
        thread8.join()
    except NameError:
        pass  #Thread has already completed execution or does not exist
