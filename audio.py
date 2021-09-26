import numpy as np
import math
import pygame, pygame.sndarray

import calculations

pygame.mixer.init(channels=1)

sample_rate = 44100
volume = 4096
duration = 1
double_mixer = True

def sine_wave(hz, peak, n_samples=sample_rate):
    length = sample_rate / float(hz)
    omega = np.pi * 2 / length
    xvalues = np.arange(int(length)) * omega
    onecycle = peak * np.sin(xvalues)
    return np.resize(onecycle, (n_samples,)).astype(np.int16)

def calculate_waveform(intensities, envelope, note):
    pitch = 261.6*math.pow(2, note/12)
    waveform = sine_wave(pitch, volume * intensities[0])
    for i in range(1,len(intensities)):
        waveform = np.add(waveform, sine_wave(pitch * (i+1), volume * intensities[i]))
    waveform = np.array([int(envelope(i/len(waveform)) * waveform[i]) for i in range(len(waveform))])
    return waveform
def calculate_waveform_from_vec(v, note):
    intensities, envelope = calculations.calculate_intensities(v)
    waveform = calculate_waveform(intensities, envelope, note)
    if double_mixer: waveform = np.array([(a,a) for a in waveform])
    #else:
    waveform = np.array([np.int32(a) for a in waveform])
    return waveform

def calculate_sound(waveform):
    sound = pygame.sndarray.make_sound(waveform)
    return sound