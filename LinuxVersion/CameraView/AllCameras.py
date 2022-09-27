import cv2
from PIL import Image
import os
import numpy as np

dim = (320, 240)
start = True
cadr = 0
while True:
	for i in range(6):
		if start:
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
	
		if start==False:
			if i == 0:
				cap = cv2.VideoCapture(i, cv2.CAP_V4L2)
				_, frame = cap.read()
				frame1 = cv2.resize(cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE), dim, 
						interpolation = cv2.INTER_AREA)
			elif i==1:
				cap = cv2.VideoCapture(i, cv2.CAP_V4L2)
				_, frame = cap.read()
				frame2 = cv2.resize(cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE), dim, 
						interpolation = cv2.INTER_AREA)	
			elif cadr>=5 and i== 2:
				cap = cv2.VideoCapture(i, cv2.CAP_V4L2)
				_, frame = cap.read()
				frame3 = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
			elif cadr>=5 and i==3:
				cap = cv2.VideoCapture(i, cv2.CAP_V4L2)
				_, frame = cap.read()
				frame4 = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
			elif cadr>=5 and i==4:
				cap = cv2.VideoCapture(i, cv2.CAP_V4L2)
				_, frame = cap.read()
				frame5 = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
			elif cadr>=5 and i==5:
				cap = cv2.VideoCapture(i, cv2.CAP_V4L2)
				_, frame = cap.read()
				frame6 = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

		
		cap.release() 


	result = np.concatenate((np.concatenate((frame1, frame2, frame3), axis=1),
	 np.concatenate((frame4, frame5, frame6), axis=1)), axis=0)
	cam = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

	cv2.imshow('Camera',cam) 

	start=False
	cadr += 1
	print(cadr)
	if(cadr>=6):
		cadr = 0
		print("Cadr")

	keyCode = cv2.waitKey(10) & 0xFF
	if keyCode == 27 or keyCode == ord('q'):
    		break

cv2.destroyAllWindows()