import os
import serial
import time
from datetime import datetime


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
step = 1

def command(ser, command):
  #start
  ser.write(str.encode(command)) 
  
  while True:
    line = ser.readline()
    if line == b'ok\n':
        break

def splus(step=10):
    global servo_angle
    servo_angle+=step
    strw = "M280 P0 S"+str(servo_angle)+"r\n"
    command(ser, strw)

def sminus(step=10):
    global servo_angle
    servo_angle-=step
    strw = "M280 P0 S"+str(servo_angle)+"r\n"
    command(ser, strw)
    
def zplus(step=1):
    global x
    global y
    global z
    z+=step
    strw = "G0 X"+str(x) + " Y"+str(y)+" Z"+str(z)+"\r\n"
    command(ser, strw)
    
def zminus(step=1):
    global x
    global y
    global z
    z-=step
    strw = "G0 X"+str(x) + " Y"+str(y)+" Z"+str(z)+"\r\n"
    command(ser, strw)
    
def up(step=1):
    global x
    global y
    global z
    y+=step
    strw = "G0 X"+str(x) + " Y"+str(y)+" Z"+str(z)+"\r\n"
    command(ser, strw)
    
def down(step=1):
    global x
    global y
    global z
    y-=step
    strw = "G0 X"+str(x) + " Y"+str(y)+" Z"+str(z)+"\r\n"
    command(ser, strw)
    
def left(step=1):
    global x
    global y
    global z
    x-=step
    strw = "G0 X"+str(x) + " Y"+str(y)+" Z"+str(z)+"\r\n"
    command(ser, strw)
    
def right(step=1):
    global x
    global y
    global z
    x+=step
    strw = "G0 X"+str(x) + " Y"+str(y)+" Z"+str(z)+"\r\n"
    command(ser, strw)

def setZero():
    global x
    global y
    global z
    x = 0
    y = 0
    z = 0
    strw = "G0 X"+str(x) + " Y"+str(y)+" Z"+str(z)+"\r\n"
    command(ser, strw)
    #strw = "M280 P0 S" + str(90)+"r\n"
    #command(ser, strw)


if __name__ ==  "__main__":
    setZero()
    while True:
        cmd = input("Enter command:")
        if(cmd == 'step'):
            step = int(input("Enter step:"))
        elif (cmd == 'left'):
            left(step)
        elif (cmd == 'right'):
            right(step)
        elif (cmd == 'up'):
            up(step)    
        elif (cmd == 'down'):
            down(step)
        elif (cmd == 'zero'):
            setZero()
        elif (cmd == 'exit'):
            break;
        else:
            print("Invalid command")

        print("X: "+str(x) + " Y: "+str(y) + " Z:"+ str(z) + " Servo: " + str(servo_angle) + " Step: "+str(step))