import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
q = [16,20,21,25,26,17,27,22]
dynrange = 3.3
GPIO.setup(q, GPIO.OUT)

def vtn(v):  
    if not (0.0 <= v <=dynrange):
        print(f"напряжение выходит за динамический диапазон цап(0.00-{dynrange:.2f}B)")
        print("Устанавливаем 0.0В")
        return 0

    return int(v/dynrange*255)

def n2d(v):
    for i in range(8):
        GPIO.output(q[i], (n>>i)&1)

try:
    while True:
        try:

            v = float(input("Веедите напряжени в вольтах:"))
            n = vtn(v)
            n2d(n)

        except ValueError:
            print("Вы ввели не число, попробуйте еще раз\n")

finally:
    GPIO.output(q,0)
    GPIO.cleanup()
