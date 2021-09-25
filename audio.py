import numpy as np
import math
import pygame, pygame.sndarray

import calculations

pygame.mixer.init(channels=1)

sample_rate = 44100
volume = 4096
duration = 1

def play_for(sample_wave, ms):
    """Play the given NumPy array, as a sound, for ms milliseconds."""
    sound = pygame.sndarray.make_sound(np.array([(a,a) for a in sample_wave]))
    sound.play(-1)
    pygame.time.delay(ms)
    sound.stop()

def sine_wave(hz, peak, n_samples=sample_rate):
    """Compute N samples of a sine wave with given frequency and peak amplitude.
       Defaults to one second.
    """
    length = sample_rate / float(hz)
    omega = np.pi * 2 / length
    xvalues = np.arange(int(length)) * omega
    onecycle = peak * np.sin(xvalues)
    return np.resize(onecycle, (n_samples,)).astype(np.int16)

def waveform(intensities, note):
    pitch = 261.6*math.pow(2, note/12)
    waveform = sine_wave(pitch, volume)
    for i in range(len(intensities)):
        waveform = np.add(waveform, sine_wave(pitch * (i+2), volume * intensities[i]))
    print(waveform)
    return waveform
    	
play_for(waveform(calculations.overtones_from_vec([0.5,0.5,0.9,0.5,0.5]), 0),int(1000*duration))
#play_pitches([0,4,7,12],1)
#play_pitches([11,14,7,19],1)
#play_pitches([1,2,3,4,5,6,7],1)