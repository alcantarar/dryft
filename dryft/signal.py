import numpy as np
import matplotlib.pyplot as plt

def detrend(force_f, Fs, aerial_means, step_begin, step_end, trim, plots=False):
    '''
    This function reads in a text file of 3D *running* ground reaction force data and removes drift in a stepwise manner.
    Author: Ryan Alcantara || ryan.alcantara@colorado.edu || github.com/alcantarar

    Parameters
    -------------
    filename :          filename of Nx3 array of 3D [horizontal,horizontal,vertical] force data to import via pd.read_csv.
    Fs :                Sampling frequency of force data.
    Fc :                Cut off frequency for 4th order zero-lag butterworth filter.
    min_step :          Minimum number of frames the step ID algorithm will consider 1 step. Default max_step is 0.4*Fs.
    step_threshold :    (optional) threshold in Newtons used to define heel-strike and toe-off. Default is 100N because
                        it is better to be aggressive for detrending. Can re-run Step_ID function with a reasonable 
                        step_threshold once signal is detrended.
    plots :             (optional) Logical input to receive graphs depicting detrend process.

    Returns
    -------------
    force_fd :          Nx3 array of filtered, detrended 3D force data 
    aerial_means :      Mean of force during aerial phase for original signal
    aerial_means_d :    Mean of force during aerial phase for detrended signal

    Raises
    -------------
    ValueError
        if imported file is not Nx3 dimensions. Requires 3D force data: [horizontal, horizontal, vertical].

    IndexError
        if aerial phase is exceptionally short. Happens when step identification is poor. Check plots and increase step_threshold or min_step 

    Examples
    -------------
     fname = '/Users/alcantarar/data/drifting_forces.csv'
     force_fd, aerial_means, aerial_means_d = detrend_force(fname, Fs=300, Fc=60, min_step=60) #step_threshold = 100N, no plots
    #OR
     force_fd,_,_ = detrend_force('drifting_forces.csv',300,60,60,100,True) #suppress aerial means outputs

    '''
    # force = readcheck_input(filename)
    # # filter 4th order zero lag butterworth
    # fn = (Fs / 2)
    # b, a = butter(2, Fc / fn)
    # force_f = filtfilt(b, a, force, axis=0)  # filtfilt doubles order (2nd*2 = 4th order effect)

    # %% split steps and create aerial phases
    # max_step = 0.4 * Fs
    # step_begin, step_end = step_ID(force_f, step_threshold, Fs, min_step, max_step)
    # 
    # # create aerial phases (foot not on ground) and trim artefacts from filtering
    # aerial_begin = step_end[:-1]
    # aerial_end = step_begin[1:]
    # print('Number of aerial begin/end:', aerial_begin.shape[0],
    #       aerial_end.shape[0])  # matching number of step beginnings/ends
    # 
    # if plots:
    #     plot_separated_steps(force_f, step_begin, step_end)
    #     plt.tight_layout()
    # 
    # # %% trim filtering artefact and calculate mean of each aerial phase
    # trim = trim_aerial_phases(force_f, step_begin, step_end)
    # 
    # # calculate mean force during aerial phase (foot not on ground, should be zero)
    # aerial_means = np.full([aerial_begin.shape[0] + 1, 3], np.nan)
    # # all but last step
    # i = 0
    # while i < min(step_begin.shape[0], step_end.shape[0]) - 1:
    #     aerial_means[i, 0] = np.mean(force_f[aerial_begin[i] + trim:aerial_end[i] - trim, 0])
    #     aerial_means[i, 1] = np.mean(force_f[aerial_begin[i] + trim:aerial_end[i] - trim, 1])
    #     aerial_means[i, 2] = np.mean(force_f[aerial_begin[i] + trim:aerial_end[i] - trim, 2])
    #     i = i + 1
    # # last step
    # aerial_means[i, 0] = np.mean(force_f[aerial_begin[i - 1] + trim:aerial_end[i - 1] - trim, 0])
    # aerial_means[i, 1] = np.mean(force_f[aerial_begin[i - 1] + trim:aerial_end[i - 1] - trim, 1])
    # aerial_means[i, 2] = np.mean(force_f[aerial_begin[i - 1] + trim:aerial_end[i - 1] - trim, 2])
    # 
    # # plot aerial phases
    # if plots:
    #     plot_aerial_phases(force_f, aerial_means, aerial_begin, aerial_end, trim)
    #     plt.tight_layout()

    # %% Detrend signal    
    force_fd = np.zeros(force_f.shape)
    diff_vals = []

    aerial_begin = step_end[:-1]
    aerial_end = step_begin[1:]

    # first step [0], extended from beginning of file
    i = 0
    diff_temp = (aerial_means[i] + aerial_means[i + 1]) / 2
    diff_vals.append(diff_temp)
    force_fd[0:step_begin[i + 1], :] = force_f[0:step_begin[i + 1], :] - diff_temp
    # 1:n-1 steps
    i = 1
    while i < min(step_begin.shape[0], step_end.shape[0]) - 1:
        diff_temp = (aerial_means[i] + aerial_means[i + 1]) / 2
        diff_vals.append(diff_temp)
        force_fd[step_begin[i]:step_begin[i + 1], :] = force_f[step_begin[i]:step_begin[i + 1], :] - diff_temp
        i = i + 1
    # last step [n], extended to end of file
    diff_temp = (aerial_means[i - 1] + aerial_means[i]) / 2
    diff_vals.append(diff_temp)
    force_fd[step_begin[i]:force_f.shape[0], :] = force_f[step_begin[i]:force_f.shape[0], :] - diff_temp

    if plots:
        # plot raw vs detrended
        plt.detrendp, (sigcomp, meancomp) = plt.subplots(2, 1, sharex=False, figsize=(15, 7))
        sigcomp.plot(np.linspace(0, force_fd.shape[0] / Fs, force_fd.shape[0]),
                     force_f[:, 2],
                     color='tab:blue',
                     alpha=0.7)  # converted to sec
        sigcomp.plot(np.linspace(0, force_fd.shape[0] / Fs, force_fd.shape[0]),
                     force_fd[:, 2],
                     color='tab:red',
                     alpha=0.7)  # converted to sec
        sigcomp.grid()
        sigcomp.legend(['original signal', 'detrended signal'], loc=1)
        sigcomp.set_xlabel('Seconds')
        sigcomp.set_ylabel('force (N)')

    # calculate mean aerial for detrend data
    aerial_means_d = np.zeros(aerial_means.shape[0])
    # gb - could use list comp (?) here to speed it up
    for i in range(aerial_begin.shape[0]):
        aerial_means_d[i] = np.mean(
            force_fd[aerial_begin[i] + trim:aerial_end[i] - trim, 2])  # just vertical force
    aerial_means_d = aerial_means_d[aerial_means_d != 0.0]

    if plots:
        # plot detrend vs old mean aerial
        meancomp.set_title('mean of aerial phases')
        meancomp.set_xlabel('steps')
        meancomp.set_ylabel('force (N)')
        meancomp.grid()
        # np.ylim([-20,20])
        for i in range(aerial_means.shape[0] - 1):
            meancomp.plot(i, aerial_means[i, 2],
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

    return force_fd, aerial_means_d

