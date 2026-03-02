import time
import adc_plot

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time
        
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

try:
    adc = R2R_ADC(3.290, compare_time=0.0001, verbose=False)

    voltage_values = []
    time_values = []
    duration = 3.0

    start_time = time.time()

    while time.time() - start_time < duration:
        voltage_values.append(adc.get_sc_voltage())
        time_values.append(time.time() - start_time)

    adc_plot.plot_voltage_vs_time(time_values, voltage_values, 3.3)

finally:
    adc.deinit()
