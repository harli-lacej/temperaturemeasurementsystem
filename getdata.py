from mcp9808 import mcp9808 as MCP9808
import mysql.connector
import supervisor
import time
import threading
import os
import subprocess
import re
from prettytable import PrettyTable

def insert_varibles_into_table(deviceID,temperature):
    try:
        connection = mysql.connector.connect(
        host="htl-projekt.com",
        user="harlilacej",
        password="!Insy_2021$",
        port=33060,
        database="2023_EcoSense_DA"
        )
        cursor = connection.cursor()
        mySql_insert_query = '''INSERT INTO temperature(deviceID,temperature) VALUES (%s,%s) '''

        record = (deviceID,temperature)
        cursor.execute(mySql_insert_query, record)
        connection.commit()

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

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
