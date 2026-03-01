import RPi.GPIO as GPIO

class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose=False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial=0)

    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()
    

        for i, bit in enumerate(self.gpio_bits):
            GPIO.output(bit, (number >> i) & 1)
        
        if self.verbose:
            actual_voltage = (number / 255) * self.dynamic_range
            print(f"Установлено число: {number} (0x{number:02X}), "
                  f"напряжение: {actual_voltage:.3f} В")
    
    def set_voltage(self, voltage):
        voltage = max(0, min(self.dynamic_range, voltage))
      
        number = int((voltage / self.dynamic_range) * 255)
        self.set_number(number)
        
        if self.verbose:
            print(f"Запрошено напряжение: {voltage:.3f} В, "
                  f"установлено число: {number}")

if __name__ == "__main__":
    try:
        dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183, True)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")

    finally:
        dac.deinit()
