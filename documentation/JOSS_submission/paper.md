---
title: 'Dryft: A Python and MATLAB package to correct drifting ground reaction force signals during running’
tags:
  - biomechanics
  - signal processing
  - detrend
  - GRF
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
Ground reaction forces (GRFs) are exerted by the body on the ground during running and are used to calculate a variety of
clinical and performance-related biomechanical variables.
GRFs can be measured by platforms and treadmills instrumented with three-dimensional force transducers.
However, force transducer signals can be affected by changes in temperature or signal amplifiers, causing the signal to 
drift.
If ignored, signal drift causes inaccuracies in data and potentially data loss if the signal exceeds the range of the 
force transducer.
For example, contact time is defined as the time the foot is in contact with the ground and is often calculated as the 
duration when the vertical GRF signal is above a set threshold.  
Signal drift can cause an increasing (or decreasing) amount of the vertical GRF signal to fall below the threshold, 
artificially increasing the variability in contact time values or other time-dependent biomechanical variables (Figure 1).

![Figure 1](Figure_1.png)
*Figure 1. Vertical ground reaction force signal where signal drifts positively 100 Newtons. 
Contact time increases by ~0.04s, or ~17%.* 
 
To counteract signal drift, it is best practice to tare (“zero”) the force transducer signal between trials during data 
collection. 
This must be done when no force is being applied to the force transducers to ensure accurate signals.
However, zeroing force transducers may not be feasible for protocols requiring extended periods of continuous running on an 
instrumented treadmill, allowing GRF signals to drift over time.
There are signal processing methods available to remove offsets [v3d] and linear drift [scipy/matlab detrend] in GRF 
signals, but their effectiveness is limited as signal drift is not guaranteed to be linear over long durations. 
Here, I introduce `dryft`, a Python and MATLAB package that takes a stepwise approach to removing drift in 
a GRF signal produced during treadmill running.


# Summary
During the aerial phase of running, the body exerts no force on the ground. 
I assume any substantial forces measured by the instrumented treadmill during an aerial phase are due to signal drift.
`dryft` implements a stepwise approach that zeros each step separately by subtracting the mean of the aerial phases 
before and after a step, represented by:

$$S_n = D_n - \frac{A_n + A_{n+1}}{2}$$

Where $n$ is a given step, $A$ is the mean vertical GRF during the aerial phase, $D$ is the drifting signal 
signal, and $S$ is the returned signal with drift removed. 
This process is repeated for all steps present in a trial, with drift of the first and last step in a trial estimated from 
only one adjacent aerial phase.

I generated a drifting signal by adding a sine wave (amplitude: 100 N, wavelength: 30 s) to a 
30-second vGRF signal collected by an instrumented signal available from Fukuchi et al. (2017).
Figure 2 illustrates the improvement in mean aerial phase values when using `dryft` to correct the signal’s drift.
`dryft` can be repeatedly implemented to further reduce signal drift, although substantial improvements are
observed with a single use.

![Figure 2](mean_aerial_phases.png)
*Figure 2. Vertical ground reaction forces (top) and mean aerial phase values (bottom) before (blue dots) and after 
(red dots) using `dryft` to correct for signal drift.*  

The primary application of the `dryft` package is to remove signal drift in GRF signals produced during treadmill running, 
but one of its supporting functions, `signal.splitsteps()` may also be useful to biomechanical researchers.
`signal.splitsteps()` provides a fast and robust method for identifying initial contact and toe-off within a 
vertical GRF signal. 
Once identified, these events can used to calculate commonly investigated stride kinematic variables like contact time, 
leg swing time, step time, step length, or step frequency.

# Acknowledgements

The author would like to thank MRP for their support as well as GB and 
[/r/learnpython](https://reddit.com/r/learnpython) for their feedback during package development. 

# References