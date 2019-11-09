%% FIRST, IMPORT DATA FROM FUKUCHI ET AL 2017: USE RBDS001runT35forces.txt (column 3 is vertical)

Fs = 300;
dt = 1/Fs;
StopTime = 30;
t = (0:dt:StopTime-dt)';
Fc = 1/30;
sine_drift = sin(2*pi*Fc*t)*100;
exp_drift = exp(t/8);
plot(t,exp_drift)
vGRF = RBDS001runT25forces;
drift_vGRF = vGRF + sine_drift;

plot(drift_vGRF)


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
