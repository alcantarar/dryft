# -*- coding: utf-8 -*-
"""

'dryft' is a library used to remove non-linear ground reaction force signal drift in a stepwise manner. It is intended
for running ground reaction force data commonly analyzed in the field of Biomechanics. The aerial phase before and after
a given step are used to tare the signal instead of assuming an overall linear trend or signal offset.

Licensed under an MIT License (c) Ryan Alcantara 2019

"""

import numpy as np

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
