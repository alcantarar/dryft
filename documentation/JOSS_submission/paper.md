---
title: "Dryft: A Python and MATLAB package to correct drifting ground reaction force signals during treadmill running"
tags:
  - biomechanics
  - signal processing
  - detrend
  - GRF
  - walking
authors:
  - name: Ryan S. Alcantara
    orcid: 0000-0002-8539-711X
    affiliation: "1"
affiliations:
 - name: Department of Integrative Physiology, University of Colorado Boulder, Boulder CO, USA 
   index: 1
date: 31 October 2019 #spooktober
bibliography: paper.bib
---

# Background
Ground reaction forces (GRFs) are exerted by the body on the ground during running, measured by treadmills instrumented
with force transducers, and are used to calculate a variety of clinical and performance-related biomechanical variables
[@kram:1998]. However, force transducer signals can be affected by changes in temperature during warm up or over long periods
[@sloot2015comprehensive], causing the signal to drift. If ignored, signal drift can lead to the inaccurate calculation of
biomechanical variables. For example, ground contact time is defined as the time the foot is in contact with the ground and is often
calculated as the time a vertical GRF exceeds a threshold. Signal drift can cause more (or less) of the vertical GRF
signal to fall below the threshold, affecting one's ability to identify stance phase [@riley2008kinematics] or calculate of time-dependent GRF
metrics. Signal drift can also potentially lead to data loss if the signal exceeds the range of the force transducer.

![The process of correcting drift in a vertical ground reaction force (GRF) signal collected during treadmill running.
After aerial phases have been identified using a force threshold, `dryft` interpolates aerial phase values to estimate
the underlying drift and subtracts it from the vertical GRF signal. ](example_JOSS.png)
 
To prospectively counteract signal drift, it is best practice to zero (tare) the force transducers between trials
during data collection. However, zeroing force transducers may not be feasible for protocols requiring extended periods
of continuous running on an instrumented treadmill. There are signal processing methods available to remove a constant
offset [@v3d:FP_ZERO] or linear drift [@scipy:detrend] in GRF signals, but their effectiveness is
limited because signal drift may not be linear over the duration of the trial. Here I introduce `dryft`, an open source
Python and MATLAB package that takes a simple approach to identifying and correcting linear or non-linear drift in GRF signals
produced during treadmill running.

# Summary
The body exerts no force on the ground during the aerial phase of running and `dryft` assumes that any ground
reaction force measured during an aerial phase is due to noise or drift in the signal. `dryft` implements a user-defined
force threshold to approximate the start and end of each stance phase and identify aerial phases in a
filtered vertical GRF signal (Figure 1). Next, the force measured by the instrumented treadmill during the middle of each aerial
phase is identified. The middle value of each aerial phase is identified to avoid the possibility that part of the
adjacent stance phases are included in the drift estimation process. These aerial phase values are then cubic spline
interpolated to the full length of the GRF signal to estimate the underlying drift in the GRF signal. The
estimated drift is then subtracted from the GRF signal (Figure 1). This process can also be applied to horizontal GRF signals
once aerial phases have been identified using the vertical GRF signal.

To test the performance of this method, I added drift to a 30-second vertical GRF signal collected by an instrumented
treadmill during running [@fukuchi2017public]. Using `dryft` to reduce this vertical GRF signal’s drift produced favorable results, as
the average (± SD) force measured across the extracted aerial phases values was -0.01 N (± 0.09 N) for the corrected signal (Figure 2). While `dryft` was
intended to be used with GRF signals measured during treadmill running, it could also be applied to GRF signals measured
during split-belt treadmill walking, since only one foot is on a belt at a time. However, extra care should be
taken to identify crossover steps prior to correcting drift in split-belt treadmill walking GRF data as they will
influence the accuracy of the force values measured during the swing phase.

![Vertical ground reaction force (GRF) measured during each aerial phase before (red) and after (blue) using `dryft` to correct
the drifting vertical GRF signal. Each point represents the force measured by the treadmill at the middle
of an aerial phase.](steps.png)

# Conclusion
Prior work has corrected drift in GRF signals by subtracting the force measured during a given
aerial phase from the following stance phase [@sloot2015comprehensive; @paolini2007testing; @riley2008kinematics]. The
success of this approach heavily relies on how accurately stance and aerial phases are identified and assumes that there
is no change in drift within a given step (consecutive aerial and stance phases). Instead, `dryft` interpolates the
force measured at the middle of each aerial phase and subtracts this from the entire trial. This package can be used to
identify stance phases and correct linear or non-linear drift in GRF signals produced during treadmill running or
split-belt treadmill walking.


# Acknowledgements

The author would like to thank Maggie Peterson for their continued support and Gary Bruening, the Applied Biomechanics 
Lab, and [/r/learnpython](https://reddit.com/r/learnpython) for their feedback on this package and manuscript.

# References
