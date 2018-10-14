#Skyler Szot
#convert mp3 to wav

from pydub import AudioSegment
from scipy import signal as sig
import numpy as np
import wave
import sys
from scipy.signal import butter, lfilter, freqz
import subprocess
import os

#Lowpass Filter Design

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

#Process signal

def processSignal(filePath, speed): #speed 1 = slow, 2 = med, 3 = fast
	folder = os.path.dirname(filePath)
	temp = subprocess.check_output(['ffmpeg','-loglevel','panic', '-y', '-i', filePath, '/tmp/analysis.mp3'])
	sound = AudioSegment.from_mp3(folder+"/tmp/analysis.mp3")
	sound.export(folder+'/tmp/analysis.wav', format="wav")

	spf = wave.open(folder + '/tmp/analysis.wav','r')
	fsamp = spf.getframerate()

	lower = 0
	upper = 0

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

	#downsample ratio
	ratio = 10
	downsamp = signal[::ratio]
	fsamp = fsamp/ratio

	# Filter requirements.
	order = 6
	fs = fsamp    # sample rate, Hz
	cutoff = 140  # desired cutoff frequency of the filter, Hz

	# Demonstrate the use of the filter.
	T = len(downsamp)/fs         # seconds
	n = len(downsamp) # total number of samples
	t = np.linspace(0, T, n, endpoint=False)

	data = downsamp

	# Filter the data, and plot both the original and filtered signals.

	y = butter_lowpass_filter(data, cutoff, fs, order)

	window = int(len(y)/fsamp/5)

	m = 0
	total = [0]*(int(len(y)/fsamp/window))

	for m in range(int(len(y)/fsamp/window)):
		h = y[int(fsamp*window*m):int(fsamp*window*(m+1))]

		f, Pxx_den = sig.periodogram(h, fs)
		i = 0
		maxfreq = 0
		maxi = 0
		while(f[i]<lower):
			i+=1
		while(f[i]<upper):
			if (Pxx_den[i] > Pxx_den[maxi]):
				maxi = i
			i+=1
		bpm = f[maxi]*60
		total[m] = bpm
	total.remove(min(total))
	total.remove(max(total))
	return(np.average(total), np.std(total))

if __name__ == '__main__':
	print(processSignal("/home/osboxes/Sound-Repo-Thing/like.mp4", 2))
		
