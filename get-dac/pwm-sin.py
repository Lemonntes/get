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
