# home_20222
import RPi.GPIO as GPIO
from time import sleep
from ubidots import ApiClient

import time

from gpiozero import Servo

water = 4
servo = Servo(17)
motor = 2
light = 3

GPIO.setup(water, GPIO.IN)
GPIO.setup(light, GPIO.OUT)
GPIO.setup(motor, GPIO.OUT)
GPIO.output(light, GPIO.HIGH)
GPIO.output(motor, GPIO.HIGH)
print("hello")
api = ApiClient(token='BBFF-YFJcg7ZMEkqpoCphNdJh05NxPCaU2r')

x = api.get_variable('625e51133fde4103d6b1ce89')
y = api.get_variable('625e5229184466000ab70cdd')
g = api.get_variable('625e5246b88ac802b7b70b5e')

x.save_value({'value': 0})
y.save_value({'value': 0})
g.save_value({'value': 0})
print(x, y, g)

while True:
    if GPIO.input(water) == 1:
        y.save_value({'value': 1})
        GPIO.output(motor, GPIO.LOW)
    else:
        y.save_value({'value': 0})
        GPIO.output(motor, GPIO.HIGH)
    time.sleep(1)
    last_value1 = g.get_values(1)
    print(last_value1)
    time.sleep(1)
    if int(last_value1[0]['value']) == 1:
        servo.min()
        print("door opened")

    else:
        servo.max()
        print("door closed")
    time.sleep(1)
    last_value = x.get_values(1)
    time.sleep(1)
    if int(last_value[0]['value']) == 1:
        print("door opened")
        GPIO.output(light, GPIO.LOW)
        print("light ON")
    else:
        GPIO.output(light, GPIO.HIGH)
        print("light OFF")
