import numpy as np
import matplotlib.pyplot as plt

def stepid(vGRF, threshold, Fs, min_tc, max_tc):
    '''
    This function reads in FILTERED running* ground reaction force data and splits steps based on a force threshold.

    *Running, hopping, or activity where 1 foot is on the ground at a time.

    Author: Ryan Alcantara | ryan.alcantara@colorado.edu | github.com/alcantarar
    License: MIT License in root directory

    Parameters
    -------------
    vGRF :              Array of FILTERED vertical ground reaction force (vGRF) data
    threshold :         Threshold in Newtons used to define heel-strike and toe-off. Please be responsible and set < 50N.
    Fs :                Sampling Frequency of force signal
    min_tc :            Minimum contact time (s) considered one step. Jogging should be > 0.2*Fs.
    max_tc :            Maximum contact time (s) considered one step. Jogging should be < 0.4*Fs.

    Returns
    -------------
    step_begin_all :    Array of frame indexes for beginning of stance phase
    step_end_all :      Array of frame indexes for end of stance phase
    (prints # of suspicious steps and # of step starts/ends too)

    Example
    -------------
     step_begin_all, step_end_all = step_ID(vGRF_filtered, 20, 1000, 60, 90) #20N threshold, 1000Hz, 60-90 frame step length OK
    Number of step begin/end: 77 77
    array([101, 213, 323, 435]) #step_begin_all
    array([177, 289, 401, 511]) #step_end_all

    '''

    if min_tc < max_tc:
        # step Identification Forces over step_threshold register as step (foot on ground).
        compare = (vGRF > threshold).astype(int)

        events = np.diff(compare)
        step_begin = np.squeeze(np.asarray(np.nonzero(events == 1)).transpose())
        step_end = np.squeeze(np.asarray(np.nonzero(events == -1)).transpose())

        # if trial starts with end of step, ignore
        step_end = step_end[step_end > step_begin[0]]
        # trim end of step_begin to match step_end.
        step_begin = step_begin[0:step_end.shape[0]]

        # initialize
        step_len = np.full(step_begin.shape, np.nan)  # step begin and end should be same length...
        step_begin_all = np.full(step_begin.shape, np.nan)
        step_end_all = np.full(step_end.shape, np.nan)
        # calculate step length and compare to min/max step lengths

        step_len = step_end - step_begin
        good_step = np.logical_and(step_len >= min_tc*Fs, step_len <= max_tc*Fs)

        step_begin_all = step_begin[good_step]
        step_end_all = step_end[good_step]
        # ID suspicious steps (too long or short)
        if np.any(step_len < min_tc*Fs):
            print('Out of', step_len.shape[0], 'steps,', sum(step_len < min_tc*Fs), ' < ',
                  min_tc, 'seconds.')
        if np.any(step_len > max_tc*Fs):
            print('Out of', step_len.shape[0], 'steps,', sum(step_len > max_tc*Fs), ' > ',
                  max_tc, 'seconds.')
        # print sizes
        print('Number of step begin/end:', step_end_all.shape[0], step_begin_all.shape[0])

        return step_begin_all, step_end_all

    else:
        raise IndexError('Did not separate steps. min_tc > max_tc.')


def plotsteps(force,begin,end):
    '''
    Plots separated steps on top of each other. Requires an array of beginning/end of stance phase indexes and 1d force data.
    Example:
     plot_separated_steps(force_filtered, steps[:,0], steps[:,1])
    '''
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


def trim_aerial_phases(force, begin, end):
    '''
    Receives user input to determine how much it needs to trim off the beginning and end of the aerial phase.
    This is done because filtering can cause artificial negative values where zero values rapidly change to positive values.
    These changes primarily occur during the beginning/end of stance phase.

    Graph appears with vertical black lines at the beginning/end of the a aerial phase. Function is
    waiting for two mouse clicks on plot where you'd like to trim the aerial phase. Click within the two black vertical lines!

    Input:
    -------------
    force :       1d array of vertical ground reaction force (vGF) data.
    begin :       array of frames indicating start of stance phase
    end :         array of frames indicating end of stance phase

    Returns:
    -------------
    trim :        Amount of frames to trim off the beginning and end of each aerial phase. Is average of userinputs.

    '''
    # plot a first 2 steps and get user input for how much to trim off beginning/end of aerial phase
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
            plt.close(trim_fig)

    # can't trim more than step length, but assume trim is good and step length is bad.
    aerial_begin = end[:-1]
    aerial_end = begin[1:]
    aerial_len = aerial_end - aerial_begin
    if np.any(aerial_len < trim * 2): raise IndexError(
        'Trim amount is greater than aerial phase length. If trim selection was reasonable, adjust threshold or min_step_len.')

    return trim
