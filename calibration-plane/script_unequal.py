# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 09:57:39 2020

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Script-Simulation of Auto Focus Calibration for unequal samples
"""

from __init__ import *

import os,imageio

import copy as cp
import numpy as np

import matplotlib.pyplot as plt

unequal_folder_path=os.getcwd()+'//frames/unequal'

O_P.GenerateFolder(unequal_folder_path)

center_canvas=[canvas.shape[0]/2,canvas.shape[1]/2]

figures=[]

for k in range(n_interval+1):
    
    this_offset=offset_start+(offset_end-offset_start)*k/n_interval
    this_zoom_factor=this_offset/offset_end
    
    print('-- frame:',k)
    print('-- zoom factor:',this_zoom_factor)
    
    #generate circle samples
    this_samples_circle=C_A_A.GenerateCircleSamples(offset_start,
                                                    offset_end,
                                                    n_interval,
                                                    radius_circle_original,
                                                    center_canvas,
                                                    this_zoom_factor)
    
    C_A_A.UnequalCircleEqual(canvas,
                             n_interval,
                             int(np.round(interval_circle_original/this_zoom_factor)),
                             this_samples_circle)
    
    this_fig_path=unequal_folder_path+'//'+str(k)+'.png'
    plt.savefig(this_fig_path,dpi=300,bbox_inches='tight')
    
    #collect fig to create GIF
    figures.append(imageio.imread(this_fig_path))
        
    plt.close()
    
#save GIF 
'''operator experiment'''
imageio.mimsave(unequal_folder_path+'\\unequal circle array.gif',figures,duration=0.13) 
