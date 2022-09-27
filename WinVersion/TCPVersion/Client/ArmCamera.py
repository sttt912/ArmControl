import cv2
import tkinter as tk
from PIL import Image, ImageTk
import os
import numpy as np
import ArmControl


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
red_icon = tk.PhotoImage(file = './icons/red.png')
green_icon = tk.PhotoImage(file = './icons/green.png')



cnf = []
file = open('camera.cnf', mode = 'r', encoding = 'UTF-8')

for line in file:
    cnf.append(line) 

file.close()


#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(int(cnf[0]))
cap2 = cv2.VideoCapture(int(cnf[1]))


def servoUpdateadd():
    ArmControl.ServoAddAngle()
    if ArmControl.servoCheckStatus():
        color_button.config(image = green_icon)
    else:
        color_button.config(image = red_icon)
    print(ArmControl.getServo())
    
def servoUpdateSubtract():
    ArmControl.ServoSubtractAngle()
    if ArmControl.servoCheckStatus():
        color_button.config(image = green_icon)
    else:
        color_button.config(image = red_icon)
    print(ArmControl.getServo())
    
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


video_button = tk.Button(imageFrame, image = right_icon, command = ArmControl.XCordinatesAdd)
video_button.place(x=180, y = 400)
photo_button = tk.Button(imageFrame, image = left_icon, command = ArmControl.XCordinatesSubtract)
photo_button.place(x=320, y = 400)
gallery_button = tk.Button(imageFrame, image = up_icon, command = ArmControl.YCordinatesAdd)
gallery_button.place(x=250, y = 340)
gallery_button = tk.Button(imageFrame, image = down_icon, command = ArmControl.YCordinatesSubtract)
gallery_button.place(x=250, y = 460)
gallery_button = tk.Button(imageFrame, image = zplus_icon, command = ArmControl.ZCordinatesAdd)
gallery_button.place(x=50, y = 340)
gallery_button = tk.Button(imageFrame, image = zminus_icon, command = ArmControl.ZCordinatesSubtract)
gallery_button.place(x=50, y = 460)
gallery_button = tk.Button(imageFrame, image = splus_icon, command = servoUpdateadd)
gallery_button.place(x=400, y = 340)
gallery_button = tk.Button(imageFrame, image = sminus_icon, command = servoUpdateSubtract)
gallery_button.place(x=400, y = 460)
color_button = tk.Button(imageFrame, image = red_icon)
color_button.place(x=600, y = 460)

    
show_frame()
window.mainloop()

