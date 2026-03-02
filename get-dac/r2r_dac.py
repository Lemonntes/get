import RPi.GPIO as GPIO

def decimal2binary(n):
    return [int(a) for a in bin(n)[2:].zfill(8)]

class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose = False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial = 0)

    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()

    def set_number(self, number):
        number = max(0, min(255, int(number)))
        bits = decimal2binary(number)
        GPIO.output(self.gpio_bits, bits)

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            if self.verbose:
                print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 – {self.dynamic_range:.2f} В)")
            self.set_number(0)
            return

        number = int(voltage / self.dynamic_range * 255)
        self.set_number(number)

if __name__ == '__main__':
    try:
        dac = R2R_DAC([16,20,21,25,26,17,27,22], 3.183, True)

        while True:
            try:
                voltage = float(input('Введите напряжение в вольтах: '))
                dac.set_voltage(voltage)

            except ValueError:
                print('Вы ввели не число. Попробуйте еще раз\n')

    finally:
        dac.deinit()
