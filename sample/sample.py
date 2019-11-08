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
step_begin, step_end = signal.splitsteps(vGRF=GRF_filt[:,2],
                                  threshold=110,
                                  Fs=300,
                                  min_tc=0.2,
                                  max_tc=0.4,
                                  plot=False)
# plot.stance(GRF_filt[:,2], step_begin, step_end)

# Determine force signal at middle of aerial phase (feet not on ground)
aerial_vals, aerial_loc = signal.aerialforce(GRF_filt[:,2], step_begin, step_end) #aerial_vals will be same width as GRF_filt
plot.aerial(GRF_filt[:,2], aerial_vals, aerial_loc, step_begin, step_end) #aerial_vals and GRF_filt must be (n,) arrays

# Detrend signal
force_fd = signal.detrend(GRF_filt[:,2], aerial_vals, aerial_loc)


# compare detrended signal to original
step_begin_d, step_end_d = signal.splitsteps(vGRF=force_fd,
                                             threshold=10,
                                             Fs=300,
                                             min_tc=0.2,
                                             max_tc=0.4,
                                             plot=False)
aerial_vals_d, aerial_loc_d = signal.aerialforce(force_fd, step_begin_d, step_end_d)

# plot original vs detrended signal
plt.detrendp, (plt1, plt2) = plt.subplots(2, 1, figsize=(15, 7))
plt1.plot(np.linspace(0, force_fd.shape[0] / Fs, force_fd.shape[0]),
             GRF_filt[:,2],
             color='tab:blue',
             alpha=0.75)  # converted to sec
plt1.plot(np.linspace(0, force_fd.shape[0] / Fs, force_fd.shape[0]),
             force_fd,
             color='tab:red',
             alpha=0.75)  # converted to sec
plt1.grid()
plt1.legend(['original signal', 'detrended signal'], loc=1)
plt1.set_xlabel('Seconds')
plt1.set_ylabel('force (N)')

# plot detrend vs original aerial phases
plt2.set_title('Aerial Phases')
plt2.set_xlabel('step')
plt2.set_ylabel('force (N)')
plt2.grid()
for i in range(aerial_vals.shape[0]):
    plt2.plot(i, aerial_vals[i],
                  marker='.',
                  color='tab:blue',
                  label='original signal')
    plt2.plot(i, aerial_vals_d[i],
                  marker='.',
                  color='tab:red',
                  label='detrended signal')
    plt2.legend(['original signal', 'detrended signal'], loc=1)  # don't want it in loop, but it needs it?
plt.tight_layout()
plt.show(block=True)


# Can be applied again to further reduce drift
# force_fdd, aerial_vals_dd = signal.detrend(force_fd, aerial_vals_d, aerial_loc_d)
