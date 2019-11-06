library(ggplot2)
library(ggthemes)
library(viridis)

data.raw = read.csv('detrend_plots_data.csv') #exported from sample.py [force_fd] and [GRF_filt]
head(data.raw)

data.raw$t = rep(seq(0.003333333,30, 1/300),2)

ggplot(data = data.raw[data.raw$frame <1782 & data.raw$frame > 1520,]) +
  geom_abline(intercept = 0, slope = 0, lwd = 1, alpha = 1)+
  geom_line((aes(x = t, y = force, color = signal)), alpha = 1, lwd = 1)+
  scale_color_tableau(palette = 'Classic 10')+
  scale_y_continuous('Vertical Ground Reaction Force [N]', breaks = seq(0,2000,300))+
  scale_x_continuous('Time [s]', breaks = seq(5,6,.2))+
  theme_classic()+
  theme(axis.line = element_line(size =1, color = 'black'),
        axis.ticks = element_line(size = 1, color = 'black'),
        axis.text = element_text(size = 12, color = 'black'),
        axis.title = element_text(size = 14, face = 'bold', color = 'black'),
        legend.position = c(.85,.9),
        legend.text = element_text(size = 12, face = 'bold', color = 'black'),
        legend.title = element_blank(),
        legend.key.width = unit(.3, 'in'),
        legend.background = element_rect(fill = alpha('white',0.8), size = 1, linetype = 'solid', color = 'black'),
        plot.margin = unit(c(10,10,10,10),'points'))

# ggsave('waveform.png',height = 4, width = 8, units = 'in')

data.mean = read.csv('means_plots_data.csv') #exported from sample.py [aerial_means_d]
head(data.mean)

ggplot(data = data.mean) +
  geom_abline(intercept = 0, slope = 0, lwd = 1, alpha = 1, color = 'black')+
  geom_point((aes(y = force, x = step, color = signal)), size = 2, alpha = 1)+
  scale_y_continuous('Mean Aerial Phase Force [N]', breaks = seq(-100,100,20))+
  scale_x_continuous('Step #')+
  scale_color_tableau(palette = 'Classic 10')+
  theme_classic()+
  theme(axis.line = element_line(size =1, color = 'black'),
        axis.ticks = element_line(size = 1, color = 'black'),
        axis.text = element_text(size = 12, color = 'black'),
        axis.title = element_text(size = 14, face = 'bold', color = 'black'),
        legend.position = c(.85,.85),
        legend.text = element_text(size = 12, face = 'bold', color = 'black'),
        legend.title = element_blank(),
        legend.key.width = unit(.3, 'in'),
        legend.background = element_rect(fill = alpha('white',0.8), size = 1, linetype = 'solid', color = 'black'),
        plot.margin = unit(c(10,10,10,10),'points'))

# ggsave('steps.png',height = 4, width = 8, units = 'in')

step <- read.csv('stepID.csv') #exported from sample.py [step_begin] and [step_end]
head(step)

temp <- data.frame(matrix(nrow = 100, ncol = nrow(step)))
orig <- data.raw$force[data.raw$signal == 'original']
for (i in 1:nrow(step)){
  temp[1:(step$end[i]-step$begin[i]+1),i] <- orig[step$begin[i]:step$end[i]]
  
}
colnames(temp) <- seq(1:nrow(step))

library(reshape2)

temp_m <- melt(temp) #X1 = step1, X2 = step2
temp_m$time <- rep(data.raw$t[1:100],nrow(step))
colnames(temp_m) <- c('Step','force','time')
temp_m$Step <- as.numeric(temp_m$Step)
head(temp_m)

ggplot(data = temp_m[temp_m$Step <25,], aes(x = time, y = force, group = Step))+
  geom_line(aes(color = Step), lwd = 1, alpha = 0.7)+
  # scale_color_gradient2_tableau(palette = "Green-Blue Diverging", guide = "colourbar")+
  scale_color_viridis(option = 'viridis')+
  scale_y_continuous('Vertical Ground Reaction Force [N]', breaks = seq(0,2000,300))+
  scale_x_continuous('Time [s]', breaks = seq(0,.3,.1))+
  theme_classic()+
  theme(axis.line = element_line(size =1, color = 'black'),
        axis.ticks = element_line(size = 1, color = 'black'),
        axis.text = element_text(size = 12, color = 'black'),
        axis.title = element_text(size = 14, face = 'bold', color = 'black'),
        legend.position = c(.85,.6),
        legend.text = element_text(size = 12, face = 'bold', color = 'black'),
        legend.title = element_text(face = 'bold'),
        legend.key.width = unit(.35, 'in'),
        legend.background = element_rect(fill = alpha('white',0.8), size = 1, linetype = 'solid', color = 'black'),
        plot.margin = unit(c(10,10,10,10),'points'))

# ggsave('Figure_1.png',height = 4, width = 8, units = 'in')
