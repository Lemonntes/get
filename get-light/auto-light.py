import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
led = 26
sen = 6

GPIO.setup(led, GPIO.OUT)
GPIO.setup(sen, GPIO.IN)
while True:
    GPIO.output(led, not GPIO.input(sen))
