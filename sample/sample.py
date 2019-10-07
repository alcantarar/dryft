import dryft as dr
import pandas as pd
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
# Read in data from force plate
GRF = pd.read_csv('sample/drifting_forces.txt', header=None)

# Apply Butterworth Filter
Fs = 600
Fc = 60
Fn = (Fs / 2)
b,a = butter(2, Fc/Fn)
GRF_filt = filtfilt(b, a, GRF, axis=0)  # filtfilt doubles order (2nd*2 = 4th order effect)

# Identify where stance phase occurs (foot on ground)
step_begin, step_end = dr.s (vGRF=GRF_filt[:,2],
                                  threshold=110,
                                  Fs=300,
                                  min_tc=0.2,
                                  max_tc=0.4,
                                  plot=False)
# step.plot(GRF_filt[:,2], step_begin, step_end)

# Identify where aerial phase occurs (feet not on ground)
aerial_begin_all = step_end[:-1]
aerial_end_all = step_begin[1:]
print('Number of aerial begin/end:', aerial_begin_all.shape[0], aerial_end_all.shape[0])

# Determine average force signal during aerial phase
# Must trim beginning and end of aerial phase to get true aerial phase value
trim = aerial.trim(GRF_filt[:,2], step_begin, step_end)
aerial_means = aerial.calc_aerial_force(GRF_filt[:,2], step_begin, step_end, trim ) #aerial_means will be same width as GRF_filt
aerial.plot(GRF_filt[:,2], aerial_means, aerial_begin_all, aerial_end_all, trim) #aerial_means and GRF_filt must be (n,) arrays

# Detrend signal
force_fd, aerial_means_d = signal.detrend(GRF_filt[:,2],
                                          Fs,
                                          aerial_means,
                                          step_begin,
                                          step_end,
                                          trim,
                                          plot=True) #grf_filt and aerial_means must be same width
