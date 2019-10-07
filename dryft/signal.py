"""

'dryft' is a library used to remove non-linear ground reaction force signal drift in a stepwise manner. It is intended
for running ground reaction force data commonly analyzed in the field of Biomechanics. The aerial phase before and after
a given step are used to tare the signal instead of assuming an overall linear trend or signal offset.

Licensed under an MIT License (c) Ryan Alcantara 2019
Distributed here: https://github.com/alcantarar/detrend_force


"""
import numpy as np
import matplotlib.pyplot as plt


def detrend(force_f, Fs, aerial_means, step_begin, step_end, trim, plot=False):
    """Remove linear or non-linear drift from running ground reaction force data in a step-wise manner.

    Created by Ryan Alcantara (ryan.alcantara@colorado.edu)


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

    force_fd, aerial_means_d = signal.detrend(force_f = GRF[:,2],
                                              Fs = 300,
                                              aerial_means = aerial_means,
                                              step_begin = step_begin,
                                              step_end = step_end,
                                              trim = 8,
                                              plot=False)

    plt.plot(force_fd)
    plt.plot(GRF[:,2])
    plt.legend(['detrended signal', 'original signal'])
    plt.show()

    """

    force_fd = np.zeros(force_f.shape)
    diff_vals = []

    aerial_begin = step_end[:-1]
    aerial_end = step_begin[1:]

    # first step [0], extended from beginning of file
    i = 0
    diff_temp = (aerial_means[i] + aerial_means[i + 1]) / 2
    diff_vals.append(diff_temp)
    force_fd[0:step_begin[i + 1],] = force_f[0:step_begin[i + 1],] - diff_temp
    # 1:n-1 steps
    i = 1
    while i < min(step_begin.shape[0], step_end.shape[0]) - 1:
        diff_temp = (aerial_means[i] + aerial_means[i + 1]) / 2
        diff_vals.append(diff_temp)
        force_fd[step_begin[i]:step_begin[i + 1],] = force_f[step_begin[i]:step_begin[i + 1],] - diff_temp
        i = i + 1
    # last step [n], extended to end of file
    diff_temp = (aerial_means[i - 1] + aerial_means[i]) / 2
    diff_vals.append(diff_temp)
    force_fd[step_begin[i]:force_f.shape[0],] = force_f[step_begin[i]:force_f.shape[0],] - diff_temp

    if plot:
        # plot raw vs detrended
        plt.detrendp, (sigcomp, meancomp) = plt.subplots(2, 1, sharex=False, figsize=(15, 7))
        sigcomp.plot(np.linspace(0, force_fd.shape[0] / Fs, force_fd.shape[0]),
                     force_f,
                     color='tab:blue',
                     alpha=0.7)  # converted to sec
        sigcomp.plot(np.linspace(0, force_fd.shape[0] / Fs, force_fd.shape[0]),
                     force_fd,
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
            force_fd[aerial_begin[i] + trim:aerial_end[i] - trim,])
    aerial_means_d = aerial_means_d[aerial_means_d != 0.0]

    if plot:
        # plot detrend vs old mean aerial
        meancomp.set_title('mean of aerial phases')
        meancomp.set_xlabel('steps')
        meancomp.set_ylabel('force (N)')
        meancomp.grid()
        # np.ylim([-20,20])
        for i in range(aerial_means.shape[0] - 1):
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

    Created by Ryan Alcantara (ryan.alcantara@colorado.edu)

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
    trim : `number`
        Number of frames to trim off the beginning and end of each aerial phase when degrending force signa.
        Is calculated as average of user inputs.

    """

    aerial_begin = end[:-1]
    aerial_end = begin[1:]
    aerial_len = aerial_end - aerial_begin
    if np.any(aerial_len < trim * 2): raise IndexError(
        'Trim amount is greater than aerial phase length. If trim selection was reasonable, adjust threshold or min_step_len in step.split.')

    # calculate mean force during aerial phase (foot not on ground, should be zero)
    # aerial_means = np.full([aerial_begin.shape[0] + 1,], np.nan)
    if force.ndim == 1:  # one axis only
        aerial_means = np.full([aerial_begin.shape[0] + 1, ], np.nan)
        i = 0
        while i < min(begin.shape[0], end.shape[0]) - 1:
            aerial_means[i,] = np.mean(force[aerial_begin[i] + trim:aerial_end[i] - trim])
            i = i + 1
        # last step
        aerial_means[i] = np.mean(force[aerial_begin[i - 1] + trim:aerial_end[i - 1] - trim])
    else: raise IndexError('force.ndim != 1')

    return aerial_means


def plotaerial(force, aerial_means, begin, end, trim, colormap=plt.cm.viridis):
    """Plot untrimmed aerial phases, trimmed aerial phases, and the means of the trimmed aerial phases.

    Created by Ryan Alcantara (ryan.alcantara@colorado.edu)

    Visualizes the means used to account for drift in `dryft.signal.detrend` .

    Parameters
    ----------
    force : `ndarray`
        Filtered vertical ground reaction force (vGRF) signal [n,]. Using unfiltered signal will cause unreliable results.
    aerial_means : `ndarray`
        Array of mean force signal measured during each aerial phase.
    begin : `ndarray`
        Array of frame indexes for start of each stance phase.
    end : `ndarray`
        Array of frame indexes for end of each stance phase. Same size as `begin`.
    trim : `number`
        Number of frames to remove from beginning and end of aerial phase when calculating mean. aerial.trim output.
    colormap : `colormap`
        Default is `matplotlib.plt.cm.viridis`

    """

    if aerial_means.shape[0] == begin.shape[0] + 1 == end.shape[0] + 1:
        colors = colormap(np.linspace(0, 1, aerial_means.shape[0]))
        plt.fig, (untrimp, trimp, meanp) = plt.subplots(3, 1, sharex=False, figsize=(15, 7))

        # plot of untrimmed aerial phases
        untrimp.set_title('untrimmed aerial phases')
        untrimp.set_ylabel('force (N)')
        untrimp.grid()
        for i in range(begin.shape[0]):
            untrimp.plot(force[begin[i]:end[i]],
                         color=colors[i])
            # plot of trimmed aerial phases
        trimp.set_title('trimmed aerial phases')
        trimp.set_ylabel('force (N)')
        trimp.grid()
        for i in range(begin.shape[0]):
            trimp.plot(force[begin[i] + trim:end[i] - trim],
                       color=colors[i])
        # plot all the means of trimmed aerial phases
        meanp.set_title('mean of trimmed aerial phases')
        meanp.set_xlabel('steps')
        meanp.set_ylabel('force (N)')
        meanp.grid()
        for i in range(aerial_means.shape[0]):
            meanp.plot(i, aerial_means[i],
                       marker='o',
                       color=colors[i])
        plt.show(block = False)


def plotsteps(force, begin, end):
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
    plt.show(block = False)


def splitsteps(vGRF, threshold, Fs, min_tc, max_tc, plot=False):
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

    Created by Ryan Alcantara (ryan.alcantara@colorado.edu)

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
    trim : `number`
        Number of frames to trim off the beginning and end of each aerial phase when degrending force signa.
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
    else: raise IndexError('force.ndim != 1')
    return trim

