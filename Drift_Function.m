%Program detrends force signal in a step-specific manner.Subtracts mean of
%aerial phase before and after given step across whole trial.
%Inputs: location of data_v (volts from HighSpeed Treadmill),
% line 52 (signal to detrend), and line 131 if needed (amount to trim off 
% the beginning and end of aerial phase).

%Outputs: crap ton of plots and data_detrend variable
%Created by: Ryan Alcantara - ryan.alcantara@colorado.edu
%Last edited 8/17/2018
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clearvars
close all
clc
%first import voltages (xyz*4 transducers = 12 channels)
[fname, fpath]=uigetfile('*.csv','Select GRF data file :');
disp(fname)
channels = readtable([fpath fname]); %read everything
channels = channels(:,3:14); %keep signals
ch_names = table2cell(channels(3,1:end)); %pull column names (sometimes in diff orders)
channels.Properties.VariableNames = ch_names; %save column names
channels = channels(5:end,:); %keep just signal values (no frames, colnames)
channels = varfun(@str2double,channels, 'InputVariables',@(x) ~isnumeric(x)); %convert strings to numbers
channels.Properties.VariableNames = ch_names; %re-insert column names

%% convert to newtons. CALMAT (in HighSpeedV2F_Table) is specific to your treadmill. pull from v3d.
[volts_transducers, newtons_transducers, summed_force, colnames] = HighSpeedV2F_Table(channels);
%% simple filter
Fs_force = 1000;
Fc_force = 30;
fn = (Fs_force/2);
[b a] = butter(4,Fc_force/fn);
summed_force_f = filtfilt(b,a,summed_force);
data_n_f = filtfilt(b,a,newtons_transducers);
data_v_f = filtfilt(b,a,volts_transducers);
%% chose signal to detrend. 
%Options:
% -> newtons_transducers is unfiltered transducer in newtons.
% -> data_n_f is filtered transducer in newtons.
% -> volts_transducers is raw voltage
% -> data_v_f is filtered transducer in volts (idk why but why not)

%Available for comparison, but won't work with detrend code. Need n x 12.
% -> summed_force is sum of transducers, unfiltered, in newtons
% -> summed_force_f is sum of transducers, filtered, in newtons
data_drift = newtons_transducers;

%% simple step ID

step_threshold = 100; %newtons. be heavy-handed at first. 
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

%if trial starts with end of step, 
%ignore it so that trial starts with first whole step
step_end.keep = step_end.all(step_end.all > step_begin.all(1)); 
step_begin.keep = step_begin.all(1:length(step_end.keep));
%above compare indexes from begin #1 to every step end index, keep if end > begin is true

