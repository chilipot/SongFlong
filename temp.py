#Skyler Szot
#convert mp3 to wav

import scipy
#wav convert imports
from pydub import AudioSegment

#downsample import
from scipy import signal as sig

#plot imports
import matplotlib.pyplot as plt
import numpy as np
import wave
import sys

#filter imports
import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt

#sound = AudioSegment.from_mp3("/home/osboxes/Sound-Repo-Thing/Avicii.mp3") #126
#sound = AudioSegment.from_mp3("/home/osboxes/Sound-Repo-Thing/redhot.mp3") #96
#sound = AudioSegment.from_mp3("/home/osboxes/Sound-Repo-Thing/scorpin.mp3") #126
#sound = AudioSegment.from_mp3("/home/osboxes/Sound-Repo-Thing/america.mp3") #120
#sound = AudioSegment.from_mp3("/home/osboxes/Sound-Repo-Thing/god.mp3") #77
#sound = AudioSegment.from_mp3("/home/osboxes/Sound-Repo-Thing/hotel.mp3") #147
#sound = AudioSegment.from_mp3("/home/osboxes/Sound-Repo-Thing/kiki.mp3") #91
#sound = AudioSegment.from_mp3("/home/osboxes/Sound-Repo-Thing/sail.mp3") #119
#sound = AudioSegment.from_mp3("/home/osboxes/Sound-Repo-Thing/thrift.mp3") #95
#sound = AudioSegment.from_mp3("/home/osboxes/Sound-Repo-Thing/oneday.mp3") #145
sound = AudioSegment.from_mp3("/home/osboxes/Sound-Repo-Thing/allday.mp3") #139?

sound.export("/home/osboxes/Sound-Repo-Thing/file.wav", format="wav")

spf = wave.open('file.wav','r')
fsamp = spf.getframerate()
print("Original Sample Rate: ", fsamp)


lower = 0
upper = 0
speed = int(input("Enter relative speed slow = 1, medium = 2, fast = 3"))
if (speed == 1):
	lower = 1
	upper = 2
if (speed == 2):
	lower = 1.5
	upper = 2.5
if (speed == 3):
	lower = 2
	upper = 3

#Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.fromstring(signal, 'Int16')

print("Original Signal Length", len(signal))

#plot wav file
plt.figure(1)
plt.title('Original Signal Wave...')
plt.plot(signal)
#plt.show()

#downsample ratio
ratio = 10
downsamp = signal[::ratio]
fsamp = fsamp/ratio
print("downsampled freq: ", fsamp)
print("downsampled length: ", len(downsamp))

plt.figure(2)
plt.title('Downsampled Wave...')
plt.plot(downsamp)
#plt.show()

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
cutoff = 180  # desired cutoff frequency of the filter, Hz

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
#plt.show()

window = int(len(y)/fsamp/5)
#window = 30
m = 0
total = [0]*(int(len(y)/fsamp/window))

for m in range(int(len(y)/fsamp/window)):
	h = y[int(fsamp*window*m):int(fsamp*window*(m+1))]

	f, Pxx_den = sig.periodogram(h, fs)
	plt.semilogy(f, Pxx_den)
	plt.ylim([1e1, 1e7])
	plt.xlim([0, 10])
	plt.xlabel('frequency [Hz]')
	plt.ylabel('PSD [V**2/Hz]')
	#plt.show()

	#print(f)
	i = 0
	maxfreq = 0
	maxi = 0
	while(f[i]<lower):
		i+=1
	while(f[i]<upper):
		if (Pxx_den[i] > Pxx_den[maxi]):
			maxi = i
			#print(i)
		i+=1
	bpm = f[maxi]*60
	print("periodogram bpm: ", bpm, "Time: ", window*m, " to ", window*(m+1))
	total[m] = bpm
total.remove(min(total))
total.remove(max(total))
print(np.average(total))
print(np.std(total))
	
