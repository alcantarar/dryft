%Script corrects force signal drift in a step-specific manner. Subtracts 
%mean of aerial phase before and after each step for whole trial.
%
%   Calls on the following functions: 
%   split_steps.m
%   trim_aerial.m
%   mean_aerial_force.m
%   plot_aerial.m (optional)
%   detrend.m
%
%   Relies on this modified dataset from Fukuchi et al. (2017):
%   drifting_forces.txt
%
%   Author: Ryan Alcantara | ryan.alcantara@colorado.edu | github.com/alcantarar/dryft
%   License: MIT (c) 2019 Ryan Alcantara
%   Distributed as part of [dryft] | github.com/alcantarar/dryft

%% Read in data from force plate
clear
close
GRF = dlmread('drifting_forces.txt');

%% Apply Butterworth filter
Fs = 300; % From Fukuchi et al. (2017) dataset
Fc = 60;
Fn = (Fs/2);
[b, a] = butter(2, Fc/Fn);

GRF_filt = filtfilt(b, a, GRF);

%% Identify where stance phase occurs (foot on ground)
[step_begin,step_end] = split_steps(GRF_filt(:,3),... %vertical GRF
    110,... %threshold
    Fs,... %Sampling Frequency
    0.2,... %min_tc
    0.4,... %max_tc
    1); %(d)isplay plots = True

%% Identify where aerial phase occurs (feet not on ground)                                
aerial_begin =  step_end(1:end-1);
aerial_end = step_begin(2:end);

% Determine average force signal during aerial phase.
% Must trim beginning and end of aerial phase to get true aerial phase
% value. Filtering smooths out rapid transitions at start/end.
trim = trim_aerial(GRF_filt(:,3), step_begin, step_end);                         
aerial_means = mean_aerial_force(GRF_filt(:,3), step_begin, step_end, trim);
plot_aerial(GRF_filt(:,3), aerial_means, aerial_begin, aerial_end, trim)

%% Subtract aerial phase to remove drift
[vGRF_detrend, aerial_means_detrend] = detrend(GRF_filt(:,3),... %nx1 force array
    Fs,... %force sampling frequency
    aerial_means,... %mean force during aerial phase
    step_begin,... %tc_begin
    step_end,... %tc_end
    trim,... %trim off beginning and end of aerial phase
    1); %(d)isplay plots = True
