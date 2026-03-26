import RPi.GPIO as GPIO
import smbus
import time
import numpy as np
import math

class MCP4725:
    def __init__(self, dynamic_range, address=0x61, verbose=True):
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
            return

        if not (0 <= number <= 4095):
            print("Число выходит за разрядность MCP4725 (12 бит)")
            return

        first_byte = self.wm | self.pds | (number >> 8)
        second_byte = number & 0xFF
        self.bus.write_byte_data(self.address, first_byte, second_byte)

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


def get_sin_wave_amplitude(freq, time_val):
    phase = 2 * 3.14 * freq * time_val
    res = (np.sin(phase) + 1) / 2
    return res

def wait_for_sampling_period(sampling_frequency):
    time.sleep(1 / sampling_frequency)


AMPLITUDE = 3.2        
SIGNAL_FREQ = 10       
SAMPLING_FREQ = 1000    
DYNAMIC_RANGE = 3.3    
I2C_ADDRESS = 0x61    

dac = None

try:
    dac = MCP4725(dynamic_range=DYNAMIC_RANGE, address=I2C_ADDRESS, verbose=False)
    start_time = time.time()

    while True:
        current_time = time.time() - start_time
        
        normalized = get_sin_wave_amplitude(SIGNAL_FREQ, current_time)
        voltage = normalized * AMPLITUDE
        dac.set_voltage(voltage)
        wait_for_sampling_period(SAMPLING_FREQ)

except KeyboardInterrupt:
    print("\nОстановка генерации сигнала...")
finally:
    if dac is not None:
        dac.deinit()
    GPIO.cleanup()
