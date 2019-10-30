# Dryft
##### Created by [Ryan Alcantara](https://alcantarar.github.io)

Dryft is an open-source Python package that corrects running ground reaction force (GRF) 
signal drift. This package was developed for biomechanical researchers using force plates
or a force-measuring treadmill to collect an individual's GRF during running. Due to the
unfortunate prevalence of MATLAB in the field of Biomechanics, I have also developed a set of 
[MATLAB functions](dryft/MATLAB) that operate like the Python package.

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
This library was created in an effort to correct any drift in a force-measuring 
treadmill or force plate signal when someone is running on it. When running, a 
person has only 1 foot on the ground at a time, with an aerial phase inbetween each step. 
Here, I assume that the force measured by the treadmill during any given aerial phase should be zero, 
and use the aerial phases before and after a given step to tare the force signal. This will 
effectively correct for drift in the signal step-wise manner. 

The python library was developed first and has been tested . A MATLAB version was
created afterwards as it is a common language used in the field of biomechanics.

## Using dryft
