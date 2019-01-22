%Program detrends force signal in a step-specific manner.Subtracts mean of
%aerial phase before and after given step across whole trial.
%Inputs: location of data_v (volts from HighSpeed Treadmill),
% line 52 (signal to detrend), and line 131 if needed (amount to trim off 
% the beginning and end of aerial phase).

%Outputs: crap ton of plots and data_detrend variable
%Created by: Ryan Alcantara - ryan.alcantara@colorado.edu

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clearvars
close all
clc
%first import voltages (xyz*4 transducers = 12 channels)
[filename pathname] = uigetfile('*.*')
data_v = load([pathname filename]); %zero indexed, matches Nexus output
data_v = data_v(:,1:12); %trim any EMG signals at end of file

%% convert to newtons and filter. CALMAT is specific to HighSpeed Treadmill. DO NOT CHANGE.
calmat = [...
    -36.5075 0 0 0 0 0 0 0 0 0 0 0;...
    0 -36.3925 0 0 0 0 0 0 0 0 0 0;...
    0 0 142.454 0 0 0 0 0 0 0 0 0;...
    0 0 0 36.4102 0 0 0 0 0 0 0 0;...
    0 0 0 0 36.2167 0 0 0 0 0 0 0;...
    0 0 0 0 0 143.057 0 0 0 0 0 0;...
    0 0 0 0 0 0 36.3198 0 0 0 0 0;...
    0 0 0 0 0 0 0 36.4503 0 0 0 0;...
    0 0 0 0 0 0 0 0 143.061 0 0 0;...
    0 0 0 0 0 0 0 0 0 -36.3428 0 0;...
    0 0 0 0 0 0 0 0 0 0 -36.4966 0;...
    0 0 0 0 0 0 0 0 0 0 0 143.414]; %from v3d calibration matrix pipeline
%apply matrix
data_n = data_v*calmat;
%sum transducers
summed_force(:,1) = data_n(:,2)+data_n(:,5)+data_n(:,8)+data_n(:,11); %x
summed_force(:,2) = data_n(:,1)+data_n(:,4)+data_n(:,7)+data_n(:,10); %y
summed_force(:,3) = data_n(:,3)+data_n(:,6)+data_n(:,9)+data_n(:,12); %z
% simple filter
Fs_force = 1000;
Fc_force = 30;
fn = (Fs_force/2);
[b a] = butter(4,Fc_force/fn);
summed_force_f = filtfilt(b,a,summed_force);
data_n_f = filtfilt(b,a,data_n);
%% chose signal to detrend. 
%Options:
% -> data_n is unfiltered transducer in newtons.
% -> data_n_f is filtered transducer in newtons.
% -> data_v is raw voltage
% -> summed_force_f is sum of transducers, filtered, in newtons
data_drift = data_n_f;

%% visualize drift and filter for each transducer and compare to summed force. Force cancels -mostly.
figure(1)
t = 1;
for i = [1 4 7 10]
    subplot(3,2,t)
    plot(data_n_f(:,i))
    t = t+1;
    grid on
    title('transducer drift')
    
end

subplot(3,2,5:6)
plot(summed_force_f(:,i-9))
grid on
title('summed force')


%% step ID

step_threshold = 30; %newtons
blah = summed_force_f(:,3) > step_threshold; %every data point that is over the threshold
events = diff(blah); % either x2-x1 = 0-1 = -1 (end of step) or x2-x1 = 1-0 = 1 (beginning of step)
step_begin.all = find(events == 1); %index of step begin
step_end.all = find(events == -1); %index of step end

% %check steps if needed
% figure(2)
% hold on
% plot(summed_force(:,3),'LineWidth',1)
% plot(summed_force_f(:,3),'LineWidth',1)
% plot(events*1000,'-k','Linewidth',1) %start & stop
% grid on
% hold off

%if trial starts with end of step, ignore it
step_end.all = step_end.all(step_end.all > step_begin.all(1)); 
%above compare indexes from begin #1 to every step end index, keep if end > begin is true

