#!/usr/bin/python3
import os
import cv2
import time
import glob
import numpy as np
from time import sleep 
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
import face_recognition
from picamera import PiCamera
from DatabaseManager import DatabaseManager 

GledPin = 14
RledPin = 18
SPin = 15
GPIO.setmode(GPIO.BCM)
GPIO.setup(SPin,GPIO.IN)
GPIO.setup(GledPin,GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RledPin,GPIO.OUT, initial=GPIO.LOW)
dbManager = DatabaseManager()
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
#camera.framerate = 20
frame = np.empty((480, 640, 3), dtype=np.uint8)

# Create arrays of known face encodings and their names
known_face_encodings = []
known_face_names = []

for img in glob.glob("./Known/*.jpg"):
    _image = face_recognition.load_image_file(img)
    _face_encoding = face_recognition.face_encodings(_image)[0]
    known_face_encodings.append(_face_encoding)
    known_face_names.append(os.path.splitext(os.path.basename(img))[0])


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []

while True:
    
    if GPIO.input(SPin):
        camera.capture(frame, format="rgb")
        GPIO.output(GledPin,GPIO.HIGH)
        GPIO.output(RledPin,GPIO.LOW)
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame.astype(np.uint8), face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            #use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)
            if name != "Unknown":
                print(f'Found {name}')
                dbManager.add_attendance_now(name, ignore_day_duplicate = True)
                
            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # rescale points back to original image size
                top*=4;bottom*=4
                right*=4;left*=4
                
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 1)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 15), (right, bottom), (0, 255, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 1, bottom - 1), font, 1.0, (255, 255, 255), 1)
    
            # Display the resulting image
            cv2.imshow('Camera Feed', frame)
            #time.sleep(0.1)
    else:
        cv2.destroyAllWindows()
        GPIO.output(GledPin,GPIO.LOW)
        GPIO.output(RledPin,GPIO.HIGH)
        break
        
    
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the cv2 window
GPIO.output(GledPin,GPIO.LOW)
cv2.destroyAllWindows()
