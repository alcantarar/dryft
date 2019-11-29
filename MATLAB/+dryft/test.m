%% split_steps
GRF = dlmread('custom_drift_S001runT25.csv'); %REQUIRES UPDATE TO: 'path/to/dryft/MATLAB' in sample.m
GRF = GRF(2001:2500);
%filter
Fs = 300; % From Fukuchi et al. (2017) dataset
Fc = 50;
Fn = (Fs/2);
n_pass = 2;
order = 2;
C = (2^(1/n_pass)-1)^(1/(2*order)); % Correction factor per Research Methods in Biomechanics (2e) pg 288
Wn = (tan(pi*Fc/Fs))/C; % Apply correction factor to adjusted cutoff freq
Fc_corrected = atan(Wn)*Fs/pi; % Hz
[b, a] = butter(order, Fc_corrected/Fn);

GRF_filt = filtfilt(b, a, GRF);
%test
[stance_begin,stance_end, good_stances] = dryft.split_steps(GRF_filt,... %vertical GRF
    140,... %threshold
    Fs,... %Sampling Frequency
    0.2,... %min_tc
    0.4,... %max_tc
    0); %(d)isplay plots = True

assert(stance_begin(1) == 69)
assert(stance_end(1) == 148)
assert(sum(good_stances) == 4)

%% aerial_force
stance_begin = [10,35];
stance_end = [20,40];
good_stances = logical([1,1]);
sig = 1:3:100;
[aerial_vals, aerial_loc] = dryft.aerial_force(sig, stance_begin, stance_end, good_stances);

assert(aerial_vals == 82)
assert(aerial_loc == 28)
%% plot_aerial
sig = 1:3:1000;
aerial_vals = 82;
aerial_loc = 28;
stance_begin = [10,35];
stance_end = [20,40];
good_stances = logical([1,1]);
close all
dryft.plot_aerial(sig, aerial_vals, aerial_loc, stance_begin, stance_end, good_stances);
assert(ishandle(1) == 1)
close(1)

%% detrend
sig = 100:3:1000;
sig = sig';
aerial_vals = [82;100];
aerial_loc = [28;68];
vGRF_detrend = dryft.detrend(sig, aerial_vals, aerial_loc);

assert(size(vGRF_detrend,1) == 301)
assert(size(vGRF_detrend,2) == 1)