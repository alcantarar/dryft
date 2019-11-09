%% FIRST, IMPORT DATA FROM FUKUCHI ET AL 2017: USE RBDS001runT35forces.txt (column 3 is vertical)

Fs = 300;
dt = 1/Fs;
StopTime = 30;
t = (0:dt:StopTime-dt)';
Fc = 1/30;
sine_drift = sin(2*pi*Fc*t)*1000;
exp_drift = exp(t/8);
plot(t,exp_drift)
vGRF = RBDS001runT25forces;
drift_vGRF = vGRF + sine_drift;

plot(drift_vGRF)
%%
temp = drift_vGRF(110:546);

Fs = 300; % From Fukuchi et al. (2017) dataset
Fc = 60;
Fn = (Fs/2);
[b, a] = butter(2, Fc/Fn);

temp_f = filtfilt(b, a, temp);
trueGRF = vGRF(100:546);
trueGRF_f = filtfilt(b,a,trueGRF);

aerial_vals = [75, 146, 227, 302];
aerial_locs = [0,102,220,332];
hold on
plot(temp_f)
plot(aerial_locs, aerial_vals,'k*')
drift =[repmat(aerial_vals(1),aerial_locs(2)-aerial_locs(1),1); ...
    repmat(aerial_vals(2),aerial_locs(3)-aerial_locs(2),1); ...
    repmat(aerial_vals(3),aerial_locs(4)-aerial_locs(3),1); ...
    repmat(aerial_vals(4),length(temp_f)-aerial_locs(4),1)];
plot(drift)

figure
hold on
wrong = temp_f-drift;
plot(wrong,'k')
plot(trueGRF_f,'r--')
%% create custom drift
x = linspace(0,30,15);
y = [0,2,6,12,20,25,30, 33, 34, 35, 35.5, 36, 36.5, 37, 37.5]; %fake drift
y = y*3;
p = polyfit(x,y,6);

x1 = linspace(0,30, length(vGRF));
y1 = polyval(p,x1);
close 
figure
plot(x,y,'o')
hold on
plot(x1,y1);

%%
close
plot(vGRF)
hold on
plot(vGRF+y1')
custom_drift_vGRF = vGRF + y1';
csvwrite('custom_drift_S001runT25.csv',custom_drift_vGRF)
