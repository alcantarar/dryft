from dryft import step, aerial, signal
import pandas as pd
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt

GRF = pd.read_csv('drifting_forces.txt', header=None)
Fs = 600
Fc = 60
Fn = (Fs / 2)
b,a = butter(2, Fc/Fn)
GRF_filt = filtfilt(b, a, GRF, axis=0)  # filtfilt doubles order (2nd*2 = 4th order effect)

step_begin, step_end = step.split(vGRF = GRF_filt[:,2],threshold = 110, Fs = 300, min_tc = 0.2, max_tc = 0.4, plot=False)

aerial_begin_all = step_end[:-1]
aerial_end_all = step_begin[1:]
print('Number of aerial begin/end:', aerial_begin_all.shape[0], aerial_end_all.shape[0])

# step.plot(GRF_filt[:,2], step_begin, step_end)

# trim filtering artefact and calculate mean of each aerial phase
trim = aerial.trim(GRF_filt[:,2], step_begin, step_end)
aerial_means = aerial.calc_aerial_force(GRF_filt[:,2], step_begin, step_end, trim ) #aerial_means will be same width as GRF_filt
# one of the aerial phases is apparently 3000 frames long and messing it all up.
aerial.plot(GRF_filt[:,2], aerial_means, aerial_begin_all, aerial_end_all, trim) #aerial_means and GRF_filt must be (n,) arrays

# Detrend signal
force_fd, aerial_means_d = signal.detrend(GRF_filt[:,2], Fs, aerial_means, step_begin, step_end, trim, plot=True) #grf_filt and aerial_means must be same width