%remove steps that are too short (not full step @ end of trial
step_len = nan(length(step_end.all),1); %want to see what the length of each step is
good_step = 1;
for step_check = 1:length(step_end.all)
    step_len(step_check) = step_end.all(step_check) - step_begin.all(step_check); 
    %above is array of step length (end-begin), smallest so far = 195
    
    if step_end.all(step_check) - step_begin.all(step_check) > 195 %minimum length for full step length (frames)
        step_begin.all(good_step) = step_begin.all(step_check);
        step_end.all(good_step) = step_end.all(step_check);
        good_step = good_step+1;
    end
end
%trim any extra step starts/ends
if length(step_end.all) < length(step_begin.all)
    step_begin.all = step_begin.all(1:end-1);
elseif length(step_begin.all) < length(step_end.all)
    step_end.all = step_end.all(1:end-1);
end
%plot all separated steps

colors = parula(length(step_end.all));

figure(3)
hold on
for i = 1:size(step_end.all)
    plot(summed_force_f(step_begin.all(i):step_end.all(i),3),'color',colors(i,:))
end
grid on
title('all the separated steps')
hold off

%% Separate and trim aerial phases
%define aerial phases
aerial_begin = step_end.all(1:end-1);
aerial_end = step_begin.all(2:end); 
xtra = 40; %frames to trim off each end of aerial phase so filter effect at start/end of stance phase is minimized.
%initialize variables
aerial_mean = NaN(length(aerial_begin),3); %x,y,z

for i = 1:length(aerial_mean)
    aerial_mean(i,1) = mean(summed_force_f(aerial_begin(i)+xtra:aerial_end(i)-xtra,1));
    aerial_mean(i,2) = mean(summed_force_f(aerial_begin(i)+xtra:aerial_end(i)-xtra,2));
    aerial_mean(i,3) = mean(summed_force_f(aerial_begin(i)+xtra:aerial_end(i)-xtra,3));
end

colors = parula(length(aerial_begin));
%which axis to plot 
ax = 3;
%plot all untrimmed aerial phases
figure(4)
p1 = subplot(3,1,1);
title('untrimmed aerial phases','fontsize',16)
xlabel('frames')
hold on
for i = 1:length(aerial_begin)
    plot(summed_force_f(aerial_begin(i):aerial_end(i),ax),'color',colors(i,:))
end
grid on
hold off

%plot trimmed aerial phases
p2 = subplot(3,1,2);
title('trimmed aerial phases','fontsize',16)
xlabel('frames')
hold on
for i = 1:length(aerial_begin)
    plot(summed_force_f(aerial_begin(i)+xtra:aerial_end(i)-xtra,ax),'color',colors(i,:))
end
grid on
hold off

%plot means of trimmed aerial phases
p3 = subplot(3,1,3);
title('mean of trimmed aerial phases','fontsize',16)
xlabel('steps')
hold on
for i = 1:length(aerial_begin)
    plot(i,aerial_mean(i,ax),'o','color',colors(i,:))
end
grid on
hold off

linkaxes([p1,p2],'y')

%% Detrend each transducer (_t)

%initialize variables
data_detrend = NaN(size(data_n));
diff_vals = NaN(length(aerial_begin),12);
aerial_mean_t = NaN(length(aerial_begin),12);
aerial_mean_d = NaN(size(aerial_mean_t));

for t_num = 1:size(data_drift,2) %all transducers, all axes
    
    trans = data_drift(:,t_num);
    
    %calculate mean force during aerial phase for a given transducer
    for i = 1:length(aerial_begin)
        aerial_mean_t(i,t_num) = mean(trans(aerial_begin(i)+xtra:aerial_end(i)-xtra));
    end
    
    for i = 1:length(aerial_mean_t)-1
        diff_temp = (aerial_mean_t(i,t_num)+aerial_mean_t(i+1,t_num))/2; %mean of aerial phaes before/after given step (i)
        diff_vals(i,t_num) = diff_temp; %hangs onto value subtracted from each step across the 12 channels
        data_detrend(step_begin.all(i):step_begin.all(i+1),t_num) = ...
            trans(step_begin.all(i):step_begin.all(i+1)) - diff_temp; %detrended signal
    end
    
    %calculate mean aerial phase for detrend data
    for i = 1:length(aerial_begin)
        aerial_mean_d(i,t_num) = mean(data_detrend(aerial_begin(i)+xtra:aerial_end(i)-xtra,t_num));
    end
end


%sum detrended data
summed_force_detrend(:,1) = data_detrend(:,2)+data_detrend(:,5)+data_detrend(:,8)+data_detrend(:,11); %x
summed_force_detrend(:,2) = data_detrend(:,1)+data_detrend(:,4)+data_detrend(:,7)+data_detrend(:,10); %y
summed_force_detrend(:,3) = data_detrend(:,3)+data_detrend(:,6)+data_detrend(:,9)+data_detrend(:,12); %z

%% plot transducer specific drift
%adjustment values across transducers
figure(5)
plot(diff_vals)
grid on
title('values subtracted from each step - all 12 channels','fontsize',16)
xlabel('steps')

t_num = 1; %which transducer to plot (or axis if data_detrend is calculated from summed_force @ line 52)

figure(7)
p1 = subplot(3,2,2);
title('TRANSDUCER drift at end of trial','fontsize',16)
hold on
plot(linspace(0,length(data_detrend)/Fs_force,length(data_detrend)),data_detrend(:,t_num),'r')
plot(linspace(0,length(data_detrend)/Fs_force,length(data_detrend)),data_drift(:,t_num),'b')
xlim([length(data_detrend)/Fs_force-4,length(data_detrend)/Fs_force-1]) %last 3 seconds
xlabel('seconds')
legend('detrend','original')
grid on
hold off

p2 = subplot(3,2,1);
title('TRANSDUCER drift at start of trial','fontsize',16)
hold on
plot(linspace(0,length(data_detrend)/Fs_force,length(data_detrend)),data_detrend(:,t_num),'r')
plot(linspace(0,length(data_detrend)/Fs_force,length(data_detrend)),data_drift(:,t_num),'b')
xlim([0,3]) %first 3 seconds
xlabel('seconds')
grid on
hold off

p3 = subplot(3,2,3:4);
title('TRANSDUCER drift over whole trial','fontsize',16)
hold on
plot(linspace(0,length(data_detrend)/Fs_force,length(data_detrend)),data_detrend(:,t_num),'r')
plot(linspace(0,length(data_detrend)/Fs_force,length(data_detrend)),data_drift(:,t_num),'b')
xlabel('seconds')
grid on
hold off

linkaxes([p1,p2,p3],'y')

p4 = subplot(3,2,5:6);
title('mean of TRANSDUCER aerial phases','fontsize',16)
xlabel('steps')
hold on
for i = 1:length(aerial_mean_t)
    plot(i,aerial_mean_t(i,t_num),'b.')
    plot(i,aerial_mean_d(i,t_num),'r.')
end
grid on
hold off

figure(8) %detrended summed FORCE vs drifted summed FORCE. going to have to zoom in to find differences ~ 10N
for i = 1:3
    subplot(3,1,i)
    hold on
    plot(summed_force_f(:,i),'b') 
    plot(summed_force_detrend(:,i),'r') %make sure you detrended newtons and not voltages or the plot will be wrong
    grid on
    hold off
end
legend('drift summed force','detrended summed force')
disp('done')