%remove steps that are too short (not full step @ end of trial
min_step = 0.15*Fs_force;
max_step = 0.35*Fs_force;

%calculate step length and compare to min step length
step_len = step_end.keep - step_begin.keep;
good_step = step_len >= min_step; %which steps meet minimum length req
good_step = good_step <= max_step; %which steps meet max length req
step_begin.keep = step_begin.keep(good_step); %take those steps' beginnings
step_end.keep = step_end.keep(good_step); %take those steps' ends

%plot all separated steps

colors = parula(length(step_end.keep));

figure(3)
hold on
for i = 1:size(step_end.keep)
    plot(summed_force_f(step_begin.keep(i):step_end.keep(i),3),'color',colors(i,:))
end
grid on
title('all the separated steps')
hold off

%% Separate and trim aerial phases
%define aerial phases
aerial_begin = step_end.keep(1:end-1);
aerial_end = step_begin.keep(2:end); 
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
ylim([min(aerial_mean(:,ax))-10, max(aerial_mean(:,ax))+10])

linkaxes([p1,p2],'y')

%% Detrend each transducer (_t)

%initialize variables
data_detrend = NaN(size(data_drift)); %output: detrended data
diff_vals = NaN(length(aerial_begin)+1,12); %difference between consecutive aerial phases
aerial_mean_t = NaN(length(aerial_begin)+1,12); %means of aerial phases (pre detrending)
aerial_mean_d = NaN(size(aerial_mean_t)); %means of aerial phases (post detrending) for comparison

for t_num = 1:12 %all transducers, all axes
    
    trans = data_drift(:,t_num);
    
    %calculate mean force during aerial phase for a given transducer
    %     for i = 1:length(aerial_begin)
    i = 1;
    while i < min([length(step_begin.all), length(step_end.all)])-1
        aerial_mean_t(i,t_num) = mean(trans(aerial_begin(i)+xtra:aerial_end(i)-xtra)); %trim of early/late aerial phase because of filter effect
        i = i + 1;
    end
    %last one
    aerial_mean_t(i,t_num) = mean(trans(aerial_begin(i-1)+xtra:aerial_end(i-1)-xtra)); %trim of early/late aerial phase because of filter effect

    
    %     for i = 1:length(aerial_mean_t)-1
    %         diff_temp = (aerial_mean_t(i,t_num)+aerial_mean_t(i+1,t_num))/2; %mean of aerial phaes before/after given step (i)
    %         diff_vals(i,t_num) = diff_temp; %hang onto value subtracted from each step across the 12 channels
    %         data_detrend(step_begin.all(i):step_begin.all(i+1),t_num) = ...
    %             trans(step_begin.all(i):step_begin.all(i+1)) - diff_temp; % signal - difference between aerial phase before/after = detrended signal
    %     end
    %     %and last step will repeat final diff (might be slightly off)
    %     i = i+1;
    i = 1;
    while i < min([length(step_begin.all), length(step_end.all)])-1
        diff_temp = (aerial_mean_t(i,t_num)+aerial_mean_t(i+1,t_num))/2; %mean of aerial phaes before/after given step (i)
        diff_vals(i,t_num) = diff_temp; %hang onto value subtracted from each step across the 12 channels
        data_detrend(step_begin.all(i):step_begin.all(i+1),t_num) = ...
            trans(step_begin.all(i):step_begin.all(i+1)) - diff_temp;
        i = i+1;
    end
    diff_temp = (aerial_mean_t(i-1,t_num)+aerial_mean_t(i,t_num))/2; %mean of aerial phaes before/after given step (i)
    diff_vals(i,t_num) = diff_temp; %hang onto value subtracted from each step across the 12 channels
    data_detrend(step_begin.all(i):step_begin.all(i+1),t_num) = ...
        trans(step_begin.all(i):step_begin.all(i+1)) - diff_temp;

    %calculate mean aerial phase for detrend data
    %     for i = 1:length(aerial_begin)
    i = 1;
    while i < min([length(step_begin.all), length(step_end.all)])-1
        aerial_mean_d(i,t_num) = mean(data_detrend(aerial_begin(i)+xtra:aerial_end(i)-xtra,t_num));
        i = i+1;
    end
    aerial_mean_d(i,t_num) = mean(data_detrend(aerial_begin(i-1)+xtra:aerial_end(i-1)-xtra,t_num)); %repeat last one

end


%sum detrended data
summed_force_detrend(:,1) = data_detrend(:,2)+data_detrend(:,5)+data_detrend(:,8)+data_detrend(:,11); %x
summed_force_detrend(:,2) = data_detrend(:,1)+data_detrend(:,4)+data_detrend(:,7)+data_detrend(:,10); %y
summed_force_detrend(:,3) = data_detrend(:,3)+data_detrend(:,6)+data_detrend(:,9)+data_detrend(:,12); %z

%% plot transducer specific drift
%adjustment values across transducers
% figure(5)
% plot(diff_vals)
% grid on
% title('values subtracted from each step - all 12 channels','fontsize',16)
% xlabel('steps')
% if unique(data_drift == newtons_transducers) || unique(data_drift == data_n_f)
%     ylabel('newtons')
% elseif unique(data_drift == volts_transducers) || unique(data_drift == data_v_f)
%     ylabel('volts')
% end

t_num = 3; %which transducer to plot

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
    plot(i,aerial_mean_t(i,t_num),'bo')
    plot(i,aerial_mean_d(i,t_num),'ro')
end
fit1 = polyfit((1:length(aerial_mean_t))', aerial_mean_t(:,t_num),2);
plot(polyval(fit1,1:length(aerial_mean_t)),'b','LineWidth',1.5)
fit2 = polyfit((1:length(aerial_mean_t))', aerial_mean_d(:,t_num),2);
plot(polyval(fit2,1:length(aerial_mean_t)),'r','LineWidth',1.5)
grid on
hold off
%%
figure(8) %detrended summed FORCE vs drifted summed FORCE. going to have to zoom in to find differences ~ 10N
%filter detrended data 
summed_force_detrend_f = summed_force_detrend;
summed_force_detrend_f(isnan(summed_force_detrend_f)) = 0; %replace nan with 0 for filtering
summed_force_detrend_f = filtfilt(b,a,summed_force_detrend_f);
for i = 1:3
   s(i) = subplot(3,1,i);
    hold on
    plot(summed_force_detrend_f(:,i),'r') %make sure you detrended newtons and not voltages or the plot will be wrong
    plot(summed_force_f(:,i),'b') 
    grid on
    hold off
end
legend('drift summed force','detrended summed force')
disp('done')
linkaxes(s,'x')