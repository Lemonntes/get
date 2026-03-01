import RPi.GPIO as GPIO

class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose=False):
        self.gpio_pin = gpio_pin
        self.pwm_frequency = pwm_frequency
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        
        self.pwm = GPIO.PWM(self.gpio_pin, self.pwm_frequency)
        self.pwm.start(0)
        
        if self.verbose:
            print(f"PWM DAC инициализирован на пине {gpio_pin}, частота: {pwm_frequency} Гц")
    
    def deinit(self):
        self.pwm.stop()
        GPIO.cleanup(self.gpio_pin)
        
        if self.verbose:
            print("PWM DAC деинициализирован")
    
    def set_voltage(self, voltage):
        voltage = max(0, min(self.dynamic_range, voltage))
        
        duty_cycle = (voltage / self.dynamic_range) * 100
        
        self.pwm.ChangeDutyCycle(duty_cycle)
        
        if self.verbose:
            print(f"Запрошено напряжение: {voltage:.3f} В, установлен duty cycle: {duty_cycle:.1f}%")

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
