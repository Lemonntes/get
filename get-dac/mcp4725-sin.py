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
