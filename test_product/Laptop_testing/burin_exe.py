from cgi import test
import subprocess
import sys
from easygui import *
import time
import os
import psutil
import datetime
from psutil._common import BatteryTime
import os
import platform
from easygui import *
from api import update_db,validate_serial_num
import cv2
import shutil
test_return ="FAILED"
class Logger(object):
    # def __init__(self):
    def __init__(self,LOG_FILE_NAME="Default.log"):
        # self.terminal = sys.stdout
        # now = datetime.now()
        # current_time    = now.strftime("%d_%m_%Y_%H_%M_%S")
        # # LOG_FILE_NAME   = "D:/EXI_SW_DUMPs/CAN_LOGS/BDU_LOGS_32C1A100498" + current_time + ".txt"
        # LOG_FILE_NAME   = "D:/EXI_SW_DUMPs/CAN_LOGS/BDU_LOGS_32C1A100301_" + current_time + ".txt"
        self.terminal = sys.stdout
        self.log = open(LOG_FILE_NAME, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  

    def flushu(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass    



def burin_log_test(test_log):
    try:
        # test_log=[]
        test_return="PASSED"
        with open(r"C:\Users\Administrator\Desktop\BIT_log.log","r",encoding="utf-16-le") as f:

            Pass_arr =['CPU','Memory (RAM)','2D Graphics','Temperature','Sound','Disk (C:)']
            data = f.readlines() # read all lines at once
            test_output = str(data)
            print(len(data))
            test_res=[]
            for i in range(len(data)):
                if "Test Name                   Cycles   Operations      Result Errors   Last Error" in data[i]:
                    print("+fount+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    for j in range(len(Pass_arr)):
                        if Pass_arr[j] in data[i+j+1] and "PASS" in data[i+j+1]:
                            print(data[i+j+1])
                            test_log.append(f"PASSED : {data[i+j+1]}")
                            test_res.append("PASSED")
                        else:
                            print(data[i+j+1])
                            test_log.append(f"FAILED : {data[i+j+1]}")
                            test_res.append("FAILED")


        if "FAILED" in test_res:
            test_return="FAILED"
        else:
            test_return="PASSED"
        print(test_res)
        print(test_return)
    
    except Exception as er:
        test_output = "FAILED"
        print("Failed : No FIle BIT_log file Found",er)
        test_return ="FAILED"
        test_log.append("Failed : No FIle BIT_log file Found")

    return test_return, test_log, test_output

def main_func():
    out_num = enterbox("Enter Serial Number","Laptop Testing (Burnin Log Push)")
    now = datetime.datetime.now()
    # out_num=serial_number
    # now = datetime.datetime.now()
    print("END Time: ", now.strftime("%H:%M:%S"))

    logpath = 'C:/LAPTOP_LOGS/'
    isdir = os.path.isdir(logpath) 
    if isdir == False:
        os.mkdir(logpath) 

    subFolder = logpath +  "LAPTOP_LOGS_" + now.strftime("%d_%m_%Y") + "/"
    isdir = os.path.isdir(subFolder) 
    if isdir == False:
        os.mkdir(subFolder) 

    current_time    = now.strftime("%d_%m_%Y_%H_%M_%S")
    LOG_FILE_NAME   = subFolder + "LAPTOP_LOGS_" + out_num + "_"+ current_time + ".txt"
    
    
    # print("serial_number--------------------",serial_number)
    
    sys.stdout = Logger(LOG_FILE_NAME)
    try:
        data={
            "test_status":"",
            "test_log":"",
            "test_output":""
        }
        test_return="FAILED"
        test_log=[]

        # with open(r'C:\Users\vvdnl\Desktop\Laptop_testing\readme.txt', 'r') as f:
            # serial_number = f.readline()
            # print(serial_number)

            # res=f.read()
            # print(res)
            # test_log.append(res)
            # f.close()
            # serial= res.split("-")
            # serial_num= serial[0]
            # print(serial_num)
        
        test_log=[]

        # out1 = enterbox("Enter Serial Number","Laptop Testing")
        res = validate_serial_num(out_num)
        # data={
        #             'serial_number': [out1],
        #             'stage_id':'47'
        #             }
        
        if res['serial_number']==out_num:
            print("Serial Number Validated succesfull")      
        else:
            out=msgbox(f"{res}", "Serial Validate")
            print('not sucess')




        if "PASSED" in res:
            time.sleep(.5)
            test_return,test_log, test_output = burin_log_test(test_log)
        else:
            test_return="FAILED"
            test_output="FAILED"
            test_log.append("NOt able to run  read Burnin Log. Make Support there is a Burin_log,log File in Desktop")
            print("NOt able to run  read Burnin Log. Make Support there is a Burin_log,log File in Desktop")
            

    except Exception as er:
        print("Error:-",er)
        test_return="FAILED"
        test_output="FAILED"
        test_log.append("FAILED Unable to open serial.txt File")
    
    data["test_status"]=test_return
    data["test_log"]= str(test_log)
    data["test_output"]= test_output
    
    res=update_db(out_num,data)
    out = msgbox(f"MSG:{res}","burning test")
    return test_return,test_log,test_output

# with open('D:/readme.txt', 'r') as f:
#             serial_number = f.readline()
#             print(serial_number)

main_func()
