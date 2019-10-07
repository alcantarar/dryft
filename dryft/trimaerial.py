# -*- coding: utf-8 -*-
"""

'dryft' is a library used to remove non-linear ground reaction force signal drift in a stepwise manner. It is intended
for running ground reaction force data commonly analyzed in the field of Biomechanics. The aerial phase before and after
a given step are used to tare the signal instead of assuming an overall linear trend or signal offset.

Licensed under an MIT License (c) Ryan Alcantara 2019

"""

import numpy as np
import matplotlib.pyplot as plt

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

