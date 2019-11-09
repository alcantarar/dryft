function [stance_begin,stance_end] = split_steps(force_f,threshold, Fs_force, min_tc, max_tc, d)
%SPLIT_STEPS reads in FILTERED running ground reaction force data and 
%identifies stance phase beginning/end based on a force threshold.
%
%   Author: Ryan Alcantara | ryan.alcantara@colorado.edu | github.com/alcantarar/dryft
%   License: MIT (c) 2019 Ryan Alcantara
%   Distributed as part of [dryft] | github.com/alcantarar/dryft
%
%   INPUTS
%   -------------
%   force_f :   Nx1 array of FILTERED vertical GRF data.
%   threshold : Threshold used to define heel-strike and toe-off. Please be responsible and set < 30N.
%   Fs_force :  Sampling Frequency of force signal
%   min_tc :    Min Contact Time - Minimum duration (s) the step ID algorithm will consider 1 stance phase. Jogging should be > 0.2s.
%   max_tc :    Max Contact Time - Maximum duration (s) the step ID algorithm will consider 1 stance phase. Jogging should be < 0.4s.
%   d :         Binary (1 or 0) argument for displaying plots.
%
%   OUTPUTS
%   -------------
%   stance_begin :  Array of frame indexes for beginning of stance phase
%   stance_end :    Array of frame indexes for end of stance phase
%
%   EXAMPLE
%   -------------
%   % design and apply lowpass butterworth filter (4th order)
%   Fn = Fs_force/2;
%   Fc = 15;
%   [b,a] = butter(2, Fc/Fn);
%   force_f = filtfilt(b,a,GRF);
%
%   % ID steps
%   threshold = 20; %Newtons
%   min_tc = 0.2; %seconds
%   max_tc = 0.4; %seconds
%   d = 1; 
%   [stance_begin,stance_end] = split_steps(force_f,threshold, Fs, min_tc, max_tc, d)
%
if max_tc < min_tc
    error('max_tc must be greater than min_tc')
end

compare = force_f > threshold; %every data point that is over the threshold
events = diff(compare); % either x2-x1 = 0-1 = -1 (end of step) or x2-x1 = 1-0 = 1 (beginning of step)
stance_begin.all = find(events == 1); %index of stance phase begin
stance_end.all = find(events == -1); %index of stance phase end

if d
    %check steps if needed
    figure(2)
    hold on
    plot(force_f,'LineWidth',1)
    plot(events*max(force_f)/2,'-k','Linewidth',1) %start & stop
    grid on
    hold off
end

%if trial starts with end of stance phase, 
%ignore it so that trial starts with first whole stance phase
stance_end.keep = stance_end.all(stance_end.all > stance_begin.all(1)); 
stance_begin.keep = stance_begin.all(1:length(stance_end.keep));
%above compare indexes from begin #1 to every stance phase end index, keep if end > begin is true

%remove stance phases that are too short (not full step @ end of trial
min_tc = min_tc*Fs_force;
max_tc = max_tc*Fs_force;

%calculate stance phase duration (frames) and compare to min step length
step_len = stance_end.keep - stance_begin.keep;
good_step1 = step_len >= min_tc; %which stance phases meet minimum length req
good_step2 = step_len <= max_tc; %which stance phases meet max length req
good_step = (good_step1 + good_step2 == 2);

stance_begin = stance_begin.keep(good_step); %take those stance phases' beginnings
stance_end = stance_end.keep(good_step); %take those stance phases' ends

disp(['Number of stance phase begin/ends: ', num2str(length(stance_begin)), '/', num2str(length(stance_end))])

end


