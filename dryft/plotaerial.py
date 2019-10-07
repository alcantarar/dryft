# -*- coding: utf-8 -*-
"""

'dryft' is a library used to remove non-linear ground reaction force signal drift in a stepwise manner. It is intended
for running ground reaction force data commonly analyzed in the field of Biomechanics. The aerial phase before and after
a given step are used to tare the signal instead of assuming an overall linear trend or signal offset.

Licensed under an MIT License (c) Ryan Alcantara 2019

"""

import numpy as np
import matplotlib.pyplot as plt

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