"""

Removes non-linear ground reaction force signal drift in a stepwise manner. It is intended
for running ground reaction force data commonly analyzed in the field of Biomechanics. The aerial phase before and after
a given stance phase are used to tare the signal instead of assuming an overall linear trend or signal offset.

Licensed under an MIT License (c) Ryan Alcantara 2019

Distributed here: https://github.com/alcantarar/dryft


"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def detrend(force_f, aerial, aerial_loc):
    """Remove drift from running ground reaction force signal based on aerial phases.

    Parameters
    ----------
    force_f : `ndarray`
        Filtered ground reaction force signal [n,]. Using unfiltered signal may cause unreliable results.
    aerial : `ndarray`
        Array of force signal measured at middle of each aerial phase.
    aerial_loc : `ndarray`
        Array of frame indexes for values in aerial. output from `aerialforce()`

    Returns
    -------
    force_fd : `ndarray`
        Array with shape of force_f, but with drift removed (detrended).

    Examples
    --------
        from dryft import signal

        force_fd = signal.detrend(force_f, aerial, aerial_loc)

    """

    force_f = force_f.flatten()
    # Create NaN array with aerial values at respective frame locations

    drift_signal = np.full(force_f.shape, np.nan)
    drift_signal[aerial_loc] = aerial
    # Use 3rd order spline to fill NaNs, creating the underlying drift of the signal.
    drift_signal_p = pd.Series(drift_signal)
    drift_signal_p = drift_signal_p.interpolate(method = 'spline', order = 3, s = 0, limit_direction= 'both')
    drift_signal = drift_signal_p.to_numpy()
    # Subtract drift from force signal
    force_fd = force_f - drift_signal

    return force_fd


def findgoodaerial(stance_begin, stance_end, good_stances):
    """Locate good aerial phases when bad stance phases are present.

        Parameters
        ----------
        stance_begin : `ndarray`
            Array of frame indexes for start of each stance phase.
        stance_end : `ndarray`
            Array of frame indexes for end of each stance phase. Same size as `begin`.
        good_stances : `ndarray`
            Boolean array of which stance phases meet min_tc & max_tc requirements.

        Returns
        -------
        good_aerial_begin : `ndarray`
            Array of frame indexes for aerial phase beginnings not connected to bad steps (per min/max_tc requirements).
        good_aerial_end : `ndarray`
            Array of frame indexes for aerial phase ends not connected to bad steps (per min/max_tc requirements).

        """
    bs = np.where(good_stances == False)
    aerial_start = np.ones((len(good_stances),), dtype=bool)
    aerial_end = np.ones((len(good_stances),), dtype=bool)

    aerial_end[bs[0]] = False
    aerial_end[bs[0] + 1] = False

    aerial_start[bs[0]] = False
    aerial_start[bs[0] - 1] = False

    good_aerial_begin = stance_end[aerial_start][:-1]
    good_aerial_end = stance_begin[aerial_end][1:]

    return good_aerial_begin, good_aerial_end


def aerialforce(force, begin, end, good_stances):
    """Calculate force signal at middle of aerial phase of running.

    Parameters
    ----------
    force : `ndarray`
        Filtered vertical ground reaction force (vGRF) signal [n,]. Using unfiltered signal will cause unreliable results.
    begin : `ndarray`
        Array of frame indexes for start of each stance phase.
    end : `ndarray`
        Array of frame indexes for end of each stance phase. Same size as `begin`.
    good_stances : `ndarray`
        Boolean array of which stance phases meet min_tc & max_tc requirements.

    Returns
    -------
    aerial : `ndarray`
        Array containing force measured at middle of aerial phase force signal.
    aerial_loc : `ndarray`
        Array of frame indexes for values in aerial. output from `aerialforce()`

    """
    if False in good_stances:
        aerial_begin, aerial_end = findgoodaerial(begin, end, good_stances)
    else:
        aerial_begin = end[good_stances][:-1]
        aerial_end = begin[good_stances][1:]

    # calculate force at middle of aerial phase (foot not on ground, should be zero)
    if force.ndim == 2:  # one axis only
        force = force.flatten()
        aerial = np.full([aerial_begin.shape[0], ], np.nan)
        aerial_middle = np.full([aerial_begin.shape[0], ], np.nan)
    elif force.ndim == 1:
        aerial = np.full([aerial_begin.shape[0], ], np.nan)
        aerial_middle = np.full([aerial_begin.shape[0], ], np.nan)
    else: raise IndexError('Can only handle shape (n,) or (n,1)')

    for i in range(aerial.shape[0]):
        aerial_len = aerial_end-aerial_begin
        aerial_middle[i,] = round(aerial_len[i]/2)
        aerial[i,] = force[aerial_begin[i]+aerial_middle.astype(int)[i]]
    aerial_loc = aerial_begin + aerial_middle.astype(int)

    return aerial, aerial_loc


def splitsteps(vGRF, threshold, Fs, min_tc, max_tc, plot=False):
    """Read in filtered vertical ground reaction force (vGRF) signal and ID stance phases based on a threshold.

    Designed for running, hopping, or activity where 1 foot is on the force plate at a time.
    Identified stance phases are compared to min/max contact time (tc) to eliminate ones that are too short/long. 
    Update these parameters and threshold if little-no stance phases are identified. Setting plots=True can aid in 
    troubleshooting.

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
        Minimum contact time, in seconds, to consider as a real stance phase. Jogging > 0.2s
    max_tc : number
        Maximum contact time, in seconds, to consider as a real stance phase. Jogging > 0.4s
    plot : `bool`
        If true, return plot showing vGRF signal with initial and final contact points identified. Helpful for
        determining appropriate threshold, min_tc, and max_tc values.

    Returns
    -------
    stance_begin_all : `ndarray`
        Array of frame indexes for every start of stance phase found in trial. Use `good_stances` to index which ones
        pass the min/max_tc requirements.
    stance_end_all : `ndarray`
        Array of frame indexes for every end of stance phase found in trial. Use `good_stances` to index which ones
        pass the min/max_tc requirements.
    good_stances : `ndarray`
        Boolean array of which stance phases meet min_tc & max_tc requirements.

    Examples
    --------
        from dryft import signal
        stance_begin, stance_end = signal.splitsteps(vGRF=GRF_filt[:,2],
                                             threshold=110,
                                             Fs=300,
                                             min_tc=0.2,
                                             max_tc=0.4,
                                             plot=False)
        stance_begin
        stance_end

    array([102, 215, 325])
    array([171, 285, 397])

    """

    if min_tc < max_tc:
        # Identification. Forces over threshold register as stance phase (foot on ground).
        compare = (vGRF.flatten() > threshold).astype(int)

        events = np.diff(compare)
        stance_begin_all = np.squeeze(np.asarray(np.nonzero(events == 1)).transpose())
        stance_end_all = np.squeeze(np.asarray(np.nonzero(events == -1)).transpose())

        if plot:
            plt.plot(vGRF)
            plt.plot(events*500)
            plt.show(block = False)

        # if trial starts with end of stance phase, ignore
        stance_end_all = stance_end_all[stance_end_all > stance_begin_all[0]]
        # trim end of stance_begin_all to match stance_end_all.
        stance_begin_all = stance_begin_all[0:stance_end_all.shape[0]]

        stance_len = stance_end_all - stance_begin_all
        good_stances = np.logical_and(stance_len >= min_tc*Fs, stance_len <= max_tc*Fs)

        # ID suspicious stance phases (too long or short)
        if np.any(stance_len < min_tc*Fs):
            print('Out of', stance_len.shape[0], 'stance phases,', sum(stance_len < min_tc*Fs), ' < ',
                  min_tc, 'seconds.')
        if np.any(stance_len > max_tc*Fs):
            print('Out of', stance_len.shape[0], 'stance_phases,', sum(stance_len > max_tc*Fs), ' > ',
                  max_tc, 'seconds.')
        # print sizes
        print('Total number of contact time begin/end:', stance_begin_all.shape[0], stance_end_all.shape[0])

        return stance_begin_all, stance_end_all, good_stances

    else:
        raise IndexError('Did not ID stance phases: min_tc > max_tc.')
