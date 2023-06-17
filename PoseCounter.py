import cv2
import imutils
import mediapipe as mp
import numpy as np
import time

from Utils.CameraCapture import WebcamVideoStream

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
cap = WebcamVideoStream(src=0).start()
pTime = 0
## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.2, min_tracking_confidence=0.2,model_complexity=0) as pose:
    while True:

        frame = cap.read()  # reading Frame
        frame = imutils.resize(frame, width=400)
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                  )

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(image, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                    1, (255, 0, 0), 3)
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
