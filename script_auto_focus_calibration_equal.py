# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 09:56:16 2020

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Script-Simulation of Auto Focus Calibration for equal samples
"""

from configuration_auto_focus_calibration import *

import os,imageio

import copy as cp
import numpy as np

import matplotlib.pyplot as plt

figures=[]

#invarious offset in different frame associated VCM code
for k in range(n_interval+1):
    
    this_offset=offset_start+(offset_end-offset_start)*k/n_interval
    this_zoom_factor=this_offset/offset_end
    
    print('-- frame:',k)
    print('-- zoom factor:',this_zoom_factor)
    
    #Generate circle array
    C_A_A.EqualCircleArray(canvas,
                           n_interval,
                           int(np.round(radius_circle_original/this_zoom_factor)),
                           int(np.round(interval_circle_original/this_zoom_factor)))
    
    this_fig_path=equal_folder_path+'//'+str(k)+'.png'
    plt.savefig(this_fig_path,dpi=300,bbox_inches='tight')
    
    #collect fig to create GIF
    figures.append(imageio.imread(this_fig_path))
        
    plt.close()
    
#save GIF 
'''operator experiment'''
imageio.mimsave(equal_folder_path+'\\'+'equal circle array.gif',figures,duration=0.13) 