#!/usr/bin/env python
# coding: utf-8

# In[23]:


import cv2
import tkinter as tk
from PIL import Image, ImageTk
import os
import numpy as np
import json 


g = 0
x = 0
y = 0
z = 0
servo_angle = 150

  
def splus(step=10):
    global servo_angle
    servo_angle+=step
    create_servo_json(servo_angle, 'Servo')

def sminus(step=10):
    global servo_angle
    servo_angle-=step
    create_servo_json(servo_angle, 'Servo')
    
def zplus(step=1):
    global g
    global x
    global y
    global z
    z+=step
    create_move_json(g,x,y,z, 'Move')
    
def zminus(step=1):
    global g
    global x
    global y
    global z
    z-=step
    create_move_json(g,x,y,z, 'Move')
    
def up(step=1):
    global g
    global x
    global y
    global z
    y+=step
    create_move_json(g,x,y,z, 'Move')
    
def down(step=1):
    global g
    global x
    global y
    global z
    y-=step
    create_move_json(g,x,y,z, 'Move')
    
def left(step=1):
    global g
    global x
    global y
    global z
    x-=step
    create_move_json(g,x,y,z, 'Move')
    

def create_move_json(g, x, y, z, cmd):
    trunk_template = [
        'G', g,
        'X', x,
        'Y', y,
        'Z', z
    ]

    to_json = {cmd: trunk_template}
    
    with open('cmd/data.json', 'w') as f:
        json.dump(to_json, f, sort_keys=True, indent=2)
    
def create_servo_json(angle, cmd):
    trunk_template = [
        'G', angle
    ]

    to_json = {cmd: trunk_template}
    
    with open('cmd/data.json', 'w') as f:
        json.dump(to_json, f, sort_keys=True, indent=2)
        
def right(step=1):
    global g
    global x
    global y
    global z
    x+=step
    create_move_json(g,x,y,z, 'Move')
    
window = tk.Tk()
window.title("Arm Camera")
window.geometry("980x650")

imageFrame = tk.Frame(window)
imageFrame.grid(row=0, column=0, padx=5, pady =0)
label = tk.Label(imageFrame)
label.grid(row=0, column=0)

left_icon = tk.PhotoImage(file = './icons/left.png')
right_icon = tk.PhotoImage(file = './icons/right.png')
up_icon = tk.PhotoImage(file = './icons/up.png')
down_icon = tk.PhotoImage(file = './icons/down.png')
zplus_icon = tk.PhotoImage(file = './icons/zplus.png')
zminus_icon = tk.PhotoImage(file = './icons/z_minus.png')

splus_icon = tk.PhotoImage(file = './icons/Splus.png')
sminus_icon = tk.PhotoImage(file = './icons/Sminus.png')



cnf = []
file = open('camera.cnf', mode = 'r', encoding = 'UTF-8')

for line in file:
    cnf.append(line) 

file.close()


cap = cv2.VideoCapture(int(cnf[0]))
cap2 = cv2.VideoCapture(int(cnf[1]))


def show_frame():
    global frame
    _, frame = cap.read()
    _, frame1 = cap2.read()
    
    rotate_90 = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE) 
    rotate_90_counter = cv2.rotate(frame1, cv2.ROTATE_90_COUNTERCLOCKWISE) 
    
    img_flip1=cv2.flip(rotate_90,1)
    img_flip_1=cv2.flip(rotate_90_counter,1)

    numpy_horizontal_concat = np.concatenate((img_flip1, img_flip_1), axis=1)
    frame = cv2.cvtColor(numpy_horizontal_concat, cv2.COLOR_BGR2RGB)
    
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    label.image = imgtk
    label.configure(image = imgtk)
    label.after(10, show_frame)


video_button = tk.Button(imageFrame, image = right_icon, command = right)
video_button.place(x=180, y = 400)
photo_button = tk.Button(imageFrame, image = left_icon, command = left)
photo_button.place(x=320, y = 400)
gallery_button = tk.Button(imageFrame, image = up_icon, command = up)
gallery_button.place(x=250, y = 340)
gallery_button = tk.Button(imageFrame, image = down_icon, command = down)
gallery_button.place(x=250, y = 460)
gallery_button = tk.Button(imageFrame, image = zplus_icon, command = zplus)
gallery_button.place(x=50, y = 340)
gallery_button = tk.Button(imageFrame, image = zminus_icon, command = zminus)
gallery_button.place(x=50, y = 460)
gallery_button = tk.Button(imageFrame, image = splus_icon, command = splus)
gallery_button.place(x=400, y = 340)
gallery_button = tk.Button(imageFrame, image = sminus_icon, command = sminus)
gallery_button.place(x=400, y = 460)
    
show_frame()
window.mainloop()

