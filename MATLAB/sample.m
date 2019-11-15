%Script corrects force signal drift in a step-specific manner. Subtracts
%mean of aerial phase before and after each step for whole trial.
%
%   Calls on the following functions:
%   split_steps.m
%   trim_aerial.m
%   aerial_force.m
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
GRF = dlmread('custom_drift_S001runT25.csv');

%% Apply Butterworth filter
Fs = 300; % From Fukuchi et al. (2017) dataset
Fc = 50;
Fn = (Fs/2);
[b, a] = butter(2, Fc/Fn);

GRF_filt = filtfilt(b, a, GRF);

%% Identify where stance phase occurs (foot on ground)
[stance_begin,stance_end, good_stances] = split_steps(GRF_filt,... %vertical GRF
    140,... %threshold
    Fs,... %Sampling Frequency
    0.2,... %min_tc
    0.4,... %max_tc
    0); %(d)isplay plots = True

%% Identify where aerial phase occurs (feet not on ground)
% Determine force signal during middle of aerial phase.
[aerial_vals, aerial_loc] = aerial_force(GRF_filt, stance_begin, stance_end, good_stances);
plot_aerial(GRF_filt, aerial_vals, aerial_loc, stance_begin, stance_end, good_stances)

%% Subtract aerial phase to remove drift
vGRF_detrend = detrend(GRF_filt, aerial_vals, aerial_loc);

%% Compare original to detrended signal

% Split steps BUT WITH A LOWER STEP THRESHOLD. GO AS LOW AS YOU CAN.
[stance_begin_d,stance_end_d, good_stances_d] = split_steps(vGRF_detrend, 25, Fs, 0.2, 0.4, 0);
%calculate force at middle of aerial phase
[aerial_vals_d, aerial_loc_d] = aerial_force(vGRF_detrend, stance_begin_d, stance_end_d, good_stances_d);

% Plot original vs detrended signal
figure
% plot waveforms
subplot(2,1,1)
hold on
plot(linspace(0,length(GRF_filt)/Fs, length(GRF_filt)), GRF_filt,'b')
plot(linspace(0,length(vGRF_detrend)/Fs, length(vGRF_detrend)), vGRF_detrend,'r')
grid on
legend({'original signal', 'detrended signal'})
title('Entire Trial')
xlabel('Time [s]')
ylabel('Force [N]')
% plot aerial phases
subplot(2,1,2)
hold on
plot(aerial_loc, aerial_vals, 'b.')
plot(aerial_loc_d, aerial_vals_d, 'r.')
legend({'original signal', 'detrended signal'})
grid on
title('Aerial phases')
xlabel('Frame')
ylabel('Force [N]')

