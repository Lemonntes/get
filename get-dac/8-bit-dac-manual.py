import RPi.GPIO as GPIO
pins = [16,20,21,25,26,17,27,22]
GPIO.setmode(GPIO.BCM)
GPIO.setup(pins, GPIO.OUT)
dynamic_range = 3.183
def voltage_to_number(voltage):
    if not (0<=voltage<=dynamic_range):
        print(f'Напряжение выходит за динамический диапазон ЦАП (0.00 - {dynamic_range:.2f} В)')
        print('Устанавливаем 0.0 В')
        return 0
    return int(voltage/dynamic_range*255)
def decimal2binary(n):
    return [int(a) for a in bin(n)[2:].zfill(8)]
def number_to_dac(number):
    num = decimal2binary(number)
    for i in range(8):
        GPIO.output(pins[i], num[i])

try:
    while True:
        try:
            voltage = float(input('Введите напряжение в вольтах: '))
            number = voltage_to_number(voltage)
            number_to_dac(number)
        except ValueError:
            print('Вы ввели не число. Попробуйте еще раз\n')

finally:
    GPIO.output(pins, 0)
    GPIO.cleanup()
