import csv
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np

samplerate, data = wavfile.read('random/soun2d.wav')
print(data.shape[0])
print("number of channels = ",data.shape[1])
length=data.shape[0]/samplerate;
print("length =", length)

time = np.linspace(0., length, data.shape[0])
plt.plot(time, data[:, 0], label="Left channel")
plt.plot(time, data[:, 1], label="Right channel")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()
        

        
fout = open('output.csv', 'w')
wrt = csv.writer(fout)
wrt.writerow(data)
fout.close()