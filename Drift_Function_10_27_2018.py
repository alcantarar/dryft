#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def detrend_force(filename,Fs,Fc,min_step_length,step_threshold = 100,plots_on = False):
    '''This function reads in a comma separated file of *running* ground reaction force data and removes drift in a stepwise manner.
    
    force_imported:     Nx3 array of 3D [horizontal,horizontal,vertical] force data
    Fs:                 sampling frequency of force signal
    Fc:                 cutt off frequency for 4th order zero-lag butterworth filter
    min_step_length:    the minimum number of frames the step ID algorithm will consider 1 step
    step_threshold:     threshold in Newtons used to define heel-strike and toe-off. default is 100N (better to be aggressive for detrending)
    plots_on:           T/F logical input to receive graphs depicting detrend process
    
    '''
    
    import pylab as py
    from scipy.signal import butter, filtfilt
    import copy
    
    force_imported = py.loadtxt(filename,delimiter = ',')
    
    fn = (Fs/2)
    b,a = butter(2,Fc/fn)
    force_imported_f = filtfilt(b,a,force_imported,axis = 0)
    
    if py.size(force_imported,1) == 3:  
        force = copy.copy(force_imported)
        force_f = copy.copy(force_imported_f)
        
        #step Identification Forces over step_threshold register as step (foot on ground).
        blah = force_f[:,2] > step_threshold
        blah = blah.astype(int)
        events = py.diff(blah)
        step_begin = py.find(events == 1)
        step_end = py.find(events == -1)
        
        #if trial starts with end of step, ignore
        step_end = step_end[step_end > step_begin[0]]

        #check step length
        #initialize
        step_len = py.ndarray(py.size(step_end))
        step_begin_all = py.ndarray(py.size(step_begin))
        step_end_all = py.ndarray(py.size(step_end))
        step_len[:] = py.nan
        step_begin_all[:] = py.nan
        step_end_all[:] = py.nan
        
        good_step = 0
        
        for step_check in range(py.size(step_len)):
            step_len[step_check] = step_end[step_check] - step_begin[step_check]
            if step_end[step_check] - step_begin[step_check] > min_step_length: #removes false positives by comparing to min_step_length
                step_begin_all[good_step] = step_begin[step_check]
                step_end_all[good_step] = step_end[step_check]
                good_step = good_step+1                
        
        #remove unused NaN cells
        step_end_all = step_end_all[~py.isnan(step_end_all)]
        step_begin_all = step_begin_all[~py.isnan(step_begin_all)]
        #check sizes of begin/end
        step_end_all = step_end_all.astype(int)
        step_begin_all = step_begin_all.astype(int)
        print('step begin/end:',py.size(step_end_all), py.size(step_begin_all))


        #create aerial phases (foot not on ground) and trim artefacts from filtering
        aerial_begin = step_end_all[:-1]
        aerial_end = step_begin_all[1:]
        print('aerial begin/end:',py.size(aerial_begin),py.size(aerial_end)) #matching number of step beginnings/ends

        if plots_on != False:
            py.figure(1)
            py.title('All Separated Steps')
            py.grid()
            for i in range(py.size(step_end_all)): py.plot(force_f[step_begin_all[i]:step_end_all[i],2])
        
        # %%plot a few steps and get user input for how much to trim off beginning/end of aerial phase
        fig, ax = py.subplots()
        ax.plot(force[step_begin_all[0]:step_end_all[1],2])
        ax.plot(force_f[step_begin_all[0]:step_end_all[1],2])
        start_a = force_f[step_begin_all[0]:step_end_all[1],2] == force_f[step_end_all[0],2]
        end_a = force_f[step_begin_all[0]:step_end_all[1],2] == force_f[step_begin_all[1],2]
        ax.axvline(start_a.nonzero(),color = 'k')
        ax.axvline(end_a.nonzero(),color = 'k')
        ax.set_title('select how much to trim off beginning/end of aerial phase (between black lines)')
        
        #user input from mouse click
        points = py.asarray(py.ginput(2),dtype = int)
        py.pause(.2)
        py.close(fig)
        trim = round((points[0,0]-start_a.nonzero()[0][0] + end_a.nonzero()[0][0]-points[1,0])/2)
        trim = trim.astype(int)
        print('trimming ',trim,' frames from the start/end of aerial phase')
        
        #initialize
        aerial_mean = py.ndarray([py.size(aerial_begin),3])
        
        #calculate mean force during aerial phase (foot not on ground, should be zero)
        for i in range(py.size(aerial_begin)):
            aerial_mean[i,0] = py.mean(force_f[aerial_begin[i]+trim:aerial_end[i]-trim,0])
            aerial_mean[i,1] = py.mean(force_f[aerial_begin[i]+trim:aerial_end[i]-trim,1])
            aerial_mean[i,2] = py.mean(force_f[aerial_begin[i]+trim:aerial_end[i]-trim,2])
        
        #plot aerial phases
        if plots_on != False:

            colors = py.cm.viridis(py.linspace(0,1,py.size(aerial_begin)))
            py.fig, (untrimp, trimp, meanp) = py.subplots(3,1,sharex = False, figsize = (15,10))
            #plot of untrimmed aerial phases
            untrimp.set_title('untrimmed aerial phases')
            untrimp.grid()
            for i in range(py.size(aerial_begin)):
                untrimp.plot(force_f[aerial_begin[i]:aerial_end[i],2],color = colors[i])  
            #plot of trimmed aerial phases    
            trimp.set_title('trimmed aerial phases')
            trimp.grid()
            for i in range(py.size(aerial_begin)):
                trimp.plot(force_f[aerial_begin[i]+trim:aerial_end[i]-trim,2],color = colors[i])
            #plot all the means of trimmed aerial phases
            meanp.set_title('mean of trimmed aerial phases')
            meanp.set_xlabel('steps')
            meanp.grid()
            for i in range(py.size(aerial_begin)):
                meanp.plot(i,aerial_mean[i,2],'o',color = colors[i])
        
        # %%detrend signal    
        force_fd = py.zeros([py.size(force_f,0),3])
        #force_fd = copy.copy(force_f[:,2])
        #print('loop values')
        diff_vals = []
        for i in range(py.size(aerial_mean[:,2])-1):
            diff_temp = (aerial_mean[i,2]+aerial_mean[i+1,2])/2 #mean between two subsequent aerial phases
            diff_vals.append(diff_temp)
            force_fd[step_begin[i]:step_begin[i+1],:] = force_f[step_begin[i]:step_begin[i+1],:] - diff_temp
            
        if plots_on != False:
            py.figure(figsize = (10,3))
            py.title('mean of aerial phases and correction values')
            py.xlabel('steps',fontsize = 16)
            py.grid()
            for i in range(py.size(aerial_mean,0)):
                py.plot(i,aerial_mean[i,2],'o',color = colors[i])                
            py.plot(py.linspace(.5,py.size(diff_vals)-.5, py.size(diff_vals)),diff_vals,'.k') 
                
            #plot raw vs detrended
            py.figure(figsize = (20,10))
            py.plot(py.linspace(0,py.size(force_f,0)/Fs,py.size(force_f,0)),force_f[:,2], alpha = 0.7) #converted to sec
            py.plot(py.linspace(0,py.size(force_f,0)/Fs,py.size(force_f,0)),force_fd[:,2],'r', alpha = 0.7) #converted to sec
            py.grid()
            py.legend(['original signal','detrended signal'],fontsize =16)
            py.xlabel('Seconds', fontsize = 16)
        
        
        #calculate mean aerial for detrend data
        aerial_mean_d = py.zeros(py.size(aerial_mean[:,2]))
        for i in range(py.size(aerial_begin)):
            aerial_mean_d[i] = py.mean(force_fd[aerial_begin[i]+trim:aerial_end[i]-trim,2]) #just vertical force
        aerial_mean_d = aerial_mean_d[aerial_mean_d !=0.0]

        if plots_on != False:
            #plot detrend vs old mean aerial
            py.figure(figsize = (20,5))
            py.title('mean of aerial phases')
            py.xlabel('steps',fontsize = 16)
            py.grid()
            #py.ylim([-20,20])
            for i in range(py.size(aerial_mean,0)-1):
                py.plot(i,aerial_mean[i,2],'.', color = 'tab:blue', label = 'original signal')
                py.plot(i,aerial_mean_d[i],'.', color = 'tab:red', label = 'detrended signal')
                py.legend(['original signal','detrended signal']) #don't want it in loop, but it needs it?


    else: raise ValueError('force data must be Nx3 columns [horiz, horiz, vertical]')
