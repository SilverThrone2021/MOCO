import cv2
import keyboard
import mediapipe as mp
import time
from tkinter import *
from tkvideo import tkvideo as t
from moviepy.editor import *

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
vid_cod = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
#out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
output = cv2.VideoWriter("C:/Users/Jackie/Videos/5.avi", vid_cod, 12, (640,480))


mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils


Time_1 = 0

while True:
   success, img = cap.read()
   imgRGB = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
   results = pose.process(imgRGB)
   print(results.pose_landmarks)
   if results.pose_landmarks:
       mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

       x = mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
       for id, lm in enumerate(results.pose_landmarks.landmark):
           h, w, c = img.shape
           print(id, lm)
           cx, cy = int(lm.x*w), int(lm.y*h)
           cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)


   Time_2 = time.time()
   fps = 1/(Time_2-Time_1)
   Time_1 = Time_2

   cv2.putText(img, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
   ret, frame = cap.read()

   x = mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
   laplacian = cv2.Laplacian(img, x, cv2.CV_64F)
   output.write(laplacian)
   cv2.imshow('image', laplacian)
   cv2.waitKey(1)

   # Take each frame
   #_, frame = cap.read()
   # Convert to HSV for simpler calculations
   #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
   # Calculation of Laplacian
   #laplacian = cv2.Laplacian(frame, cv2.CV_64F)
   cv2.imshow('laplacian', img)

   k = cv2.waitKey(5) & 0xFF
   if keyboard.is_pressed('\x1b'):
       cv2.destroyAllWindows()
       cap.release()
       break

cv2.destroyAllWindows()
cap.release()

time.sleep(5)
cap1 = cv2.VideoCapture('C:/Users/Jackie/Videos/5.avi')

if (cap1.isOpened() == False):
   print("Error opening video stream or file")

while (cap1.isOpened()):
   ret, frame = cap1.read()

   if ret == True:
       cv2.imshow('Frame', frame)

   if cv2.waitKey(25) & 0xFF == ord('\x1b'):
       break

cap.release()
cv2.destroyAllWindows()
