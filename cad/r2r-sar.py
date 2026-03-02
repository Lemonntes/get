from r2r_adc import R2R_ADC
import time
import matplotlib.pyplot as plt

adc = R2R_ADC(3.18)

voltage_values = []
time_values = []
duration = 3.0

try:
    start_time = time.time()
    while time.time() - start_time < duration:
        voltage_values.append(adc.get_sar_voltage())
        time_values.append(time.time() - start_time)
    
    plt.figure(figsize=(10,6))
    plt.plot(time_values, voltage_values)
    plt.title('Зависимость напряжения от времени (АЦП последовательного приближения)')
    plt.xlabel('Время (с)')
    plt.ylabel('Напряжение (В)')
    plt.xlim(0, max(time_values))
    plt.ylim(0, 3.3)
    plt.grid(True)
    plt.show()
finally:
    adc.deinit()
