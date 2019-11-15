from dryft import signal, plot
import pandas as pd
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
import numpy as np

# Read in data from force plate
# GRF = pd.read_csv('drifting_forces.txt', header=None)
GRF = pd.read_csv('../MATLAB/custom_drift_S001runT25.csv', header = None)

# slice_bad = np.asarray(GRF_bad)[:,]
# slice_try = slice_bad.flatten()

# Apply Butterworth Filter
Fs = 300
Fc = 50
Fn = (Fs / 2)
b,a = butter(2, Fc/Fn)
GRF_filt = filtfilt(b, a, GRF, axis=0)  # filtfilt doubles order (2nd*2 = 4th order effect)
# GRF_filt = GRF_filt[:,2] # just vertical for 'drifting_forces.txt'

# Identify where stance phase occurs (foot on ground)
stance_begin_all, stance_end_all, good_stances = signal.splitsteps(vGRF=GRF_filt,
                                                          threshold=140,
                                                          Fs=300,
                                                          min_tc=0.2,
                                                          max_tc=0.4,
                                                          plot=True)
stance_begin = stance_begin_all[good_stances]
stance_end = stance_end_all[good_stances]
# plot.stance(GRF_filt, stance_begin, stance_end)
# *stance_begin and stance_end can be used to detrend other columns of GRF_filt as well*

# Determine force signal at middle of aerial phase (feet not on ground)
aerial_vals, aerial_loc = signal.aerialforce(GRF_filt, stance_begin_all, stance_end_all, good_stances)

# Plot all aerial phases to see what is being subtracted from signal in signal.detrend()
plot.aerial(GRF_filt, aerial_vals, aerial_loc, stance_begin_all, stance_end_all, good_stances)

# Detrend signal
force_fd = signal.detrend(GRF_filt, aerial_vals, aerial_loc)

# Compare corrected signal to original
stance_begin_all_d, stance_end_all_d, good_stances_d = signal.splitsteps(vGRF=force_fd,
                                                          threshold=25,
                                                          Fs=300,
                                                          min_tc=0.15,
                                                          max_tc=0.4,
                                                          plot=False)
stance_begin_d = stance_begin_all_d[good_stances_d]
stance_end_d = stance_end_all_d[good_stances_d]

aerial_vals_d, aerial_loc_d = signal.aerialforce(force_fd, stance_begin_all_d, stance_end_all_d, good_stances_d)

# Plot waveforms (original vs corrected)
plt.detrendp, (plt1, plt2) = plt.subplots(2, 1, figsize=(15, 7))
plt1.plot(np.linspace(0, force_fd.shape[0] / Fs, force_fd.shape[0]),
          GRF_filt,
          color='tab:red',
          alpha=0.75,
          label='Original Signal')  # converted to sec
plt1.plot(np.linspace(0, force_fd.shape[0] / Fs, force_fd.shape[0]),
          force_fd,
          color='tab:blue',
          alpha=0.75,
          label='Corrected Signal')  # converted to sec
plt1.grid(zorder =0)
plt1.legend(loc=2)
plt1.set_xlabel('Seconds')
plt1.set_ylabel('Force (N)')

# Plot aerial phases (original vs corrected)
plt2.set_title('Aerial Phases')
plt2.set_xlabel('Frames')
plt2.set_ylabel('Force (N)')
plt.scatter(aerial_loc,
            aerial_vals,
            marker='o',
            color='tab:red',
            label='Original Signal', zorder = 2)
plt.scatter(aerial_loc_d,
            aerial_vals_d,
            marker='o',
            color='tab:blue',
            label='Corrected Signal', zorder = 2)

plt2.legend(loc=2)
plt.tight_layout()
plt2.grid(zorder = 0)
plt.show(block=True)
