# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright (c) 2024, System Level Solutions (India) Pvt. Ltd.
#
# Purpose   : Bulk message 
# Package   : python_scripts
# File name : wpmsg.py
# Project   : Alpesh Dhokia
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import os 
import csv
import time
import pywhatkit
import keyboard

from readchar import readkey, key
from datetime import datetime

wait_time_1 = 65
close_time_1 = 70
wait_time = 8
close_time = 10
country_code = "+91"
image_name = ""
message = ""
# schedule_time = "{}:{}".format(datetime.now().hour,datetime.now().minute+1)

while True:
    image = input("Do you want to send image/photo ? [yes/no]\n\t")
    if image.lower() == 'yes' or image.lower() == 'no':
        break
if image.lower() == 'yes':
    files = os.listdir()
    for _file in files:
        if _file.endswith(".PNG") or _file.endswith(".jpg"):
            image_name = _file
            print("Sending image/photo :",image_name)
            break
    if not image_name:
        print("Can't find (.PNG or .jpg) image /photo in the directory.")  

file=open('number2.csv', mode ='r')    
csvFile = csv.reader(file, delimiter = ",")
num_list=[]
message_list = []
time_list = []
for line in csvFile:    
    num=line[0].strip()
    num_list.append(num)
    message_list.append(line[1])
    time_list.append(line[2])

message = message_list[1]
print("Message: {}".format(message))
schedule_time = time_list[1]
if schedule_time != '':    
    hour = int(schedule_time[:2])
    minut = int(schedule_time[3:])
count = 0
for contact in num_list[1:]:
    count += 1
    contact = country_code+contact
    if image_name != "":
        if schedule_time != '' or not contact[1:].isdigit():
            print("ERROR:Not Possible Image/scheduled-time/whatsapp-group")
            break
        else:
            if count == 1:
                pywhatkit.sendwhats_image(contact, "{}".format(image_name), 
                                        message,
                                        wait_time_1, 
                                        True, close_time_1)
                time.sleep(60)
            else:
                pywhatkit.sendwhats_image(contact, "{}".format(image_name), 
                                          message, wait_time, True, close_time)
    else:        
        if count == 1:
            if not contact[1:].isdigit() :
                if schedule_time != '':
                    pywhatkit.sendwhatmsg_to_group(contact, message, hour, minut,
                                                wait_time_1, True, close_time_1)                    
                else:
                    pywhatkit.sendwhatmsg_to_group_instantly(contact, message, 
                                                        wait_time_1, True, close_time_1)             
            else:
                if schedule_time != '':
                    pywhatkit.sendwhatmsg(contact, message, hour, minut , 
                                          wait_time_1, True, close_time_1)                    
                else:

                    pywhatkit.sendwhatmsg_instantly(contact, message, wait_time_1, 
                                                    True, close_time_1)
            time.sleep(60)
        else:
            if not contact[1:].isdigit() :                
                pywhatkit.sendwhatmsg_to_group_instantly(contact, message, 
                                                         wait_time, True, 
                                                         close_time)             
            else:                
                pywhatkit.sendwhatmsg_instantly(contact, message, wait_time, 
                                                True, close_time)

print("+++++ Completed. +++++")    
