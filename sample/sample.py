from dryft import signal, plot
import pandas as pd
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
import numpy as np

# Read in data from force plate
GRF = pd.read_csv('drifting_forces.txt', header=None)

# Apply Butterworth Filter
Fs = 300
Fc = 60
Fn = (Fs / 2)
b,a = butter(2, Fc/Fn)
GRF_filt = filtfilt(b, a, GRF, axis=0)  # filtfilt doubles order (2nd*2 = 4th order effect)

# Identify where stance phase occurs (foot on ground)
stance_begin, stance_end = signal.splitsteps(vGRF=GRF_filt[:,2],
                                  threshold=110,
                                  Fs=300,
                                  min_tc=0.2,
                                  max_tc=0.4,
                                  plot=False)
# plot.stance(GRF_filt[:,2], stance_begin, stance_end)
# *stance_begin and stance_end can be used to detrend other columns of GRF_filt as well*

# Determine force signal at middle of aerial phase (feet not on ground)
aerial_vals, aerial_loc = signal.aerialforce(GRF_filt[:,2], stance_begin, stance_end)

# Plot all aerial phases to see what is being subtracted from signal in signal.detrend()
plot.aerial(GRF_filt[:,2], aerial_vals, aerial_loc, stance_begin, stance_end)

# Detrend signal
force_fd = signal.detrend(GRF_filt[:,2], aerial_vals, aerial_loc)

# Compare detrended signal to original
stance_begin_d, stance_end_d = signal.splitsteps(vGRF=force_fd,
                                             threshold=10,
                                             Fs=300,
                                             min_tc=0.2,
                                             max_tc=0.4,
                                             plot=False)
aerial_vals_d, aerial_loc_d = signal.aerialforce(force_fd, stance_begin_d, stance_end_d)

# Plot waveforms (original vs detrended)
plt.detrendp, (plt1, plt2) = plt.subplots(2, 1, figsize=(15, 7))
plt1.plot(np.linspace(0, force_fd.shape[0] / Fs, force_fd.shape[0]),
             GRF_filt[:,2],
             color='tab:blue',
             alpha=0.75)  # converted to sec
plt1.plot(np.linspace(0, force_fd.shape[0] / Fs, force_fd.shape[0]),
             force_fd,
             color='tab:red',
             alpha=0.75)  # converted to sec
plt1.grid(zorder =0)
plt1.legend(['original signal', 'detrended signal'], loc=1)
plt1.set_xlabel('Seconds')
plt1.set_ylabel('force (N)')

# Plot aerial phases (original vs detrended)
plt2.set_title('Aerial Phases')
plt2.set_xlabel('Step')
plt2.set_ylabel('force (N)')
plt.scatter(np.arange(aerial_vals_d.shape[0]),
         aerial_vals_d,
         marker='o',
         color='tab:red',
         label='detredned signal', zorder = 2)
plt.scatter(np.arange(aerial_vals.shape[0]), #REMOVE LINES
         aerial_vals,
         marker='o',
         color='tab:blue',
         label='original signal', zorder = 2)

plt2.legend(['original signal', 'detrended signal'], loc=1)  # don't want it in loop, but it needs it?
plt.tight_layout()
plt2.grid(zorder = 0)
plt.show(block=True)
