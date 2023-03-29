import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Hand Detector
detector = HandDetector(detectionCon=0.1, maxHands=2)

# Find Function
# x is the raw distance y is the value in cm
x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x, y, 2)  # y = Ax^2 + Bx + C

# Loop
while True:
    success, img = cap.read()
    hands = detector.findHands(img, draw=False)
    handdots = detector.findHands(img)

    if len(hands)>0:
        lmList = hands[0]['lmList']
        x, y, w, h = hands[0]['bbox']
        x1, y1, z1 = lmList[5]
        x2, y2, z2 = lmList[17]

        distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
        A, B, C = coff
        distanceCM = A * distance ** 2 + B * distance + C

        # print(distanceCM, distance)
        cvzone.putTextRect(img, f'{int(distance)} 3d', (x + 5, y - 10))

    '''if len(hands)>0:
        lmList = hands[0]['lmList']
        x, y, w, h = hands[0]['bbox']
        x1, y1, z1 = lmList[5]
        x2, y2, z2 = lmList[17]

        distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
        A, B, C = coff
        distanceCM = A * distance ** 2 + B * distance + C

        # print(distanceCM, distance)
        cvzone.putTextRect(img, f'{int(distance)} 2d', (x + 5, y - 10))'''

    cv2.imshow("Image", img)
    cv2.waitKey(1)
