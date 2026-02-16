import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
leds = [16,12,25,17,27,23,22,24]
upb = 9
db = 10
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(upb, GPIO.IN)
GPIO.setup(db, GPIO.IN)
GPIO.output(leds,0)

num = 0
def dec2bin(v):
    return [int(el) for el in bin(v)[3:].zfill(8)]
st = 0.2
while True:
    if GPIO.input(upb):
        num = num +1
        print(num, dec2bin(num))
        time.sleep(st)
    if GPIO.input(db):
        num = num -1
        print(num, dec2bin(num))
        time.sleep(st)
    GPIO.output(leds, dec2bin(num))