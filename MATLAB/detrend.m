function [force_fd,aerial_means_d] = detrend(force_f, Fs, aerial_means, step_begin, step_end, trim, d)
%DETREND Removes linear or non-linear drift from running ground reaction
%force data in a stepwise manner.
%   INPUT
%   -----
%   force_f: nx1 array containing force signal to be detrended
%   Fs: Sampling frequency of force signal
%   aerial_means: mean force signal for aerial phase. Output from
%       [trim_aerial.m].
%   step_begin: array of frames for initial contact. Output from
%       [split_steps.m].
%   step_end: array of frames for toe-off. Output from [split_steps.m]
%   trim: number of frames to trim from beginning/end of aerial phase.
%       Output from [trim_aerial.m].
%   d: binary argument to display plots. Helpful for troubleshooting.
%
%   OUTPUT
%   ------
%   force_fd: detrended force signal
%   aerial_means_d: means of aerial phase for detrended signal. Should be
%       close to zero. May be able to apply [detrend.m] multiple times if
%       signal not detrended enough (NOT TESTED).
%
%   Author: Ryan Alcantara | ryan.alcantara@colorado.edu 
%   License: MIT (c) 2019 Ryan Alcantara
%   Distributed as part of [dryft] | github.com/alcantarar/dryft

force_fd = NaN(size(force_f));
aerial_begin = step_end(1:end-1);
aerial_end = step_begin(2:end);

%first step, extend from beginning of trial
i = 1;
diff_temp = aerial_means(i); %mean of aerial phase after first step guranteed to be there
diff_vals(i) = diff_temp; %hang onto value subtracted from each step
force_fd(1:step_begin(i+1)) = force_f(1:step_begin(i+1)) - diff_temp;
%2:n-1 steps
i = 2;
while i < min([length(step_begin), length(step_end)])
    diff_temp = (aerial_means(i-1)+aerial_means(i))/2; %mean of aerial phaes before/after given step (i)
    diff_vals(i) = diff_temp; %hang onto value subtracted from each step
    force_fd(step_begin(i):step_begin(i+1)) = force_f(step_begin(i):step_begin(i+1)) - diff_temp;
    i = i+1;
end
%last step, extend to end of file
diff_temp = aerial_means(i-1); %mean of aerial phaes before last step
diff_vals(i) = diff_temp; %hang onto value subtracted from each step
force_fd(step_begin(i):end) = force_f(step_begin(i):end) - diff_temp;

if d
    figure
    subplot(2,1,1)
    hold on
    plot(linspace(0,length(force_fd)/Fs, length(force_fd)), force_f,'b')
    plot(linspace(0,length(force_fd)/Fs, length(force_fd)), force_fd,'r')
    grid on
    legend({'original signal', 'detrended signal'})
    xlabel('time')
    ylabel('force')
end    

%calculate mean aerial phase for detrend data
aerial_means_d = mean_aerial_force(force_fd, step_begin, step_end, trim);

% i = 1;
% while i < min([length(step_begin), length(step_end)])
%     aerial_mean_d(i,t_num) = mean(force_fd(aerial_begin(i)+trim:aerial_end(i)-trim,t_num));
%     i = i+1;
% end
% aerial_mean_d(i,t_num) = mean(force_fd(aerial_begin(i-1)+trim:aerial_end(i-1)-trim,t_num)); %repeat last one

if d
    subplot(2,1,2)
    hold on
    for i = 1:length(aerial_means)
        plot(i, aerial_means(i), 'b.')
        plot(i, aerial_means_d(i), 'r.')
    end
    legend({'original signal', 'detrended signal'})
    grid on
    title('mean of aerial phase')
    xlabel('steps')
    ylabel('force')
end
end

