import socket

g = 0
x = 0
y = 0
z = 0
servo_angle = 150
HOST = '127.0.0.1' 
PORT = 1331             


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


def UARTstart():
    data = s.recv(5000).decode('utf-8')
    print(data)

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


def servoCheckStatus():
    strw = "M119"
    s.sendall(strw.encode())
    data = s.recv(1024).decode('utf-8')
    print(data)
    
    
def getZCordinates():
    global z
    return z

def getYCordinates():
    global y
    return y

def getXCordinates():
    global x
    return x

def getCordinates():
    strw = "M114"
    s.sendall(strw.encode())
    data = s.recv(1024).decode('utf-8')
    print(data)

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
    strw = "G0 X"+str(x) + " Y"+str(y)+" Z"+str(z)
    s.sendall(strw.encode())
    
def create_servo_move(angle, cmd):
    strw = "M280 P0 S"+str(angle)
    s.sendall(strw.encode())