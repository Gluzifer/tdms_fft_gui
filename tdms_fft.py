import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq, ifft
from nptdms import TdmsFile


def tdms_fft(tdms_file, group_name, channel_name, sr, data_start, data_end):
    plt.style.use('seaborn-poster')

    # t = []
    x = []

    # tdms_file = TdmsFile.read(filepath)
    group = tdms_file[group_name]
    channel = group[channel_name]
    channel_data = channel[:]
    channel_properties = channel.properties

    # Assign data to variable used in fft
    x = channel_data[data_start:data_end]

    # sampling rate
    # resolution is 0.1 sec, thus sampling rate is 1/0.1 = 100
    # sr = 200000

    X = fft(x)
    N = len(X)
    # freq = n/T
    freq = fftfreq(N, 1 / sr)

    plt.figure(figsize = (12, 6))

    half_length = int(len(X) / 2) # len(X) will due to symmetry always be odd

    # Plot while excluding the negative frequencies
    plt.stem(freq[0:half_length], np.abs(X)[0:half_length], 'b', markerfmt=" ", basefmt="-b")
    plt.xlabel('Freq (Hz)')
    plt.ylabel('FFT Amplitude |X(freq)|')
    # plt.xlim(0, 100000)
    # Set yscale according to maximum excluding the constant term
    plt.ylim(0, max(np.abs(X)[1:]))
    plt.tight_layout()
    plt.show()


# tdms_fft("../Logged Data_2021_08_11_16_23_35.tdms", 'Untitled', 'Dev1/ai0', 200000)
