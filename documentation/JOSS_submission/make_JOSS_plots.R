library(ggplot2)
library(ggthemes)
library(viridis)


data.aerial = read.csv('aerial_plots_data.csv') #exported from sample.py [aerial_means_d]
head(data.aerial)

ggplot(data = data.aerial) +
  geom_abline(intercept = 0, slope = 0, lwd = 1, alpha = 1, color = 'black')+
  geom_point((aes(y = aerial_val, x = aerial_loc, color = signal)), size = 3, alpha = 1)+
  scale_y_continuous('Force at Middle of Aerial Phase [N]', breaks = seq(-100,100,20))+
  scale_x_continuous('Frame')+
  scale_color_tableau(label = c('Corrected','Original'),palette = 'Classic Blue-Red 6')+
  theme_classic()+
  theme(axis.line = element_line(size =1, color = 'black'),
        axis.ticks = element_line(size = 1, color = 'black'),
        axis.text = element_text(size = 12, color = 'black'),
        axis.title = element_text(size = 14, face = 'bold', color = 'black'),
        legend.position = c(.15,.85),
        legend.text = element_text(size = 12, face = 'bold', color = 'black'),
        legend.title = element_blank(),
        legend.key.width = unit(.3, 'in'),
        legend.background = element_rect(fill = alpha('white',0.8), size = 1, linetype = 'solid', color = 'black'),
        plot.margin = unit(c(10,10,10,10),'points'))

# ggsave('steps.png',height = 4, width = 8, units = 'in')


data.ex = read.csv('joss_example.csv') #exported from sample.py [force_fd] and [GRF_filt]


head(data.ex)

ggplot(data = data.ex) +
  geom_abline(intercept = 0, slope = 0, lwd = 1, alpha = 1)+
  geom_line((aes(x = time, y = wrong)), alpha = 1, lwd = 1)+
  geom_line((aes(x = time, y = right)), alpha = 1, lwd = 1, color = 'red')+
  scale_color_tableau(label = c('Corrected','Original'),palette = 'Classic 10')+
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

# ggsave('example.eps',height = 8, width = 8, units = 'in')
