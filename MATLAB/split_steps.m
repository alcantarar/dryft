function [step_begin,step_end] = split_steps(force_f,threshold, Fs_force, min_tc, max_tc, d)
%STEP_ID_RA reads in FILTERED running ground reaction force data and splits steps based on a force threshold.
% %
%   Author: Ryan Alcantara || ryan.alcantara@colorado.edu || github.com/alcantarar
%
%   INPUTS
%   -------------
%   force_f :   Nx1 array of FILTERED vertical GRF data.
%   threshold : Threshold used to define heel-strike and toe-off. Please be responsible and set < 50N.
%   Fs_force :  Sampling Frequency of force signal
%   min_tc :    Min Contact Time - Minimum duration (s) the step ID algorithm will consider 1 stance phase. Jogging should be > 0.2s.
%   max_tc :    Max Contact Time - Maximum duration (s) the step ID algorithm will consider 1 stance phase. Jogging should be < 0.4s.
%   d :         Binary (1 or 0) argument for displaying plots.
%
%   OUTPUTS
%   -------------
%   step_begin :  Array of frame indexes for beginning of stance phase
%   step_end :    Array of frame indexes for end of stance phase
%
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
%   [step_begin,step_end, step_len] = step_ID_RA(force_f,threshold, Fs_force min_tc, max_tc, d)
%
if max_tc < min_tc
    error('max_tc must be greater than min_tc')
end

compare = force_f > threshold; %every data point that is over the threshold
events = diff(compare); % either x2-x1 = 0-1 = -1 (end of step) or x2-x1 = 1-0 = 1 (beginning of step)
step_begin.all = find(events == 1); %index of step begin
step_end.all = find(events == -1); %index of step end

if d
    %check steps if needed
    figure(2)
    hold on
    plot(force_f,'LineWidth',1)
    plot(events*max(force_f)/2,'-k','Linewidth',1) %start & stop
    grid on
    hold off
end

%if trial starts with end of step, 
%ignore it so that trial starts with first whole step
step_end.keep = step_end.all(step_end.all > step_begin.all(1)); 
step_begin.keep = step_begin.all(1:length(step_end.keep));
%above compare indexes from begin #1 to every step end index, keep if end > begin is true

%remove steps that are too short (not full step @ end of trial
min_tc = min_tc*Fs_force;
max_tc = max_tc*Fs_force;

%calculate step length and compare to min step length
step_len = step_end.keep - step_begin.keep;
good_step1 = step_len >= min_tc; %which steps meet minimum length req
good_step2 = step_len <= max_tc; %which steps meet max length req
good_step = (good_step1 + good_step2 == 2);

step_begin = step_begin.keep(good_step); %take those steps' beginnings
step_end = step_end.keep(good_step); %take those steps' ends

disp(['Number of contact time begin/ends: ', num2str(length(step_begin)), '/', num2str(length(step_end))])

end


