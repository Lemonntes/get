import numpy as np
import time

def get_sin_wave_amplitude(freq,time):
    phase = 2 *3.14 * freq * time
    res = (np.sin(phase) + 1) / 2
    return res

def wait_For_sampling_period(sampling_frequency):
    time.sleep(1/sampling_frequency)
