import numpy as np
import math
import pygame, pygame.sndarray
import matplotlib.pyplot as plt

import calculations

pygame.mixer.init(channels=1)

sample_rate = 44100
volume = 4096
duration = 1
double_mixer = False

def sine_wave(hz, peak, n_samples=sample_rate):
    """Compute N samples of a sine wave with given frequency and peak amplitude.
       Defaults to one second.
    """
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
    #waveform = (waveform*volume)//max(abs(waveform))
    waveform = np.array([int(envelope(i/len(waveform)) * waveform[i]) for i in range(len(waveform))])
    return waveform

#def play_for(sample_wave, ms):
#    """Play the given NumPy array, as a sound, for ms milliseconds."""
#    sound = pygame.sndarray.make_sound(np.array([(a,a) for a in sample_wave]))
#    sound.play(-1)
#    pygame.time.delay(ms)
#    sound.stop()

def calculate_sound(v, note):
    intensities, envelope = calculations.calculate_intensities(v)
    waveform = calculate_waveform(intensities, envelope, note)
    #if double_mixer: waveform = np.array([(a,a) for a in waveform])
    #else:
    waveform = np.array([np.int32(a) for a in waveform])
    sound = pygame.sndarray.make_sound(waveform)
    return sound
    
    	
if __name__ == "__main__":
    i,e = list(calculations.calculate_intensities([0.4,1,1,0]))
    print(i)
    #i = [1, 0,0.5,0,0.05,0,0.2,0.4,0.43,0.48,0,0.1,0.05] # clarinet
    #print(i)
    #i = [1, 0.5, 0.2, 0.21, 0.07] #0.41] # 0.07, 0.3, 0.1, 0.1, 0.03, 0.04, 0.04] #piano?
    #i = [1, 0.4, 0.15, 0.1, 0.1, 0.05] # violin?
    #i = [1/j for j in range(1,6)]
    # a = 0.001
    # def e(x): 
    #     if x < a: return x/a
    #     return (1-x)/(1-a)
    w = calculate_waveform(i, e, 0)
    print(w)
    #sound = pygame.sndarray.make_sound(np.array([(a,a) for a in w]))
    asdfasdf = np.array([np.int32(a) for a in w])
    print(type(asdfasdf[100]))
    print('a')
    sound = pygame.sndarray.make_sound(asdfasdf)
    print('b')
    sound.play(-1)
    _, axs = plt.subplots(2)
    axs[0].plot(w)
    axs[1].bar(range(len(i)), i)
    plt.show()
