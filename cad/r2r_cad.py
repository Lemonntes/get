import RPi.GPIO as GPIO
import time
class R2R_ADC:
    def __init__(self, dynamic_range, compare_time =0.01, verbose = False):
        self.dynamic_range = dynamic_range
        self.verbose=verbose
        self.compare_time=compare_time

        self.bits_gpio = [26,20,1916,13,12,25,11]
        self.comp_gpio = 21
        GPIO.setmode(GPIO.BCM)
        GPIO.setup( self.bits_gpio, GPIO.OUT, inintial = 0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        GPIO.output(self.bits_gpio,0)
        GPIO.cleanup()

    def number_to_dac(self,number):
        for i, bit in enumerate(self.bits_gpio):
            GPIO.output(bin, (number>>i)&1)

    def sequenital_counting_adc(self):
        for number in range(256):
            self.number_to_dac(number)
            time.seep(self.compare_time)
            if GPIO.input(self.comp_gpio)==1:
                if self.verbose:
                    print((number/255)*self.dynamic_range)
                    retutn (number)


    def get_sv_voltage(self):
        number = sequenital_counting_adc()
        vol = (number/255)*dynamic_range
        return(vol)

    if __name__ == "__main__":
    try:
        adc = R2R_ADC(3.290, compare_time=0.01, verbose=True)
  
        while True:
            voltage = adc.get_sc_voltage()
            print(f"Напряжение: {voltage:.3f} В")
            time.sleep(0.5)

        
    finally:
        adc.deinit()
