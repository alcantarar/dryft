import dryft.process as dp
import pandas as pd
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt

GRF = pd.read_csv('drifting_forces.txt', header=None)
Fs = 600
Fc = 60
Fn = (Fs / 2)
b, a = butter(2, Fc/Fn)
GRF_filt = filtfilt(b, a, GRF, axis=0)  # filtfilt doubles order (2nd*2 = 4th order effect)

step_begin, step_end = dp.stepid(vGRF = GRF_filt[:,2],threshold = 50, Fs = 300, min_tc = 0.2, max_tc = 0.4)

aerial_begin_all = step_end[:-1]
aerial_end_all = step_begin[1:]
print('Number of aerial begin/end:', aerial_begin_all.shape[0], aerial_end_all.shape[0])

# dp.plotsteps(GRF_filt[:,2], step_begin, step_end)

# trim filtering artefact and calculate mean of each aerial phase
trim = dp.trim_aerial_phases(GRF_filt[:,2], step_begin, step_end)

