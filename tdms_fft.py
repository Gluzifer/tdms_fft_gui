import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq, ifft
from nptdms import TdmsFile
import csv


def convert_to_csv(tdms_file, group_name, channel_name, sr, data_start, data_end, filename, include_time_axis=True):
    t = []
    x = []

    # tdms_file = TdmsFile.read(filepath)
    group = tdms_file[group_name]
    channel = group[channel_name]
    channel_data = channel[:]

    # Assign data to variable
    x = channel_data[data_start:data_end]

    # Create nparray with the desired data
    if include_time_axis:
        # Generate time variable list
        for i in range(len(x)):
            t.append(i * 1/sr)
        data_to_write = np.array([t, x]).transpose()
    else:
        data_to_write = np.array(x).transpose()

    # Write the data into a csv

    # writing to csv file 
    out_filename = filename[:-4] + "csv"
    fields = ["Time since start of data in seconds", "Signal Amplitude"]
    with open(out_filename, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(fields)
        # writing the data rows
        csvwriter.writerows(data_to_write)

    # np.savetxt(out_filename, data_to_write, delimiter=",")


def tdms_fft(tdms_file, group_name, channel_name, sr, data_start, data_end, plot_type='stem', plot_linewidth=1, plot_linealpha=1):
    plt.style.use('seaborn-poster')

    # t = []
    x = []

    # tdms_file = TdmsFile.read(filepath)
    group = tdms_file[group_name]
    channel = group[channel_name]
    channel_data = channel[:]
    # channel_properties = channel.properties

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
    if plot_type == 'stem':
        markerline, stemlines, baseline = plt.stem(freq[0:half_length], np.abs(X)[0:half_length], 'b', markerfmt=" ", basefmt=" ")
        plt.setp(stemlines, 'linewidth', plot_linewidth)
        plt.setp(stemlines, 'alpha', plot_linealpha)
    elif plot_type == 'line':
        plt.plot(freq[0:half_length], np.abs(X)[0:half_length], linewidth=plot_linewidth, alpha=plot_linealpha)
    elif plot_type == 'step':
        plt.step(freq[0:half_length], np.abs(X)[0:half_length], linewidth=plot_linewidth, alpha=plot_linealpha)

    plt.xlabel('Freq (Hz)')
    plt.ylabel('FFT Amplitude')
    # plt.xlim(0, 100000)
    # Set yscale according to maximum excluding the constant term
    plt.ylim(0, max(np.abs(X)[1:]))
    plt.tight_layout()
    plt.show()


# tdms_fft("../Logged Data_2021_08_11_16_23_35.tdms", 'Untitled', 'Dev1/ai0', 200000)
