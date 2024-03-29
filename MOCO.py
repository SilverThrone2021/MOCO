import numpy as np
import cv2
from collections import deque

blueLower = np.array([100, 60, 60]) #// Maroon
blueUpper = np.array([140, 255, 255]) #//Blue
kernel = np.ones((5, 5), np.uint8)
bpoints = [deque(maxlen = 1024)]
gpoints = [deque(maxlen = 1024)]
rpoints = [deque(maxlen= 1024)]
ypoints = [deque(maxlen = 1024)]
bindex = 0
gindex = 0
rindex = 0
yindex = 0

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0
paintWindow = np.zeros((471, 636, 3)) + 255
paintWindow = cv2.rectangle(paintWindow, (40, 1), (140, 65), (0, 0, 0), 2)
paintWindow = cv2.rectangle(paintWindow, (160, 1), (255, 65), colors[0], -1)
paintWindow = cv2.rectangle(paintWindow, (275, 1), (370, 65), colors[1], -1)
paintWindow = cv2.rectangle(paintWindow, (390, 1), (485, 65), colors[2], -1)
paintWindow = cv2.rectangle(paintWindow, (505, 1), (600, 65), colors[3], -1)
cv2.putText(paintWindow, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 2, cv2.LINE_AA)

cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
   (grabbed, frame) = camera.read()
   frame = cv2.flip(frame, 1)
   hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

   frame = cv2.rectangle(frame, (40, 1), (140, 65), (122, 122, 122), -1)
   frame = cv2.rectangle(frame, (160, 1), (255, 65), colors[0], -1)
   frame = cv2.rectangle(frame, (275, 1), (370, 65), colors[1], -1)
   frame = cv2.rectangle(frame, (390, 1), (485, 65), colors[2], -1)
   frame = cv2.rectangle(frame, (505, 1), (600, 65), colors[3], -1)
   cv2.putText(frame, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
   cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
   cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
   cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
   cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)

   if not grabbed:
       break

   blueMask = cv2.inRange(hsv, blueLower, blueUpper)
   blueMask = cv2.erode(blueMask, kernel, iterations=2)
   blueMask = cv2.morphologyEx(blueMask, cv2.MORPH_OPEN, kernel)
   blueMask = cv2.dilate(blueMask, kernel, iterations=1)

   (cnts, _) = cv2.findContours(blueMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   center = None

   if len(cnts) > 0:
       cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
       ((x, y), radius) = cv2.minEnclosingCircle(cnt)
       cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
       M = cv2.moments(cnt)
       center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

       if center[1] <= 65:
           if 40 <= center[0] <= 140:
               bpoints = [deque(maxlen=512)]
               gpoints = [deque(maxlen=512)]
               rpoints = [deque(maxlen=512)]
               ypoints = [deque(maxlen=512)]
               bindex = 0
               gindex = 0
               rindex = 0
               yindex = 0
               paintWindow[67:, :, :] = 255
           elif 160 <= center[0] <= 255:
                   colorIndex = 0 # B
           elif 275 <= center[0] <= 370:
                   colorIndex = 1 #/ G
           elif 390 <= center[0] <= 485:
                   colorIndex = 2 #// R
           elif 505 <= center[0] <= 600:
                   colorIndex = 3 #/// Y
       else:
           if colorIndex == 0:
               bpoints[bindex].appendleft(center)
           elif colorIndex == 1:
               gpoints[gindex].appendleft(center)
           elif colorIndex == 2:
               rpoints[rindex].appendleft(center)
           elif colorIndex == 3:
               ypoints[yindex].appendleft(center)

   else:
       bpoints.append(deque(maxlen=512))
       bindex += 1
       gpoints.append(deque(maxlen=512))
       gindex += 1
       rpoints.append(deque(maxlen=512))
       rindex += 1
       ypoints.append(deque(maxlen=512))
       yindex += 1

   points = [bpoints, gpoints, rpoints, ypoints]
   for i in range(len(points)):
       for j in range(len(points[i])):
           for k in range(1, len(points[i][j])):
               if points[i][j][k - 1] is None or points[i][j][k] is None:
                   continue
               cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
               cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

   cv2.imshow("Tracking", frame)
   cv2.imshow("Paint", paintWindow)



   if cv2.waitKey(1) & 0xFF == ord("\x1b"):
       break
camera.release()
cv2.destroyAllWindows()
