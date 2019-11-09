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
GRF = dlmread('drifting_forces.txt');

%% Apply Butterworth filter
Fs = 300; % From Fukuchi et al. (2017) dataset
Fc = 60;
Fn = (Fs/2);
[b, a] = butter(2, Fc/Fn);

GRF_filt = filtfilt(b, a, GRF);

%% Identify where stance phase occurs (foot on ground)
[stance_begin,stance_end] = split_steps(GRF_filt(:,3),... %vertical GRF
    110,... %threshold
    Fs,... %Sampling Frequency
    0.2,... %min_tc
    0.4,... %max_tc
    0); %(d)isplay plots = True

%% Identify where aerial phase occurs (feet not on ground)                                
% Determine force signal during middle of aerial phase.
[aerial_vals, aerial_loc] = aerial_force(GRF_filt(:,3), stance_begin, stance_end);
plot_aerial(GRF_filt(:,3), aerial_vals, aerial_loc, stance_begin, stance_end)

%% Subtract aerial phase to remove drift
vGRF_detrend = detrend(GRF_filt(:,3), aerial_vals, aerial_loc);

%% Plot results
% 
% if d
%     figure
%     subplot(2,1,1)
%     hold on
%     plot(linspace(0,length(force_fd)/Fs, length(force_fd)), force_f,'b')
%     plot(linspace(0,length(force_fd)/Fs, length(force_fd)), force_fd,'r')
%     grid on
%     legend({'original signal', 'detrended signal'})
%     xlabel('time')
%     ylabel('force')
% end    
% 
% %calculate mean aerial phase for detrend data
% aerial_means_d = mean_aerial_force(force_fd, stance_begin, stance_end, trim);
% 
% % i = 1;
% % while i < min([length(step_begin), length(step_end)])
% %     aerial_mean_d(i,t_num) = mean(force_fd(aerial_begin(i)+trim:aerial_end(i)-trim,t_num));
% %     i = i+1;
% % end
% % aerial_mean_d(i,t_num) = mean(force_fd(aerial_begin(i-1)+trim:aerial_end(i-1)-trim,t_num)); %repeat last one
% 
% if d
%     subplot(2,1,2)
%     hold on
%     for i = 1:length(aerial_means)
%         plot(i, aerial_means(i), 'b.')
%         plot(i, aerial_means_d(i), 'r.')
%     end
%     legend({'original signal', 'detrended signal'})
%     grid on
%     title('mean of aerial phase')
%     xlabel('steps')
%     ylabel('force')
% end
% 
