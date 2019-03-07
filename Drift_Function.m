function [summed_force_detrend,transducer_force_detrend] = Drift_Function(summed_force, transducer_force,Fs_force, step_threshold, min_step, max_step, g)
%Program detrends force signal in a step-specific manner.Subtracts mean of
%aerial phase before and after given step across whole trial.
%
% INPUTS:
% summed_force:     n x 3 array of raw force data [horiz, horiz, vertical] (Newtons)
% transducer_force: n x 12 array of force data from transducers. Assumes
%                   order is Fx1, Fy1, Fz1, Fx2, Fy2, Fz2, Fx3... (Newtons)
% Fs_force:         Sampling frequency of treadmill (Hz)
% step_threshold    Force threshold to define step start/end. Default is
%                   high because may need to overcome significant drift
% min_step          Minimum contact time (s) to define acceptable step
% max_step          Max contact time (s) to define acceptable step
% g                 Logical to allow plotting of diagnostic graphs(1 == yes)
%
%OUTPUTS: Raw detrended force signals. Summed and Transducers force as separate arrays. 
%
%Created by: Ryan Alcantara - ryan.alcantara@colorado.edu
%
%% simple filter
Fc_force = 30;%hz
fn = (Fs_force/2);
[b, a] = butter(2,Fc_force/fn);
%convert nans to 0 before filtering the summed force
if isnan(summed_force)
    warning('converting NaNs to 0')
    summed_force(isnan(summed_force) == 1) = 0;
end
%filter
summed_force_f = filtfilt(b,a,summed_force);
%% simple step ID
blah = summed_force_f(:,3) > step_threshold; %every data point that is over the threshold
events = diff(blah); % either x2-x1 = 0-1 = -1 (end of step) or x2-x1 = 1-0 = 1 (beginning of step)
step_begin.all = find(events == 1); %index of step begin
step_end.all = find(events == -1); %index of step end

if g
    %check steps if needed
    figure(2)
    hold on
    plot(summed_force(:,3),'LineWidth',1)
    plot(summed_force_f(:,3),'LineWidth',1)
    plot(events*1000,'-k','Linewidth',1) %start & stop
    grid on
    hold off
end

%if trial starts with end of step, 
%ignore it so that trial starts with first whole step
step_end.keep = step_end.all(step_end.all > step_begin.all(1)); 
step_begin.keep = step_begin.all(1:length(step_end.keep));
%above compare indexes from begin #1 to every step end index, keep if end > begin is true

