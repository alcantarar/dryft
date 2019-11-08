"""

View separated aerial phases and steps produced in dryft.signal.

Licensed under an MIT License (c) Ryan Alcantara 2019

Distributed here: https://github.com/alcantarar/dryft


"""
import numpy as np
import matplotlib.pyplot as plt


def aerial(force, aerial_medians, aerial_medians_loc, begin, end, trim, colormap=plt.cm.viridis):
    """Plot untrimmed aerial phases, trimmed aerial phases, and the medians of the trimmed aerial phases.

    Visualizes the medians used to account for drift in `dryft.signal.detrend` .

    Parameters
    ----------
    force : `ndarray`
        Filtered vertical ground reaction force (vGRF) signal [n,]. Using unfiltered signal will cause unreliable results.
    aerial_medians : `ndarray`
        Array of median force signal measured during each aerial phase.
    begin : `ndarray`
        Array of frame indexes for start of each aerial phase.
    end : `ndarray`
        Array of frame indexes for end of each aerial phase. Same size as `begin`.
    trim : `number`
        Number of frames to remove from beginning and end of aerial phase when calculating median. aerial.trim output.
    colormap : `colormap`
        Default is `matplotlib.plt.cm.viridis`

    """

    if aerial_medians.shape[0] == begin.shape[0]  == end.shape[0]:
        colors = colormap(np.linspace(0, 1, aerial_medians.shape[0]))
        plt.fig, (untrimp, trimp, medianp) = plt.subplots(3, 1, sharex=False, figsize=(15, 7))

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
        # plot all the medians of trimmed aerial phases
        medianp.set_title('median of trimmed aerial phases')
        medianp.set_xlabel('steps')
        medianp.set_ylabel('force (N)')
        medianp.grid()
        medianp.plot(force)
        for i in range(aerial_medians.shape[0]):
            medianp.plot(aerial_medians_loc[i], aerial_medians[i],
                       marker='o',
                       color=colors[i])
        plt.show(block = False)
    else: raise IndexError("Number of aerial_medians isn't number of steps - 1.")


def stance(force, begin, end, colormap=plt.cm.viridis):
    """Plots separated steps on top of each other.

    Requires an `ndarray` of beginning/end of stance phase indexes and 1d force data. Use to confirm `step.split`.

    Parameters
    ----------
    force : `ndarray`
        Filtered vertical ground reaction force (vGRF) signal [n,]. Using unfiltered signal will cause unreliable results.
    begin : `ndarray`
        Array of frame indexes for start of each stance phase.
    end : `ndarray`
        Array of frame indexes for end of each stance phase. Same size as `begin`.
    colormap : `colormap`
        Default is `matplotlib.plt.cm.viridis`


    Returns
    -------
    `matplotlib.pyplot` figure of each step overlayed.

    Examples
    --------
        from dryft import plot
        plot.stance(GRF_filt[:,2], step_begin, step_end)

    """
    colors = colormap(np.linspace(0,1,begin.shape[0]))

    fig, ax = plt.subplots()
    ax.set_title('All separated steps')
    ax.grid()
    ax.set_xlabel('frames')
    ax.set_ylabel('force (N)')
    for i,n in enumerate(end): plt.plot(force[begin[i]:end[i]], color = colors[i])
    plt.tight_layout()
    plt.pause(.5)
    plt.show(block = False)