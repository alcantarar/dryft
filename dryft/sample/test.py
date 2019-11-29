"""
Test script for `dryft` package.

Licensed under an MIT License (c) Ryan Alcantara 2019

Distributed here: https://github.com/alcantarar/dryft
"""
from dryft import signal, plot
import pandas as pd
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
# Read in data from force plate
GRF = pd.read_csv(Path(__file__).parent /
                  'custom_drift_S001runT25.csv', header=None)

# Apply Butterworth Filter
Fs = 300
Fc = 50
Fn = (Fs / 2)
n_pass = 2  # filtfilt is dual pass
order = 2  # filtfilt doubles effective order (resulting order = 2*order)
# Correction factor per Research Methods in Biomechanics (2e) pg 288
C = (2**(1/n_pass) - 1)**(1/(2*order))
Wn = (np.tan(np.pi*Fc/Fs))/C  # Apply correction to adjusted cutoff freq
Fc_corrected = np.arctan(Wn)*Fs/np.pi  # Hz
b, a = butter(order, Fc_corrected/Fn)
# filtfilt doubles order (2nd*2 = 4th order effect)
GRF_filt = filtfilt(b, a, GRF, axis=0)

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

# Determine force signal at middle of aerial phase (feet not on ground)
aerial_vals, aerial_loc = signal.aerialforce(
    GRF_filt, stance_begin_all, stance_end_all, good_stances)

# Plot all aerial phases to see what is being subtracted from signal in signal.detrend()
plot.aerial(GRF_filt, aerial_vals, aerial_loc,
            stance_begin_all, stance_end_all, good_stances)

# Detrend signal
force_fd = signal.detrend(GRF_filt, aerial_vals, aerial_loc)

# Compare corrected signal to original
stance_begin_all_d, stance_end_all_d, good_stances_d = signal.splitsteps(vGRF=force_fd,
                                                                         threshold=25,
                                                                         Fs=300,
                                                                         min_tc=0.2,
                                                                         max_tc=0.4,
                                                                         plot=False)
stance_begin_d = stance_begin_all_d[good_stances_d]
stance_end_d = stance_end_all_d[good_stances_d]

aerial_vals_d, aerial_loc_d = signal.aerialforce(
    force_fd, stance_begin_all_d, stance_end_all_d, good_stances_d)

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
plt1.grid(zorder=0)
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
            label='Original Signal', zorder=2)
plt.scatter(aerial_loc_d,
            aerial_vals_d,
            marker='o',
            color='tab:blue',
            label='Corrected Signal', zorder=2)

plt2.legend(loc=2)
plt.tight_layout()
plt2.grid(zorder=0)
plt.show(block=True)

print('dryft test complete')
