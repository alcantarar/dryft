"""

'dryft' is a library used to remove non-linear ground reaction force signal drift in a stepwise manner. It is intended
for running ground reaction force data commonly analyzed in the field of Biomechanics. The aerial phase before and after
a given step are used to tare the signal instead of assuming an overall linear trend or signal offset.

Licensed under an MIT License (c) Ryan Alcantara 2019
Distributed as a module of Dryft: https://github.com/alcantarar/detrend_force

"""

import numpy as np
import matplotlib.pyplot as plt


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

