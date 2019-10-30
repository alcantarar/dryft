# `dryft`
#### Created by [Ryan Alcantara](https://alcantarar.github.io)

`dryft` is an open-source Python package that corrects running ground reaction force (GRF) 
signal drift. This package was developed for biomechanical researchers using force plates
or a force-measuring treadmill to collect an individual's GRF during running. Due to the
prevalence of MATLAB in the field of Biomechanics, I have also developed a [set of 
MATLAB functions](MATLAB) that operate like the Python package. However, this readme will 
focus on the use of the Python package.

## Table of Contents
* [Dependencies](#dependencies)
* [Recommended Installation](#recommended-installation)
* [How `dryft` Works](#how-dryft-works)
* [Using `dryft`](#using-dryft)
* [Contributing](#contributing)
* [Licensing](#licensing)

## Dependencies
This package was designed to work with and was tested with Python 3.6.7. 
Other python 3.X versions may be supported, provided dependency compatibilities and requirements are met.

The package requires the following dependencies: 
* numpy
* pandas
* matplotlib
* scipy

## Recommended Installation

I recommend using the [Anaconda](https://www.anaconda.com/distribution/#download-section) to setup a Python 3.6.7 
environment to use this package. If you wish to setup a new environment, an Anaconda [environment](environment.yml) 
file is included to automatically install most dependencies. To setup a new environment for `dryft`, type the following 
command into Anaconda Prompt:
```
conda env create -f path\to\environment.yml
```
This will create a new environment named `dryft-env`, which can be actived by typing:
```
conda activate dryft-env
```
Once the environment is setup and activated, `dryft` can be installed by cloning/downloading
this repository and then running:
```
python setup.py install
```

## How `dryft` works
Running is generally characterized by two phases: a stance and aerial phase. Only one foot is on the ground at a time during 
stance phase and both feet are off the ground during aerial phase. The force exerted by the body on the ground during 
aerial phase is zero and during stance phase it is greater than zero. If drift is present in the force signal, values 
during the aerial phase will no longer be zero. `dryft` uses the aerial phase before and after a given step to tare the 
force signal during that step. Specifically, it subtracts the mean between the two aerial phases from the step contained
 between the aerial phases. This effectively corrects for signal drift in a step-wise manner. A similar method is 
 described by [Paolini *et al.* (2007)](https://www.ncbi.nlm.nih.gov/pubmed/16759895), but no details on the software
 routine is provided. The `dryft` package differs from currently available signal correction methods, which can only 
 account for [linear drift](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.detrend.html) 
or an [offset](https://www.c-motion.com/v3dwiki/index.php/FP_ZERO).


## Using `dryft`
### Documentation
Please refer to the [API Documentation](https://alcantarar.github.io/dryft/index.html)
### Example
The following tutorial and its supporting documents is found in `setup.py`located in [sample](sample)
#### Read force signal data
The three-dimensional force data modified from [Fukuchi *et al* (2017)](https://peerj.com/articles/3298/). There is a sine wave
with an amplitude of 100 Newtons and wavelength equal to trial length added to the force signal. 
```
from dryft import signal, plot
import pandas as pd
from scipy.signal import butter, filtfilt

GRF = pd.read_csv('drifting_forces.txt', header=None)
```
#### Filter signal
Filtering data will improve step identification methods. Here I apply a zero-lag 4th order butterworth
filter with a 60Hz cutoff.
```
# Apply Butterworth Filter
Fs = 600
Fc = 60
Fn = (Fs / 2)
b,a = butter(2, Fc/Fn)
GRF_filt = filtfilt(b, a, GRF, axis=0)  # filtfilt doubles order (2nd*2 = 4th order effect)
```

#### Identify where stance and aerial phases occur
Note the unusually high force threshold to define a step. This will depend upon the amount of
drift present in your signal. `GRF_filt[:,2]` is the vertical component of the ground reaction
 force signal (vGRF) and has an artificial drift of 100 Newtons, so a threshold of 110 Newtons 
 will suffice for separating steps.

```
# stance phase
step_begin, step_end = signal.splitsteps(vGRF=GRF_filt[:,2],
                                  threshold=110,
                                  Fs=300,
                                  min_tc=0.2,
                                  max_tc=0.4,
                                  plot=False)
# plot stance phases
plot.stance(GRF_filt[:,2], step_begin, step_end)

# aerial phase
aerial_begin_all = step_end[:-1]
aerial_end_all = step_begin[1:]
print('Number of aerial begin/end:', aerial_begin_all.shape[0], aerial_end_all.shape[0])
```
#### Determine average force signal during aerial phase
To calculate the force measured during aerial phase, the beginning and end of each 
aerial phase must be ignored. This provides a better sense of what the true force value
is during aerial phase.
```
# trim beginning/end of aerial phase prior to calculation of mean
trim = signal.trimaerial(GRF_filt[:,2], step_begin, step_end)
aerial_means = signal.meanaerialforce(GRF_filt[:,2], step_begin, step_end, trim ) #aerial_means will be same width as GRF_filt

# plot aerial phases
plot.aerial(GRF_filt[:,2], aerial_means, aerial_begin_all, aerial_end_all, trim) #aerial_means and GRF_filt must be (n,) arrays
```
#### Remove force signal drift
This is performed on a per-step basis.
```
force_fd, aerial_means_d = signal.detrend(GRF_filt[:,2],
                                          Fs,
                                          aerial_means,
                                          step_begin,
                                          step_end,
                                          trim,
                                          plot=True) #grf_filt and aerial_means must be same width
 
```
## Contributing

To report an problem with `dryft`, please create a new [issue](https://github.com/alcantarar/dryft/issues).

Contact [alcantarar](https://github.com/alcantarar) with any support or general questions about `dryft`. I also welcome
meaningful contributions via [pull requests](https://github.com/alcantarar/dryft/pulls).

## Licensing

This package is licensed under the MIT License. Copyright 2019 [Ryan Alcantara](https://alcantarar.github.io).
