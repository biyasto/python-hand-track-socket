import cv2
import imutils
import mediapipe as mp
import time
from imutils.video import WebcamVideoStream
# Initializing Hand Tracking Modules
mpHands = mp.solutions.hands
Hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
pTime=0

# Capturing Video From Camera
#cap = cv2.VideoCapture(0)

cap = WebcamVideoStream(src=0).start()


# Checking Camera is Opened or Not
while True:
    img = cap.read() # reading Frame
    img = imutils.resize(img,width=400)
    converted_image = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) # converting BGR to RGB
    results = Hands.process(converted_image) # Processing Image for Tracking

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime


    if results.multi_hand_landmarks: # Getting Landmark(location) of Hands if Exists
        for hand_in_frame in results.multi_hand_landmarks: # looping through hands exists in the Frame
            mpDraw.draw_landmarks(img,hand_in_frame, mpHands.HAND_CONNECTIONS) # drawing Hand Connections
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)
    cv2.imshow("Handtrack", img) # showing Video

    if cv2.waitKey(1) == 113: # 113 - Q : press on Q : Close Video
        break