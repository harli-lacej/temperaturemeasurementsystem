from mcp9808 import mcp9808 as MCP9808
import mysql.connector
import time
import threading



st = time.time()

sensor = MCP9808.MCP9808(0x18)
sensor2 = MCP9808.MCP9808(0x19)

def insert_varibles_into_table(deviceID,temperature):
    try:
        connection = mysql.connector.connect(
        host="htl-projekt.com",
        user="harlilacej",
        password="*********",
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

lock = threading.Lock()
def get_data():
    i=0

    for i in range(10):
        lock.acquire()
        if(sensor.begin() == True):
            temp = sensor.read_temp()
            insert_varibles_into_table(1,temp)
            print("Device 1:",temp)
            time.sleep(1.5)
        lock.release()



        
    #lock.release()
def get_data2():
    a=0
    for a in range(10):
        if(sensor2.begin() == True):
                temp2 = sensor2.read_temp()
                insert_varibles_into_table(2,temp2)
                print("Device 2:",temp2)
                time.sleep(1.5)


thread1 = threading.Thread(target=get_data, args=())
thread1.start()
thread2= threading.Thread(target=get_data2, args=())
thread2.start()

thread1.join()
thread2.join()


et = time.time()

# get the execution time
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')
