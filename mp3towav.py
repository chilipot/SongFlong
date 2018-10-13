#Skyler Szot
#convert mp3 to wav

#wav convert imports
from pydub import AudioSegment

#downsample import
from scipy import signal

#plot imports
import matplotlib.pyplot as plt
import numpy as np
import wave
import sys

#filter imports
import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt

sound = AudioSegment.from_mp3("/home/osboxes/Sound-Repo-Thing/Avicii.mp3")
sound.export("/home/osboxes/Sound-Repo-Thing/file.wav", format="wav")

spf = wave.open('file.wav','r')
fsamp = spf.getframerate()
print("Original Sample Rate: ", fsamp)

#Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.fromstring(signal, 'Int16')

print("Original Signal Length", len(signal))

#plot wav file
plt.figure(1)
plt.title('Original Signal Wave...')
plt.plot(signal)
plt.show()

#downsample ratio
ratio = 10
downsamp = signal[::ratio]
fsamp = fsamp/ratio
print("downsampled freq: ", fsamp)
print("downsampled length: ", len(downsamp))

plt.figure(2)
plt.title('Downsampled Wave...')
plt.plot(downsamp)
plt.show()

import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt

#Lowpass Filter Design
import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


# Filter requirements.
order = 6
fs = fsamp    # sample rate, Hz
cutoff = 160/ratio  # desired cutoff frequency of the filter, Hz

# Get the filter coefficients so we can check its frequency response.
b, a = butter_lowpass(cutoff, fs, order)

# Plot the frequency response.
w, h = freqz(b, a, worN=8000)
plt.subplot(2, 1, 1)
plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
plt.axvline(cutoff, color='k')
plt.xlim(0, 0.01*fs)
plt.title("Lowpass Filter Frequency Response")
plt.xlabel('Frequency [Hz]')
plt.grid()


# Demonstrate the use of the filter.
# First make some data to be filtered.
T = len(downsamp)/fs         # seconds
n = len(downsamp) # total number of samples
t = np.linspace(0, T, n, endpoint=False)
# "Noisy" data.  We want to recover the 1.2 Hz signal from this.
#data = np.sin(1.2*2*np.pi*t) + 1.5*np.cos(9*2*np.pi*t) + 0.5*np.sin(12.0*2*np.pi*t)
data = downsamp

# Filter the data, and plot both the original and filtered signals.
y = butter_lowpass_filter(data, cutoff, fs, order)

plt.subplot(2, 1, 2)
plt.plot(t, data, 'b-', label='data')
plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.35)
plt.show()
