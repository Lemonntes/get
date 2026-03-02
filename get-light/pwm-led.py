import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
led = 26
GPIO.setup(led, GPIO.OUT)
pwm = GPIO.PWM(led, 200)

duty = 0.0
pwm.start(duty)


while True:
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.05)

    duty+= 1.0
    if duty > 100.0:
        duty = 0.0

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








import smbus
class MCP4725:
    def __init__(self, dynamic_range, address=0x61, verbose = True):
        self.bus = smbus.SMBus(1)
    
        self.address = address
        self.wm = 0x00
        self.pds = 0x00
    
        self.verbose = verbose
        self.dynamic_range = dynamic_range

    def deinit(self):
        self.bus.close()

    def set_number(self, number):
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать только целые числа")

        if not (0 <= number <= 4095):
            print("Число выходит за разраядность MCP4752 (12 бит)")

        first_byte = self.wm | self.pds | number >> 8
        second_byte = number & 0xFF
        self.bus.write_byte_data(0x61, first_byte, second_byte)

        if self.verbose:
            print(f"Число: {number}, отправленные по I2C данные: [0x{(self.address << 1):02X}, 0x{first_byte:02X}, 0x{second_byte:02X}]\n")

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            if self.verbose:
                print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 – {self.dynamic_range:.2f} В)")
            self.set_number(0)
            return

        number = int(voltage / self.dynamic_range * 4095)
        self.set_number(number)


if __name__ == "__main__":
    try:
        dac = MCP4725(4.23, 0x61, True)
        
        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")

    finally:
        dac.deinit()












import mcp4725_driver as dac_mod
import signal_generator as sg
import time

AMPLITUDE = 3.2        
SIGNAL_FREQ = 10       
SAMPLING_FREQ = 1000    
DYNAMIC_RANGE = 3.3    
I2C_ADDRESS = 0x61    


try:
    dac = dac_mod.MCP4725(dynamic_range=DYNAMIC_RANGE, address=I2C_ADDRESS, verbose=False)

    start_time = time.time()

    while True:
        current_time = time.time() - start_time
        
        normalized = sg.get_sin_wave_amplitude(SIGNAL_FREQ, current_time)
        voltage = normalized * AMPLITUDE
        dac.set_voltage(voltage)
        sg.wait_for_sampling_period(SAMPLING_FREQ)

finally:
    if dac is not None:
        dac.deinit()











import RPi.GPIO as GPIO
class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose = False):
        self.gpio_pin = gpio_pin
        self.pwm_frequency = pwm_frequency
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT, initial = GPIO.LOW)

        self.pwm = GPIO.PWM(self.gpio_pin, self.pwm_frequency)
        self.pwm.start(0)

    def deinit(self):
        self.pwm.stop()
        GPIO.output(self.gpio_pin, GPIO.LOW)
        GPIO.cleanup()

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            if self.verbose:
                print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 – {self.dynamic_range:.2f} В)")
            self.pwm.ChangeDutyCycle(0)
            return

        duty_cycle = (voltage / self.dynamic_range) * 100.0
        self.pwm.ChangeDutyCycle(duty_cycle)

if __name__ == "__main__":
    try:
        dac = PWM_DAC(12, 500, 3.290, True)
        
        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")

    finally:
        dac.deinit()







































import RPi.GPIO as GPIO
import pwm_dac as pd
import signal_generator as sg
import time
amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000

class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose = False):
        self.gpio_pin = gpio_pin
        self.pwm_frequency = pwm_frequency
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT, initial = GPIO.LOW)

        self.pwm = GPIO.PWM(self.gpio_pin, self.pwm_frequency)
        self.pwm.start(0)

    def deinit(self):
        self.pwm.stop()
        GPIO.output(self.gpio_pin, GPIO.LOW)
        GPIO.cleanup()

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            if self.verbose:
                print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 – {self.dynamic_range:.2f} В)")
            self.pwm.ChangeDutyCycle(0)
            return

        duty_cycle = (voltage / self.dynamic_range) * 100.0
        self.pwm.ChangeDutyCycle(duty_cycle)

try:
    dac = pd.PWM_DAC(12, 10000, 3.3, verbose = False)
    start_time = time.time()

    while True:
        current_time = time.time() - start_time
        
        normalized_amplitude = sg.get_sin_wave_amplitude(signal_frequency, current_time)
        
        voltage = normalized_amplitude * amplitude

        dac.set_voltage(voltage)
        
        sg.wait_for_sampling_period(sampling_frequency)

finally:
    dac.deinit()





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




import RPi.GPIO as GPIO
import signal_generator as sg
import time
import RPi.GPIO as GPIO

def decimal2binary(n):
    return [int(bit) for bit in bin(n)[2:].zfill(8)]

class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose=False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial=GPIO.LOW)

    def deinit(self):
        GPIO.output(self.gpio_bits, GPIO.LOW)
        GPIO.cleanup(self.gpio_bits)

    def set_number(self, number):
        number = max(0, min(255, int(number)))
        bits = decimal2binary(number)
        GPIO.output(self.gpio_bits, bits)

    def set_voltage(self, voltage):
        if voltage < 0.0:
            clamped = 0.0
        elif voltage > self.dynamic_range:
            clamped = self.dynamic_range
            if self.verbose:
                print(f"Напряжение превышает максимум ({self.dynamic_range:.3f} В)")
        else:
            clamped = voltage

        number = int(clamped / self.dynamic_range * 255)
        number = max(0, min(255, number))
        self.set_number(number)


if __name__ == '__main__':
    amplitude = 3.2
    signal_frequency = 10
    sampling_frequency = 1000

    GPIO_PINS = [16, 20, 21, 25, 26, 17, 27, 22]
    DYNAMIC_RANGE = 3.183

    dac = None
    try:
        dac = R2R_DAC(gpio_bits=GPIO_PINS, dynamic_range=DYNAMIC_RANGE, verbose=True)
        start_time = time.time()

        while True:
            t = time.time() - start_time
            norm_amp = sg.get_sin_wave_amplitude(signal_frequency, t)
            voltage = norm_amp * amplitude
            dac.set_voltage(voltage)
            sg.wait_for_sampling_period(sampling_frequency)


    finally:
        if dac is not None:
            dac.deinit()






import numpy as np
import time

def get_sin_wave_amplitude(freq, t):
    sin_val = np.sin(2 * np.pi * freq * t)
    return (sin_val + 1.0) / 2.0

def wait_for_sampling_period(sampling_frequency):    
    period = 1.0 / float(sampling_frequency)
    time.sleep(period)
