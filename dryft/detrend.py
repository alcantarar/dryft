# -*- coding: utf-8 -*-
"""

'dryft' is a library used to remove non-linear ground reaction force signal drift in a stepwise manner. It is intended
for running ground reaction force data commonly analyzed in the field of Biomechanics. The aerial phase before and after
a given step are used to tare the signal instead of assuming an overall linear trend or signal offset.

Licensed under an MIT License (c) Ryan Alcantara 2019

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
