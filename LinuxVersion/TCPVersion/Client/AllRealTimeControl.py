import cv2
import tkinter as tk
from PIL import Image, ImageTk
import os
import numpy as np
import ArmControl
    
window = tk.Tk()
window.title("Arm Camera")
window.geometry("960x550")

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



dim = (320, 240)

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
    for i in range(6):
        cap = cv2.VideoCapture(i, cv2.CAP_V4L2)
        ret, frame = cap.read()

        if ret:
            if i == 0:
                frame1 = cv2.resize(cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE), dim, 
                        interpolation = cv2.INTER_AREA)
            elif i==1:
                frame2 = cv2.resize(cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE), dim, 
                        interpolation = cv2.INTER_AREA)
            elif i==2:
                frame3 = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
            elif i==3:
                frame4 = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
            elif i ==4:
                frame5 = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
            elif i==5:
                frame6 = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

        cap.release() 


    result = np.concatenate((np.concatenate((frame1, frame2, frame3), axis=1),
     np.concatenate((frame4, frame5, frame6), axis=1)), axis=0)

    frame = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    
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

