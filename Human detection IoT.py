import cv2
import RPi.GPIO as GPIO

import numpy as np
import time
from time import sleep

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# To capture video from webcam.
cap = cv2.VideoCapture(0)

water = 4

ir = 26
servo_pin = 17

motor = 2
light = 3

GPIO.setmode(GPIO.BCM)

GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(water, GPIO.IN)

GPIO.setup(ir, GPIO.IN)
GPIO.setup(light, GPIO.OUT)
GPIO.setup(motor, GPIO.OUT)
GPIO.output(light, GPIO.HIGH)
GPIO.output(motor, GPIO.HIGH)
p = GPIO.PWM(servo_pin, 50)
p.start(0)
p.ChangeDutyCycle(0)

a = True
while a:

    print(GPIO.input(ir))

    # Read the frame

    if GPIO.input(water) == 1:

        GPIO.output(motor, GPIO.LOW)
    else:

        GPIO.output(motor, GPIO.HIGH)
    while True:
        if (GPIO.input(ir)) == 1:
            GPIO.output(light, GPIO.HIGH)
            if GPIO.input(water) == 1:

                GPIO.output(motor, GPIO.LOW)
            else:

                GPIO.output(motor, GPIO.HIGH)
            continue
        if GPIO.input(water) == 1:

            GPIO.output(motor, GPIO.LOW)
        else:

            GPIO.output(motor, GPIO.HIGH)
        _, img = cap.read()

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Draw the rectangle around each face
        for (x, y, w, h) in faces:

            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            print("people")
            GPIO.output(light, GPIO.LOW)
            break
        else:
            print("NO people")
            GPIO.output(light, GPIO.HIGH)

        # Display
        cv2.imshow('img', img)

        # Stop if escape key is pressed
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    # Release the VideoCapture object
    cap.release()
