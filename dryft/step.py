# -*- coding: utf-8 -*-
"""

'dryft.step' is used to separate and visualize running (or similar bouncing gait) ground reaction force (GRF) data
commonly analyzed in the field of Biomechanics.

"""

import numpy as np
import matplotlib.pyplot as plt

def split(vGRF, threshold, Fs, min_tc, max_tc, plot=False):
    """Read in filtered vertical ground reaction force (vGRF) signal and split steps based on a threshold.

    Created by Ryan Alcantara (ryan.alcantara@colorado.edu)

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
     from dryft import step
     step_begin, step_end = step.split(vGRF=force_filt[:,2], threshold=20, Fs=300, min_tc=0.2, max_tc=0.4, plot=False)
     step_begin
    array([102, 215, 325])
     step_end
    array([171, 285, 397])

    """

    if min_tc < max_tc:
        # step Identification Forces over step_threshold register as step (foot on ground).
        compare = (vGRF > threshold).astype(int)

        events = np.diff(compare)
        step_begin_all = np.squeeze(np.asarray(np.nonzero(events == 1)).transpose())
        step_end_all = np.squeeze(np.asarray(np.nonzero(events == -1)).transpose())

        if plot:
            plt.plot(vGRF)
            plt.plot(events*500)
            plt.show()

        # if trial starts with end of step, ignore
        step_end_all = step_end_all[step_end_all > step_begin_all[0]]
        # trim end of step_begin_all to match step_end_all.
        step_begin_all = step_begin_all[0:step_end_all.shape[0]]

        # initialize
        step_len = np.full(step_begin_all.shape, np.nan)  # step begin and end should be same length...
        step_begin_all = np.full(step_begin_all.shape, np.nan)
        step_end_all = np.full(step_end_all.shape, np.nan)
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
        print('Number of step begin/end:', step_end.shape[0], step_begin.shape[0])

        return step_begin, step_end

    else:
        raise IndexError('Did not separate steps. min_tc > max_tc.')


def plot(force, begin, end):
    """Plots separated steps on top of each other.

    Created by Ryan Alcantara (ryan.alcantara@colorado.edu)

    Requires an `ndarray` of beginning/end of stance phase indexes and 1d force data. Use to confirm `step.split`.

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
    `matplotlib.pyplot` figure of each step overlayed.

    Examples
    --------
    plot_separated_steps(force_filtered, begin_steps[:,0], end_steps[:,1])

    """
    colors = plt.cm.viridis(np.linspace(0,1,begin.shape[0]))

    fig, ax = plt.subplots()
    ax.set_title('All separated steps')
    ax.grid()
    ax.set_xlabel('frames')
    ax.set_ylabel('force (N)')
    for i,n in enumerate(end): plt.plot(force[begin[i]:end[i]], color = colors[i])
    plt.tight_layout()
    plt.pause(.5)
    plt.show()
