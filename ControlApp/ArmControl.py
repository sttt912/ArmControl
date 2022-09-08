import socket
import json

g = 0
x = 0
y = 0
z = 0
servo_angle = 150


def setZero():
    global g
    global x
    global y
    global z
    x=0
    y=0
    z=0
    create_move(g,x,y,z, 'Move')

def setCordinates(localx, localy, localz):
    global g
    global x
    global y
    global z
    x = localx
    y = localy
    z = localz
    create_move(g,x,y,z, 'Move')

def getZCordinates():
    global z
    return z

def getYCordinates():
    global y
    return y

def getXCordinates():
    global x
    return x

def getXCordinates():
    global x
    return x

def getServo():
    global servo_angle
    return servo_angle

def setServo(step=10):
    global servo_angle
    servo_angle=step
    create_servo_move(servo_angle, 'Servo')
    
def setZCordinates(step=1):
    global g
    global x
    global y
    global z
    z+=step
    create_move(g,x,y,z, 'Move')
    
def setYCordinates(step=1):
    global g
    global x
    global y
    global z
    y+=step
    create_move(g,x,y,z, 'Move')
    
def setXCordinates(step=1):
    global g
    global x
    global y
    global z
    x+=step
    create_move(g,x,y,z, 'Move')
    

def ServoAddAngle(step=10):
    global servo_angle
    servo_angle+=step
    create_servo_move(servo_angle, 'Servo')

def ServoSubtractAngle(step=10):
    global servo_angle
    servo_angle-=step
    create_servo_move(servo_angle, 'Servo')
    
def ZCordinatesAdd(step=1):
    global x
    global y
    global z
    z+=step
    create_move(g,x,y,z, 'Move')
    
def ZCordinatesSubtract(step=1):
    global x
    global y
    global z
    z-=step
    create_move(g,x,y,z, 'Move')
    
def YCordinatesAdd(step=1):
    global x
    global y
    global z
    y+=step
    create_move(g,x,y,z, 'Move')
    
def YCordinatesSubtract(step=1):
    global x
    global y
    global z
    y-=step
    create_move(g,x,y,z, 'Move')
    
def XCordinatesSubtract(step=1):
    global x
    global y
    global z
    x-=step
    create_move(g,x,y,z, 'Move')
    
def XCordinatesAdd(step=1):
    global x
    global y
    global z
    x+=step
    create_move(g,x,y,z, 'Move')

    
 def create_move(g, x, y, z, cmd):
    trunk_template = [
        'G', g,
        'X', x,
        'Y', y,
        'Z', z
    ]

    to_json = {cmd: trunk_template}
    
    with open('cmd/data.json', 'w') as f:
        json.dump(to_json, f, sort_keys=True, indent=2)
    
def create_servo_move(angle, cmd):
    trunk_template = [
        'G', angle
    ]

    to_json = {cmd: trunk_template}
    
    with open('cmd/data.json', 'w') as f:
        json.dump(to_json, f, sort_keys=True, indent=2)