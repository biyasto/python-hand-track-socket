import cv2
from cvzone.HandTrackingModule import HandDetector
import socket
import time

width, height = 1280,720

cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)
pTime = 0


#Hand detector
detector = HandDetector(maxHands=2, detectionCon=0.5)

#unity communicate
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)
while True:
    success, img = cap.read()
    flip_img = cv2.flip(img, 1)
    #hands

    hands, flip_img = detector.findHands(flip_img)
    data = []

    if hands:
        hand = hands[0]
        lmList = hand['lmList']


        for lm in lmList:
            data.extend([lm[0],height- lm[1], lm[2]])

       # lm = lmList[8]
        #data.extend([lm[0], height - lm[1], lm[2]])

        print(data)
        sock.sendto(str.encode(str(data)),serverAddressPort)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(flip_img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)


    cv2.imshow("Image",flip_img)
    cv2.waitKey(1)

