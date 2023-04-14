import cv2
import numpy as np
import mediapipe as mp
import time

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
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

    x = mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
    l = cv2.Laplacian(img, x, cv2.CV_64F)
    Time_2 = time.time()
    fps = 1/(Time_2-Time_1)
    Time_1 = Time_2

    cv2.putText(img, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow('image', l)
    cv2.waitKey(1)

    # Take each frame
    _, frame = cap.read()
    # Convert to HSV for simpler calculations
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Calculation of Laplacian
    laplacian = cv2.Laplacian(frame, cv2.CV_64F)
    cv2.imshow('laplacian', laplacian)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break


cv2.destroyAllWindows()
# release the frame
cap.release()