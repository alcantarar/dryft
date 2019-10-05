import numpy as np
import matplotlib.pyplot as plt

def trim(force, begin, end):
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


def calc_aerial_force(force, begin, end, trim ):
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

# %%
def plot(force, aerial_means, begin, end, trim, colormap=plt.cm.viridis):
    '''
    Plotting function for detrend_force. Plots 1) All the untrimmed aerial phases, 2) All the trimmed aerial phases,
    and 3) the means of the trimmed aerial phases. Visualizes the means used to account for drift in detrend_force function.

    '''
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
        plt.show()