"""

Removes non-linear ground reaction force signal drift in a stepwise manner. It is intended
for running ground reaction force data commonly analyzed in the field of Biomechanics. The aerial phase before and after
a given step are used to tare the signal instead of assuming an overall linear trend or signal offset.

Licensed under an MIT License (c) Ryan Alcantara 2019

Distributed here: https://github.com/alcantarar/dryft


"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import pandas as pd

def detrend(force_f, Fs, aerial_means, aerial_means_loc, step_begin, step_end, trim, plot=False):
    """Remove linear or non-linear drift from running ground reaction force data in a step-wise manner.

    Parameters
    ----------
    force_f : `ndarray`
        Filtered ground reaction force signal [n,]. Using unfiltered signal may cause unreliable results.
    Fs : `number`
        Sampling frequency of force signal
    aerial_means : `ndarray`
        Array of mean force signal measured during each aerial phase.
    step_begin : `ndarray`
        Array of frame indexes for start of each stance phase.
    step_end : `ndarray`
        Array of frame indexes for end of each stance phase. Same size as `begin`.
    trim : `number`
        Number of frames removed from start and end of aerial phase when calculating `aerial_means` in `aerial.trim`.
    plot : `bool` Default=False
        If true, show plots comparing signal pre vs. post stepwise detrend.

    Returns
    -------
    force_fd : `ndarray`
        Array with shape of force_f, but with drift removed (detrended).
    aerial_means_d : `ndarray`
        Array of mean force signal during aerial phase for detrended signal. Compare to `aerial_means`.

    Examples
    --------
        from dryft import signal
        import matplotlib.pyplot as plt

        force_fd, aerial_means_d = signal.detrend(GRF_filt[:,2],
                                              Fs,
                                              aerial_means,
                                              step_begin,
                                              step_end,
                                              trim,
                                              plot=True)

    """

    force_fd = np.zeros(force_f.shape)
    diff_vals = []

    aerial_begin = step_end[:-1]
    aerial_end = step_begin[1:]
    #
    # # first step [0], extended from beginning of file
    # i = 0
    # diff_temp = aerial_means[i] # just use aerial phase after first step. guaranteed to be there.
    # diff_vals.append(diff_temp)
    # force_fd[0:step_begin[i + 1],] = force_f[0:step_begin[i + 1],] - diff_temp
    # # 1:n-1 steps
    # i = 1
    # while i < min(step_begin.shape[0], step_end.shape[0])-1: #less than 79
    #     diff_temp = (aerial_means[i-1] + aerial_means[i]) / 2
    #     diff_vals.append(diff_temp)
    #     force_fd[step_begin[i]:step_begin[i + 1],] = force_f[step_begin[i]:step_begin[i + 1],] - diff_temp
    #     i = i + 1
    # # last step [n], extended to end of file
    # diff_temp = aerial_means[i-1] # just use aerial phase right before last step. guaranteed to be there
    # diff_vals.append(diff_temp)
    # force_fd[step_begin[i]:force_f.shape[0],] = force_f[step_begin[i]:force_f.shape[0],] - diff_temp

    # interp/extrap aerial_means to length of force_f
    drift_signal = np.full(force_f.shape, np.nan)
    drift_signal[aerial_means_loc] = aerial_means
    drift_signal_p = pd.Series(drift_signal)
    drift_signal_p = drift_signal_p.interpolate(method = 'spline', order = 3, s = 0, limit_direction= 'both') #sline works between values, doesn't extend
    drift_signal = drift_signal_p.to_numpy()

    force_fd = force_f - drift_signal

    if plot:
        # plot raw vs detrended
        plt.detrendp, (sigcomp, meancomp) = plt.subplots(2, 1, sharex=False, figsize=(15, 7))
        sigcomp.plot(np.linspace(0, force_fd.shape[0] / Fs, force_fd.shape[0]),
                     force_f,
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

    # calculate mean aerial for detrend data
    step_begin_d, step_end_d = splitsteps(vGRF=force_fd[:,],
                                             threshold=10,
                                             Fs=300,
                                             min_tc=0.2,
                                             max_tc=0.4,
                                             plot=False)
    aerial_means_d, aerial_means_loc_d = meanaerialforce(force_fd[:,], step_begin_d, step_end_d,trim=10)

    if plot:
        # plot detrend vs old mean aerial
        meancomp.set_title('mean of aerial phases')
        meancomp.set_xlabel('steps')
        meancomp.set_ylabel('force (N)')
        meancomp.grid()
        # np.ylim([-20,20])
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

    return force_fd, aerial_means_d


def meanaerialforce(force, begin, end, trim ):
    """Calculate mean force signal during aerial phase of running.

    Parameters
    ----------
    force : `ndarray`
        Filtered vertical ground reaction force (vGRF) signal [n,]. Using unfiltered signal will cause unreliable results.
    begin : `ndarray`
        Array of frame indexes for start of each stance phase.
    end : `ndarray`
        Array of frame indexes for end of each stance phase. Same size as `begin`.
    trim : `number`
        Number of frames to remove from beginning and end of aerial phase when calculating mean. aerial.trim output.

    Returns
    -------
    aerial_means : `ndarray`
        Array containing means of aerial phase force signal. Excludes part of start/end of aerial phase as defined by `trim`.

    """
    def closest_to_median(array):
        array = np.asarray(array)
        ind = (np.abs(array-np.median(array))).argmin()
        return array[ind]

    aerial_begin = end[:-1]
    aerial_end = begin[1:]
    aerial_len = aerial_end - aerial_begin
    if np.any(aerial_len < trim * 2): raise IndexError(
        'Trim amount is greater than aerial phase length. If trim selection was reasonable, adjust threshold or min_step_len in step.split.')

    # calculate mean force during aerial phase (foot not on ground, should be zero)
    # aerial_means = np.full([aerial_begin.shape[0] + 1,], np.nan)
    if force.ndim == 1:  # one axis only
        aerial_means = np.full([aerial_begin.shape[0], ], np.nan)
        aerial_means_loc = np.full([aerial_begin.shape[0], ], np.nan)

        for i in range(aerial_means.shape[0]):
            aerial_means[i,] = closest_to_median(force[aerial_begin[i] + trim:aerial_end[i] - trim])
            aerial_means_loc[i,] = aerial_begin[i] + trim + np.argwhere(force[aerial_begin[i] + trim:aerial_end[i] - trim] == aerial_means[i,])
        aerial_means_loc = aerial_means_loc.astype(int)
    else: raise IndexError('force.ndim != 1')

    return aerial_means, aerial_means_loc




def splitsteps(vGRF, threshold, Fs, min_tc, max_tc, plot=False):
    """Read in filtered vertical ground reaction force (vGRF) signal and split steps based on a threshold.

    Designed for running, hopping, or activity where 1 foot is on the force plate at a time.
    Split steps are compared to min/max contact time (tc) to eliminate steps that are too short/long. Update these
    parameters and threshold if little-no steps are identified. Setting plots=True can aid in troubleshooting.

    Parameters
    ----------
    vGRF : `ndarray`
        Filtered vertical ground reaction force (vGRF) signal [n,]. Using unfiltered signal will cause unreliable results.
    threshold : `number`
        Determines when initial contact and final contact are defined. In the same units as vGRF signal. Please be
        responsible and set to < 50N for running data.
    Fs : `number`
        Sampling frequency of signal.
    min_tc : `number`
        Minimum contact time, in seconds, to consider as a real step. Jogging > 0.2s
    max_tc : number
        Maximum contact time, in seconds, to consider as a real step. Jogging > 0.4s
    plot : `bool`
        If true, return plot showing vGRF signal with initial and final contact points identified. Helpful for
        determining appropriate threshold, min_tc, and max_tc values.

    Returns
    -------
    step_begin : `ndarray`
        Array of frame indexes for start of stance phase.
    step_end : `ndarray`
        Array of frame indexes for end of stance phase.

    Examples
    --------
        from dryft import signal
        step_begin, step_end = signal.splitsteps(vGRF=GRF_filt[:,2],
                                             threshold=110,
                                             Fs=300,
                                             min_tc=0.2,
                                             max_tc=0.4,
                                             plot=False)
        step_begin
        step_end

    array([102, 215, 325])
    array([171, 285, 397])

    """

    if min_tc < max_tc:
        # step Identification Forces over step_threshold register as step (foot on ground).
        compare = (vGRF > threshold).astype(int)

        events = np.diff(compare)
        print(sum((compare)))
        step_begin_all = np.squeeze(np.asarray(np.nonzero(events == 1)).transpose())
        step_end_all = np.squeeze(np.asarray(np.nonzero(events == -1)).transpose())

        if plot:
            plt.plot(vGRF)
            plt.plot(events*500)
            plt.show(block = False)

        # if trial starts with end of step, ignore
        step_end_all = step_end_all[step_end_all > step_begin_all[0]]
        # trim end of step_begin_all to match step_end_all.
        step_begin_all = step_begin_all[0:step_end_all.shape[0]]

        # initialize
        # step_len = np.full(step_begin_all.shape, np.nan)  # step begin and end should be same length...
        # step_begin = np.full(step_begin_all.shape, np.nan)
        # step_end = np.full(step_end_all.shape, np.nan)
        # calculate step length and compare to min/max step lengths

        step_len = step_end_all - step_begin_all
        good_step = np.logical_and(step_len >= min_tc*Fs, step_len <= max_tc*Fs)

        step_begin = step_begin_all[good_step]
        step_end = step_end_all[good_step]
        # ID suspicious steps (too long or short)
        if np.any(step_len < min_tc*Fs):
            print('Out of', step_len.shape[0], 'steps,', sum(step_len < min_tc*Fs), ' < ',
                  min_tc, 'seconds.')
        if np.any(step_len > max_tc*Fs):
            print('Out of', step_len.shape[0], 'steps,', sum(step_len > max_tc*Fs), ' > ',
                  max_tc, 'seconds.')
        # print sizes
        print('Number of contact time begin/end:', step_begin.shape[0], step_end.shape[0])

        return step_begin, step_end

    else:
        raise IndexError('Did not separate steps. min_tc > max_tc.')


def trimaerial(force, begin, end):
    """Receives user input to determine how much it needs to trim off the beginning and end of the aerial phase.

    Trimming is required when detrending a force signal as filtering can cause artificial negative values where zero
    values rapidly change to positive values. These changes primarily occur during the beginning/end of stance phase. A
    graph appears with vertical black lines at the beginning/end of the a aerial phase. Function is waiting for two
    mouse clicks on plot where you'd like to trim the aerial phase. Click within the two black vertical lines!

    Parameters
    ----------
    force : `ndarray`
        Filtered vertical ground reaction force (vGRF) signal [n,]. Using unfiltered signal will cause unreliable results.
    begin : `ndarray`
        Array of frame indexes for start of each stance phase.
    end : `ndarray`
        Array of frame indexes for end of each stance phase. Same size as `begin`.

    Returns
    -------
    trim : `integer`
        Number of frames to trim off the beginning and end of each aerial phase when calculating mean during aerial phase.
        Is calculated as average of user inputs.

    """

    # plot a first 2 steps and get user input for how much to trim off beginning/end of aerial phase
    if force.ndim == 1:  # one axis only
        trim_fig, ax = plt.subplots()
        ax.plot(force[begin[0]:end[1]],
                color='tab:blue')
        start_a = force[begin[0]:end[1]] == force[end[0]]
        end_a = force[begin[0]:end[1]] == force[begin[1]]
        ax.axvline(start_a.nonzero(), color='k')
        ax.axvline(end_a.nonzero(), color='k')
        ax.set_title('select how much to trim off beginning/end \n of aerial phase (between black lines)')
        ax.set_xlabel('frames')
        ax.set_ylabel('force (N)')
        plt.tight_layout()
        plt.show(block = False)
        # user input from mouse click
        bad_points = 1
        while bad_points:
            points = np.asarray(plt.ginput(2, timeout=0), dtype=int)

            if sum(points[:, 0] < start_a.nonzero()[0][0]) > 0 or sum(points[:, 0] > end_a.nonzero()[0][0]) > 0:
                # points outside of range
                print("Can't trim negative amount. Select 2 points between start/end of aerial phase")
            elif points[1, 0] < points[0, 0]:
                # points in wrong order
                print(
                    "First select amount to trim off the start, then select the amount to trim off the end of aerial phase")
            else:
                trim = (
                    np.round((points[0, 0] - start_a.nonzero()[0][0] + end_a.nonzero()[0][0] - points[1, 0]) / 2)).astype(
                    int)
                print('trimming ', trim, ' frames from the start/end of aerial phase')
                bad_points = 0
    else: raise IndexError('force.ndim != 1')

    plt.close()
    return trim

