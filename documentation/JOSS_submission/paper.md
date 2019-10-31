---
title: 'Dryft: Python and MATLAB packages to correct drifting ground reaction force signals'
tags:
  - running
  - biomechanics
  - drift
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
Ground reaction forces (GRFs) are the force exerted by the body on the ground during activities like walking and running. 
GRFs are clinically relevant and commonly measured in biomechanics.
To collect GRFs more easily, researchers use force plates and treadmills instrumented with force transducers.
Instrumented treadmills are special though, because they allow for the measurement of GRFs over long periods of time. 
However, force signals can be affected by changes in temperature or signal amplifiers, causing the signal to drift over time.
Signal drift, if ignored, can result in the loss of data if GRFs exceed the range of the force transducer. 

Even if a GRF signal does not exceed the range of the transducer, drift can still result in inaccurate data.
For example, signal drift can have additive effects on the measurement of stride kinematics like contact time during 
running. 
Contact time is the time the foot is in contact with the ground and is often defined as the duration when the vertical 
GRF is above a threshold.  
Signal drift can cause an increasing (or decreasing) amount of the vertical GRF signal to fall below the threshold, 
artificially increasing the variation in contact time or other time-dependent biomechanical variables (Figure 1).

![Figure 1](Figure_1.png)
*Figure 1. Vertical ground reaction force signal where signal drifts positively 100 Newtons. 
Contact time increases by ~0.04s, or ~17%.* 
 
To combat signal drift, it is best practice to zero the force transducer signal between trials during data collection. 
This must be done when no force is being applied to the force transducers to ensure accurate signals.
However, zeroing of force transducers may not be feasible for protocols requiring extended periods of continuous
running on an instrumented treadmill, causing GRF signals to drift over time.
There are signal processing methods available to remove offsets [v3d] and linear drift [scipy/matlab detrend], but 
drift in GRF signals is not guaranteed to be linear. 
Here, I introduce `dryft`, a Python and MATLAB package that takes a stepwise approach to removing non-linear drift in 
the GRF signal of a person during running.


# Summary
During the aerial phase of running, the body is exerting no force on the ground. 
I assume any substantial forces measured by the instrumented treadmill during an aerial phase are due to signal drift. 
`dryft` implements a stepwise approach that tares each step individually by subtracting the mean of the aerial phase 
directly before and after a step, represented by:

$$S_n = D_n - \frac{A_n + A_{n+1}}{2}$$

Where $n$ is a given step, $A$ is the mean vertical GRF during the aerial phase, $D$ is the drifting signal 
signal, and $S$ is the returned signal with drift removed. 
This process is repeated for all steps present in a trial, with drift of the first and last step estimated from 
an adjacent step. Figure 2 illustrates the change in aerial phase values using this method.

![Figure 2](mean_aerial_phases.png)
*Figure 2. Mean aerial phase vertical ground reaction force for 78 steps before (blue dots) and after (red dots) 
correcting for signal drift. `dryft` brings aerial phase values closer to zero and works on positive and 
negative drift across a range of slopes.*  

# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

# Acknowledgements

The author would like to thank MRP for their support as well as GB and 
[/r/learnpython](https://reddit.com/r/learnpython) for their feedback during package development. 

# References