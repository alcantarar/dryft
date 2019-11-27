"""

View separated aerial phases and steps produced in dryft.signal.

Licensed under an MIT License (c) Ryan Alcantara 2019

Distributed here: https://github.com/alcantarar/dryft


"""
import numpy as np
import matplotlib.pyplot as plt
from dryft import signal


def aerial(force, aerial_values, aerial_loc, stance_begin, stance_end, good_stances, colormap=plt.cm.viridis):
    """Plot aerial phase waveforms with middle identified and separated aerial phase values.

    Visualizes the aerial phase values used to correct for drift in `dryft.signal.detrend` .

    Parameters
    ----------
    force : `ndarray`
        Filtered vertical ground reaction force (vGRF) signal [n,]. Using unfiltered signal will cause unreliable results.
    aerial_values : `ndarray`
        Array of force signal measured at middle of each aerial phase. Output from `signal.aerialforce()`
    aerial_loc : `ndarray`
        Array of frame indexes for values in aerial_values. Output from `signal.aerialforce()`
    stance_begin : `ndarray`
        Array of frame indexes for start of each stance phase. Output from `signal.splitsteps()`
    stance_end : `ndarray`
        Array of frame indexes for end of each stance phase. Same size as `begin`. Output from `signal.splitsteps()`
    good_stances : `ndarray`
            Boolean array of which stance phases meet min_tc & max_tc requirements.
    colormap : `colormap`
        Default is `matplotlib.plt.cm.viridis`

    """
    # define beginning/end of aerial phases
    if False in good_stances:
        begin, end = signal.findgoodaerial(stance_begin, stance_end, good_stances)
    else:
        begin = stance_end[good_stances][:-1]
        end = stance_begin[good_stances][1:]

    if aerial_values.shape[0] == begin.shape[0]  == end.shape[0]:
        colors = colormap(np.linspace(0, 1, aerial_values.shape[0]))
        plt.fig, (plt1, plt2) = plt.subplots(2, 1, figsize=(15, 7))

        # plot of  aerial phases
        plt1.set_title('Aerial phases (black dot is middle)')
        plt1.set_ylabel('force (N)')
        plt1.grid()
        for i in range(begin.shape[0]):
            plt1.plot(force[begin[i]:end[i]],
                         color=colors[i])
            plt1.plot(aerial_loc[i]-begin[i], aerial_values[i],'k.')
            # plot of aerial phases
        # plot all the aerial phase values separate
        plt2.set_title('Force measured at middle of aerial phases')
        plt2.set_xlabel('Frame')
        plt2.set_ylabel('force (N)')
        plt2.grid()
        for i, n in enumerate(aerial_loc):
            plt2.plot(n, aerial_values[i],
                       marker='o',
                       color=colors[i])
        plt.show(block = False)
    else: raise IndexError("Number of aerial_values isn't number of steps - 1.")


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
    """
    colors = colormap(np.linspace(0,1,begin.shape[0]))

    fig, ax = plt.subplots()
    ax.set_title('All separated steps')
    ax.grid()
    ax.set_xlabel('frames')
    ax.set_ylabel('force (N)')
    for i,n in enumerate(end): plt.plot(force[begin[i]:end[i]], color = colors[i])
    plt.tight_layout()
    plt.show(block = False)