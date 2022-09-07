import os
import serial
import time
from datetime import datetime
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


cnf = []
file = open('data.cnf', mode = 'r', encoding = 'UTF-8')

for line in file:
    cnf.append(line) 

file.close()

cmd1 = str(cnf[0])[:-1]
cmd2 = int(cnf[1])

ser = serial.Serial(cmd1, cmd2)
time.sleep(2)

x = 0
y = 0
z = 0
servo_angle = 150

def command(ser, command):
  #start
  ser.write(str.encode(command)) 
  
  while True:
    line = ser.readline()
    if line == b'ok\n':
        break

def setZero():
    global x
    global y
    global z
    x = 0
    y = 0
    z = 0
    strw = "G0 X"+str(x) + " Y"+str(y)+" Z"+str(z)+"\r\n"
    command(ser, strw)
    strw = "M280 P0 S"+str(90)+"r\n"
    command(ser, strw)


class  MyHandler(FileSystemEventHandler):
    def  on_modified(self,  event):
      with open('cmd/data.json') as f:
        templates = json.load(f)

      for section, commands in templates.items():
        if(section=='Servo'):
          print("M280 P0 S" + str(commands[1]) +"r\n")
          strw = "M280 P0 S" + str(commands[1]) + "r\n"
          command(ser, strw)
        elif(section == 'Move'):
          print(str(commands[0])+str(commands[1])+" "+ str(commands[2])+str(commands[3])+" "+ str(commands[4])+str(commands[5])+" "+ str(commands[6])+str(commands[7]))
          strw = str(commands[0])+str(commands[1])+" "+ str(commands[2])+str(commands[3])+" "+ str(commands[4])+str(commands[5])+" "+ str(commands[6])+str(commands[7]) + "\r\n"
          command(ser, strw)
        else:
          print("Invalid command")
      
      #print(f'event type: {event.event_type} path : {event.src_path}')
    
    def  on_created(self,  event):
         print(f'event type: {event.event_type} path : {event.src_path}')
    def  on_deleted(self,  event):
         print(f'event type: {event.event_type} path : {event.src_path}')

if __name__ ==  "__main__":
    setZero()
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler,  path='cmd\\',  recursive=False)
    observer.start()
    
    try:
        while  True:
            m = 0
    except  KeyboardInterrupt:
        observer.stop()
        observer.join()