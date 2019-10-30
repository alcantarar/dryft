function [force_fd,aerial_means_d] = detrend(force_f, Fs, aerial_means, step_begin, step_end, trim, d)
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here


force_fd = NaN(size(force_f));
aerial_begin = step_end(1:end-1);
aerial_end = step_begin(2:end);

%first step, extend from beginning of trial
i = 1;
diff_temp = (aerial_means(i)+aerial_means(i+1))/2; %mean of aerial phaes before/after given step (i)
diff_vals(i) = diff_temp; %hang onto value subtracted from each step
force_fd(1:step_begin(i+1)) = force_f(1:step_begin(i+1)) - diff_temp;
%2:n-1 steps
i = 2;
while i < min([length(step_begin), length(step_end)]) -1
    diff_temp = (aerial_means(i)+aerial_means(i+1))/2; %mean of aerial phaes before/after given step (i)
    diff_vals(i) = diff_temp; %hang onto value subtracted from each step
    force_fd(step_begin(i):step_begin(i+1)) = force_f(step_begin(i):step_begin(i+1)) - diff_temp;
    i = i+1;
end
%last step, extend to end of file
diff_temp = (aerial_means(i-1)+aerial_means(i))/2; %mean of aerial phaes before/after given step (i)
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
for i = 1:length(aerial_begin)
    aerial_means_d(i) = mean(force_fd(aerial_begin(i)+trim:aerial_end(i)-trim));
end
aerial_means_d = aerial_means_d(aerial_means_d ~=0.0);

% i = 1;
% while i < min([length(step_begin), length(step_end)])
%     aerial_mean_d(i,t_num) = mean(force_fd(aerial_begin(i)+trim:aerial_end(i)-trim,t_num));
%     i = i+1;
% end
% aerial_mean_d(i,t_num) = mean(force_fd(aerial_begin(i-1)+trim:aerial_end(i-1)-trim,t_num)); %repeat last one

if d
    subplot(2,1,2)
    hold on
    for i = 1:length(aerial_means)-1
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
