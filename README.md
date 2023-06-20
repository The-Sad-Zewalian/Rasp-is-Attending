# Rasp-is-Attending

This project is a facial recognition attendance system developed on a Raspberry Pi. The system uses a pre-trained model to identify individuals and record attendance. 

## Pre-trained Model

We used [face_recognition](https://github.com/ageitgey/face_recognition) library in Python. This library is built on top of the dlib library, which is written in C++ and is highly optimized for facial recognition tasks. One of the main advantages of the face_recognition library is its high accuracy rate of 99.4%. Additionally, the library is designed to be fast, making it ideal for use on a Raspberry Pi, which has limited processing power compared to a desktop computer.

## SideNotes

We added LEDs to the Raspberry Pi. The LEDs were used to indicate whether the model was running or not. When the system was turned off, the red LED would light up, while the green LED would indicate that the model is running. The sliding switch was used to toggle between the two modes.

## Components

The main components of the system are the DatabaseManager.py and main.py.

The DatabaseManager.py is responsible for updating Firebase with the names of faces found in the frames captured by the Pi camera. The main.py contains the Face_Recognition library along with its functions, and is responsible for everything else in the project, including capturing frames from the Pi camera, identifying faces using the pre-trained model, and recording attendance.

![Sample Image 1](FaceRecRasp.gif)
## Requirements

### Software
The project requires Python 3.5 or later and the following libraries:
- [face_recognition](https://github.com/ageitgey/face_recognition)
- firebase_admin
- opencv
- cryptography 3.4.1 (for firebase_admin)
- rustc (for firebase_admin)
  
### Hardware
- Raspberry Pi 4
- Picamera
- some Leds
