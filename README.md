# Dryft
##### Created by [Ryan Alcantara](https://alcantarar.github.io)

Dryft is an open-source Python package that corrects running ground reaction force (GRF) 
signal drift. This package was developed for biomechanical researchers using force plates
or a force-measuring treadmill to collect an individual's GRF during running. Due to the
prevalence of MATLAB in the field of Biomechanics, I have also developed a [set of 
MATLAB functions](MATLAB) that operate like the Python package. However, this readme will 
focus on the use of the Python package.

## Dependencies
This package was designed to work with and was tested with Python 3.6.7. 
Other python 3.X versions may be supported, provided dependency compatibilities and requirements are met.

The package requires the following dependencies: 
* numpy
* pandas
* matplotlib
* scipy

## Recommended Installation

I recommend using the [Anaconda](https://www.anaconda.com/distribution/#download-section) to setup a Python 3.6.7 environment to use this package.
If you wish to setup a new environment, an Anaconda [environment](environment.yml) file is included
to automatically install most dependencies. To setup a new environment for Dryft, type the following 
command into Anaconda Prompt:
```
conda env create -f path\to\environment.yml
```
This will create a new environment named `dryft-env`, which can be actived by typing:
```
conda activate dryft-env
```
Once the environment is setup and activated, dryft can be installed by cloning/downloading
this repository and then running:
```
python setup.py install
```

## How dryft works
Running is generally characterized by two phases*. There is a "stance phase" where only one foot is on the ground 
at a time, and an "aerial phase" where both feet are off the ground. The force exerted by the body on the ground during 
aerial phase is zero and it is greater than zero during stance phase. Force plates and instrumented treadmills can 
measure this force exerted on the ground in three dimensions; this is the ground reaction force (GRF).

If there is drift in the GRF signal measured by the force plate, forces during the aerial phase will no longer be zero.
Dryft uses the aerial phases before and after a given step to tare the force signal during that step. Specifically, it 
subtracts the mean between the two aerial phases from the step contained between the aerial phases. This effectively 
corrects for signal drift in a step-wise manner. Dryft differs from current signal correction methods, which can 
only account for [linear drift](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.detrend.html) or an 
[offset](https://www.c-motion.com/v3dwiki/index.php/FP_ZERO). 

**[Groucho Running](https://www.ncbi.nlm.nih.gov/pubmed/3610929) is an exception* 
## Using dryft
