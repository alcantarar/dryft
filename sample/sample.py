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

# Identify where aerial phase occurs (feet not on ground)
#Use aerial phase after first step to the aerial phase before the last whole step.
# This method guarantees aerial phases per signal.splitsteps()
aerial_begin_all = step_end[:-1]
aerial_end_all = step_begin[1:]
print('Number of aerial begin/end:', aerial_begin_all.shape[0], aerial_end_all.shape[0])

# Determine average force signal during aerial phase
# Must trim beginning and end of aerial phase to get true aerial phase value
trim = signal.trimaerial(GRF_filt[:,2], step_begin, step_end)
aerial_means, aerial_means_loc = signal.meanaerialforce(GRF_filt[:,2], step_begin, step_end, trim ) #aerial_means will be same width as GRF_filt
# plot.aerial(GRF_filt[:,2], aerial_means, aerial_means_loc, aerial_begin_all, aerial_end_all, trim) #aerial_means and GRF_filt must be (n,) arrays

# Detrend signal
force_fd = signal.detrend(GRF_filt[:,2], aerial_means, aerial_means_loc)


# compare detrended signal to original
step_begin_d, step_end_d = signal.splitsteps(vGRF=force_fd,
                                             threshold=10,
                                             Fs=300,
                                             min_tc=0.2,
                                             max_tc=0.4,
                                             plot=False)
trim_d = signal.trimaerial(force_fd, step_begin_d, step_end_d)
aerial_means_d, aerial_means_loc = signal.meanaerialforce(force_fd, step_begin_d, step_end_d, trim_d)

# plot original vs detrended signal
plt.detrendp, (sigcomp, meancomp) = plt.subplots(2, 1, figsize=(15, 7))
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
meancomp.set_title('mean of aerial phases')
meancomp.set_xlabel('step')
meancomp.set_ylabel('force (N)')
meancomp.grid()
for i in range(aerial_means.shape[0]):
    meancomp.plot(i, aerial_means[i],
                  marker='.',
                  color='tab:blue',
                  label='original signal')
    meancomp.plot(i, aerial_means_d[i],
                  marker='.',
                  color='tab:red',
                  label='detrended signal')
    meancomp.legend(['original signal', 'detrended signal'], loc=1)  # don't want it in loop, but it needs it?
plt.tight_layout()
plt.show(block=True)


# Can be applied again to further reduce drift
# force_fdd, aerial_means_dd = signal.detrend(force_fd, Fs, aerial_means_d, step_begin, step_end, trim, plot = True)