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
aerial_medians, aerial_medians_loc = signal.aerialforce(GRF_filt[:,2], step_begin, step_end) #aerial_medians will be same width as GRF_filt
plot.aerial(GRF_filt[:,2], aerial_medians, aerial_medians_loc, aerial_begin_all, aerial_end_all) #aerial_medians and GRF_filt must be (n,) arrays

# Detrend signal
force_fd = signal.detrend(GRF_filt[:,2], aerial_medians, aerial_medians_loc)


# compare detrended signal to original
step_begin_d, step_end_d = signal.splitsteps(vGRF=force_fd,
                                             threshold=10,
                                             Fs=300,
                                             min_tc=0.2,
                                             max_tc=0.4,
                                             plot=False)
aerial_medians_d, aerial_medians_loc_d = signal.aerialforce(force_fd, step_begin_d, step_end_d)

# plot original vs detrended signal
plt.detrendp, (sigcomp, mediancomp) = plt.subplots(2, 1, figsize=(15, 7))
sigcomp.plot(np.linspace(0, force_fd.shape[0] / Fs, force_fd.shape[0]),
             GRF_filt[:,2],
             color='tab:blue',
             alpha=0.75)  # converted to sec
sigcomp.plot(np.linspace(0, force_fd.shape[0] / Fs, force_fd.shape[0]),
             force_fd,
             color='tab:red',
             alpha=0.75)  # converted to sec
sigcomp.grid()
sigcomp.legend(['original signal', 'detrended signal'], loc=1)
sigcomp.set_xlabel('Seconds')
sigcomp.set_ylabel('force (N)')

# plot detrend vs original aerial phases
mediancomp.set_title('median of aerial phases')
mediancomp.set_xlabel('step')
mediancomp.set_ylabel('force (N)')
mediancomp.grid()
for i in range(aerial_medians.shape[0]):
    mediancomp.plot(i, aerial_medians[i],
                  marker='.',
                  color='tab:blue',
                  label='original signal')
    mediancomp.plot(i, aerial_medians_d[i],
                  marker='.',
                  color='tab:red',
                  label='detrended signal')
    mediancomp.legend(['original signal', 'detrended signal'], loc=1)  # don't want it in loop, but it needs it?
plt.tight_layout()
plt.show(block=True)


# Can be applied again to further reduce drift
# force_fdd, aerial_medians_dd = signal.detrend(force_fd, aerial_medians_d, aerial_medians_loc_d)
