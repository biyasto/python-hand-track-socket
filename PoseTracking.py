import cv2
from cvzone.PoseModule import PoseDetector
import time

width, height = 1280,720

cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)

detector = PoseDetector()
posList = []
pTime = 0
while True:
    success, flip_img = cap.read()
    img = cv2.flip(flip_img, 1)
    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img)

    if bboxInfo:
        lmString = ''
        for lm in lmList:
            lmString += f'{lm[1]},{img.shape[0] - lm[2]},{lm[3]},'
        posList.append(lmString)

    #print(len(posList))

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    print(fps)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    #if key == ord('s'):
     #   with open("AnimationFile.txt", 'w') as f:
      #      f.writelines(["%s\n" % item for item in posList])