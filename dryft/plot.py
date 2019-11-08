"""

View separated aerial phases and steps produced in dryft.signal.

Licensed under an MIT License (c) Ryan Alcantara 2019

Distributed here: https://github.com/alcantarar/dryft


"""
import numpy as np
import matplotlib.pyplot as plt


def aerial(force, aerial_values, aerial_loc, begin, end, colormap=plt.cm.viridis):
    """Plot aerial phase waveforms with middle identified and separated aerial phase values.

    Visualizes the aerial phase values used to correct for drift in `dryft.signal.detrend` .

    Parameters
    ----------
    force : `ndarray`
        Filtered vertical ground reaction force (vGRF) signal [n,]. Using unfiltered signal will cause unreliable results.
    aerial_values : `ndarray`
        Array of force signal measured at middle of each aerial phase. Output from `aerialforce()`
    aerial_loc : `ndarray`
        Array of frame indexes for values in aerial_values. Output from `aerialforce()`
    begin : `ndarray`
        Array of frame indexes for start of each aerial phase.
    end : `ndarray`
        Array of frame indexes for end of each aerial phase. Same size as `begin`.
    colormap : `colormap`
        Default is `matplotlib.plt.cm.viridis`

    """

    if aerial_values.shape[0] == begin.shape[0]  == end.shape[0]:
        colors = colormap(np.linspace(0, 1, aerial_values.shape[0]))
        plt.fig, (plt1, plt2) = plt.subplots(2, 1, figsize=(15, 7))

        # plot of untrimmed aerial phases
        plt1.set_title('untrimmed aerial phases')
        plt1.set_ylabel('force (N)')
        plt1.grid()
        for i in range(begin.shape[0]):
            plt1.plot(force[begin[i]:end[i]],
                         color=colors[i])
            plt1.plot(aerial_loc[i]-begin[i], aerial_values[i],'k.')
            # plot of aerial phases
        # plot all the aerial phase values separate
        plt2.set_title('Force measured at middle of aerial phases')
        plt2.set_xlabel('Step #')
        plt2.set_ylabel('force (N)')
        plt2.grid()
        for i in range(aerial_values.shape[0]):
            plt2.plot(i, aerial_values[i],
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