%remove steps that are too short (not full step @ end of trial
min_step = min_step*Fs_force;
max_step = max_step*Fs_force;

%calculate step length and compare to min step length
step_len = step_end.keep - step_begin.keep;
good_step = step_len >= min_step; %which steps meet minimum length req
good_step = good_step <= max_step; %which steps meet max length req
step_begin.keep = step_begin.keep(good_step); %take those steps' beginnings
step_end.keep = step_end.keep(good_step); %take those steps' ends

%plot all separated steps
% if g
%     colors = parula(length(step_end.keep));
%     
%     figure(3)
%     hold on
%     for i = 1:size(step_end.keep)
%         plot(summed_force_f(step_begin.keep(i):step_end.keep(i),3),'color',colors(i,:))
%     end
%     grid on
%     title('all the separated steps')
%     hold off
% end
%% Separate and trim aerial phases
%define aerial phases
aerial_begin = step_end.keep(1:end-1);
aerial_end = step_begin.keep(2:end); 
xtra = 35; %frames to trim off each end of aerial phase so filter effect at start/end of stance phase is minimized.
%initialize variables
aerial_mean = NaN(length(aerial_begin),3); %x,y,z

for i = 1:length(aerial_mean)
    aerial_mean(i,1) = mean(summed_force_f(aerial_begin(i)+xtra:aerial_end(i)-xtra,1));
    aerial_mean(i,2) = mean(summed_force_f(aerial_begin(i)+xtra:aerial_end(i)-xtra,2));
    aerial_mean(i,3) = mean(summed_force_f(aerial_begin(i)+xtra:aerial_end(i)-xtra,3));
end

if g
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
    subplot(3,1,3);
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
end
%% Detrend each transducer (_t)

%initialize variables
data_detrend = NaN(size(transducer_force)); %output: detrended data
diff_vals = NaN(length(aerial_begin)+1,12); %difference between consecutive aerial phases
aerial_mean_t = NaN(length(aerial_begin)+1,12); %means of aerial phases (pre detrending)
aerial_mean_d = NaN(size(aerial_mean_t)); %means of aerial phases (post detrending) for comparison

for t_num = 1:12 %all transducers, all axes
    
    trans = transducer_force(:,t_num);
    
    %calculate mean force during aerial phase for a given transducer
    i = 1;
    while i < min([length(step_begin.keep), length(step_end.keep)])
        aerial_mean_t(i,t_num) = mean(trans(aerial_begin(i)+xtra:aerial_end(i)-xtra)); %trim of early/late aerial phase because of filter effect
        i = i + 1;
    end
    %last one
    aerial_mean_t(i,t_num) = mean(trans(aerial_begin(i-1)+xtra:aerial_end(i-1)-xtra)); %trim of early/late aerial phase because of filter effect

    %first step, extend to end of file
    i = 1;
    diff_temp = (aerial_mean_t(i,t_num)+aerial_mean_t(i+1,t_num))/2; %mean of aerial phaes before/after given step (i)
    diff_vals(i,t_num) = diff_temp; %hang onto value subtracted from each step across the 12 channels
    data_detrend(1:step_begin.keep(i+1),t_num) = ...
        trans(1:step_begin.keep(i+1)) - diff_temp;
    %2:n-1 steps
    i = 2;
    while i < min([length(step_begin.keep), length(step_end.keep)])
        diff_temp = (aerial_mean_t(i,t_num)+aerial_mean_t(i+1,t_num))/2; %mean of aerial phaes before/after given step (i)
        diff_vals(i,t_num) = diff_temp; %hang onto value subtracted from each step across the 12 channels
        data_detrend(step_begin.keep(i):step_begin.keep(i+1),t_num) = ...
            trans(step_begin.keep(i):step_begin.keep(i+1)) - diff_temp;
        i = i+1;
    end
    %last step, extend to end of file
    diff_temp = (aerial_mean_t(i-1,t_num)+aerial_mean_t(i,t_num))/2; %mean of aerial phaes before/after given step (i)
    diff_vals(i,t_num) = diff_temp; %hang onto value subtracted from each step across the 12 channels
    data_detrend(step_begin.keep(i):length(transducer_force),t_num) = ...
        trans(step_begin.keep(i):length(transducer_force)) - diff_temp;

    %calculate mean aerial phase for detrend data
    i = 1;
    while i < min([length(step_begin.keep), length(step_end.keep)])
        aerial_mean_d(i,t_num) = mean(data_detrend(aerial_begin(i)+xtra:aerial_end(i)-xtra,t_num));
        i = i+1;
    end
    aerial_mean_d(i,t_num) = mean(data_detrend(aerial_begin(i-1)+xtra:aerial_end(i-1)-xtra,t_num)); %repeat last one

end

%sum detrended data
summed_force_detrend(:,1) = data_detrend(:,2)+data_detrend(:,5)+data_detrend(:,8)+data_detrend(:,11); %x
summed_force_detrend(:,2) = data_detrend(:,1)+data_detrend(:,4)+data_detrend(:,7)+data_detrend(:,10); %y
summed_force_detrend(:,3) = data_detrend(:,3)+data_detrend(:,6)+data_detrend(:,9)+data_detrend(:,12); %z

transducer_force_detrend = data_detrend;

%% plot transducer specific drift
% if g
%     t_num = 3; %which transducer to plot
%     
%     figure(7)
%     p1 = subplot(3,2,2);
%     title('Transducer drift at end of trial','fontsize',16)
%     hold on
%     plot(linspace(0,length(data_detrend)/Fs_force,length(data_detrend)),data_detrend(:,t_num),'r')
%     plot(linspace(0,length(data_detrend)/Fs_force,length(data_detrend)),transducer_force(:,t_num),'b')
%     xlim([length(data_detrend)/Fs_force-4,length(data_detrend)/Fs_force-1]) %last 3 seconds
%     xlabel('seconds')
%     legend('detrend','original')
%     grid on
%     hold off
%     
%     p2 = subplot(3,2,1);
%     title('Transducer drift at start of trial','fontsize',16)
%     hold on
%     plot(linspace(0,length(data_detrend)/Fs_force,length(data_detrend)),data_detrend(:,t_num),'r')
%     plot(linspace(0,length(data_detrend)/Fs_force,length(data_detrend)),transducer_force(:,t_num),'b')
%     xlim([0,3]) %first 3 seconds
%     xlabel('seconds')
%     grid on
%     hold off
%     
%     p3 = subplot(3,2,3:4);
%     title('Transducer drift over whole trial','fontsize',16)
%     hold on
%     plot(linspace(0,length(data_detrend)/Fs_force,length(data_detrend)),data_detrend(:,t_num),'r')
%     plot(linspace(0,length(data_detrend)/Fs_force,length(data_detrend)),transducer_force(:,t_num),'b')
%     xlabel('seconds')
%     grid on
%     hold off
%     
%     linkaxes([p1,p2,p3],'x')
%     
%     subplot(3,2,5:6);
%     title('mean of Transducer aerial phases','fontsize',16)
%     xlabel('steps')
%     hold on
%     for i = 1:length(aerial_mean_t)
%         plot(i,aerial_mean_t(i,t_num),'bo')
%         plot(i,aerial_mean_d(i,t_num),'ro')
%     end
%     fit1 = polyfit((1:length(aerial_mean_t))', aerial_mean_t(:,t_num),2);
%     plot(polyval(fit1,1:length(aerial_mean_t)),'b','LineWidth',1.5)
%     fit2 = polyfit((1:length(aerial_mean_t))', aerial_mean_d(:,t_num),2);
%     plot(polyval(fit2,1:length(aerial_mean_t)),'r','LineWidth',1.5)
%     grid on
%     hold off
% end
%%
%filter detrended data 
summed_force_detrend_f = summed_force_detrend;
summed_force_detrend_f(isnan(summed_force_detrend_f)) = 0; %replace nan with 0 for filtering
summed_force_detrend_f = filtfilt(b,a,summed_force_detrend_f);

if g
    figure(8) %detrended summed FORCE vs drifted summed FORCE. going to have to zoom in to find differences ~ 10N
    for i = 1:3
        s(i) = subplot(4,1,i);
        hold on
        plot(summed_force_f(:,i),'b:','LineWidth',2)
        plot(summed_force_detrend_f(:,i),'r') %make sure you detrended newtons and not voltages or the plot will be wrong
        grid on
        hold off
    end
    disp('done')
    linkaxes(s,'x')
    
    %get aerial phases of detrended summed data
    aerial_mean_summed_d = NaN(length(aerial_mean), 3);
    for i = 1:length(aerial_mean)
        aerial_mean_summed_d(i,1) = mean(summed_force_detrend_f(aerial_begin(i)+xtra:aerial_end(i)-xtra,1));
        aerial_mean_summed_d(i,2) = mean(summed_force_detrend_f(aerial_begin(i)+xtra:aerial_end(i)-xtra,2));
        aerial_mean_summed_d(i,3) = mean(summed_force_detrend_f(aerial_begin(i)+xtra:aerial_end(i)-xtra,3));
    end
    
    %plot means of trimmed aerial phases
    ax = 1;
    subplot(4,1,4);
    title('mean of trimmed aerial phases - summed force','fontsize',16)
    xlabel('steps')
    hold on
    for i = 1:length(aerial_mean)
        plot(i,aerial_mean(i,ax),'bo')
        plot(i,aerial_mean_summed_d(i,ax),'ro')
    end
    fit1 = polyfit((1:length(aerial_mean))', aerial_mean(:,ax),2);
    plot(polyval(fit1,1:length(aerial_mean)),'b','LineWidth',1.5)
    fit2 = polyfit((1:length(aerial_mean))', aerial_mean_summed_d(:,ax),2);
    plot(polyval(fit2,1:length(aerial_mean)),'r','LineWidth',1.5)
    
    legend('drifted summed force','detrended summed force')
    grid on
    hold off
end

end