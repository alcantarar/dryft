# `dryft` for MATLAB
#### Created by [Ryan Alcantara](https://alcantarar.github.io)
While `dryft` is a Python package, I made a MATLAB version because many biomechanical researchers only know how to use
MATLAB :disappointed:. Here is a quick overview of how to use the `dryft` MATLAB code. Open an [issue](https://github.com/alcantarar/dryft/issues) 
if there are problems or better yet, contribute code via a [pull requests](https://github.com/alcantarar/dryft/pulls) 
to improve this MATLAB version! 

## Using the MATLAB version of `dryft`
#### Download package
Download zipped repository or clone with git:
```
git clone https://github.com/alcantarar/dryft.git
cd dryft/MATLAB
```
#### Add `dryft` to MATLAB path
The `dryft/MATLAB/` directory contains the MATLAB version of the `dryft` package in `/+dryft`, a `README.md`, and the following 
supporting files:
* `sample.m` (example script calling functions in the `dryft` package)
* `custom_drift_S001runT25.csv` (force data from [Fukuchi et al. (2017)](https://peerj.com/articles/3298/) that was
modified to have drift)

Next, open up `sample.m` and add `dryft` to your MATLAB path by updating `path/to/dryft/MALTAB/`:
```
addpath("path/to/dryft/MATLAB/");
savepath(); %optional, saves path/to/dryft/MATLAB/ to your MATLABPATH permanently
```

Consult the [MATLAB documentation](https://www.mathworks.com/help/matlab/ref/addpath.html) for 
more information on adding directories to your MATLAB path. To confirm that the `dryft`
package is in your path, run `help detrend` in the MATLAB command window. If it returns `dryft not found.`,
then it was not successfully added to your MATLAB path. Make sure the location of `dryft/MATLAB` is listed 
correctly when you run `path` in the MATLAB command window.

####  Example of `dryft` use
The `sample.m` script serves as a tutorial, using the `custom_drift_S001runT25.csv` as an example vertical ground reaction force trial.

## Licensing

This is distributed as part of `dryft`, which is licensed under the MIT License. 
Copyright 2019 [Ryan Alcantara](https://alcantarar.github.io).
