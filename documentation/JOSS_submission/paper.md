---
title: 'Dryft: A Python and MATLAB package to correct drifting ground reaction force signals during running'
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
[Kram et al 1998]. However, force transducer signals can be affected by changes in temperature or signal amplification
[Sloot et al. 2015, v3d documentation], causing the signal to drift. If ignored, signal drift causes inaccuracies in
data and potentially data loss if the signal exceeds the range of the force transducer. For example, ground contact
time is defined as the time the foot is in contact with the ground and is often calculated using a vertical GRF
threshold. Signal drift causes an increasing (or decreasing) amount of the vertical GRF signal to fall below the
threshold, affecting time-dependent biomechanical variables.

![Process of correcting drift from a vertical ground reaction force signal collected during treadmill running.
After aerial phases have been identified using a force threshold, aerial phase values are interpolated and subtracted
from the original signal. ](example_JOSS.png)
 
To prospectively counteract signal drift, it is best practice to zero (tare) the force transducers between trials
during data collection. This must be done when no force is being applied to the force transducers. However, zeroing
force transducers may not be feasible for protocols requiring extended periods of continuous running on an instrumented
treadmill, which could result in GRF signals drifting over time. There are signal processing methods available to
remove a constant offset [v3d documentation] or linear drift [detrend function documentation] in GRF signals, but their
effectiveness is limited because signal drift may not be linear over long durations. Prior work investigating the use
of instrumented split-belt treadmills has suggested using the aerial phase of running to tare force transducers for
each step [Paolini et al 2007, Sloot et al. 2015], but this approach has not been thoroughly explained nor the software
distributed to my knowledge. Here I introduce `dryft`, an open source Python and MATLAB package that takes a simple
approach to identifying and correcting drift in GRF signals produced during treadmill running.

# Summary
During the aerial phase of running, the body exerts no force on the ground. `dryft` assumes that any ground
reaction force measured during an aerial phase is due to signal drift. Prior work has corrected signal drift by
subtracting the force measured during a given aerial phase from each step (consecutive aerial and stance phases)
[Sloot2015, Paolini2007]. This approach assumes that there is no change in drift within a step because only one value
is being subtracted from the entire step. Instead, `dryft` interpolates the force measured during each aerial phase and
subtracts this from the entire trial (Figure 1).

To accomplish this, `dryft` uses a force threshold (user-defined) to approximate the start and end of each stance phase
and identify aerial and stance phases in a filtered vertical GRF signal. Then the GRF measured by the instrumented
treadmill during the middle of each aerial phase is extracted. Only the middle value of each aerial phase is extracted
to avoid the possibility that part of the adjacent stance phases are included in the drift estimation process. These
aerial phase values are then cubic spline interpolated to the full length of the GRF signal. These interpolated values
represent the underlying drift in the GRF signal and are subtracted, producing the corrected vertical GRF signal
(Figure 1). Once aerial phases have been identified using the vertical GRF signal, this process can be applied to
horizontal GRF signals.

![Force measured during each aerial phase before (red) and after (blue) using `dryft` to correct the drifting vertical
ground reaction force signal. Each dot represents the force measured by the treadmill at the middle of an aerial phase.](steps2.png)

To test the performance of this method, I added drift to a 30-second vertical GRF signal collected by an instrumented
treadmill during running (Fukuchi et al 2017). Using `dryft` to reduce this signal’s drift produced favorable results, as
the average force measured during across aerial phases was 0.01 N for the corrected signal (Figure 2). While `dryft` was
intended to be used with running GRF signals, it could also be applied to split-belt walking GRF signals as well, as typically
only one foot is on a belt at a time. However, extra care should be taken to the identify crossover steps
prior to correcting drift, as they may influence the accuracy of the force values measured during the swing phase.

# Acknowledgements

The author would like to thank MRP for their continued support and GB, the ABL, and
[/r/learnpython](https://reddit.com/r/learnpython) for their feedback on this package and manuscript.

# References
1. Kram, Griffin, Donelan, and Chang (1998) Force treadmill for measuring vertical and horizontal ground reaction forces.
2. Fukuchi, Fukuchi, & Duarte (2017) A public dataset of running biomechanics and the effects of running speed on lower
extremity kinematics and kinetics.
3. Scipy.signal.detrend: [https://docs.scipy.org/doc/scipy-1.1.0/reference/generated/scipy.signal.detrend.html](https://docs.scipy.org/doc/scipy-1.1.0/reference/generated/scipy.signal.detrend.html).
4. Visual3D FP_ZERO: [https://www.c-motion.com/v3dwiki/index.php/FP_ZERO](https://www.c-motion.com/v3dwiki/index.php/FP_ZERO).
5. Paolini, Della Croce, Riley, Newton, Kerrigan (2007) Testing of a tri-instrumented-treadmill unit for kinetic analysis
of locomotion tasks in static and dynamic loading conditions.
6. Sloot, Houdijk, Harlaar (2015) A comprehensive protocol to test instrumented treadmills.