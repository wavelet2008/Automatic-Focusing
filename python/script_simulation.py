# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 10:50:07 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: script-Automatic Focusing Simulation
"""

"""
demand:
    1 gif look like peak search
    2 optimized frames construction
"""

from __init__ import *

import os
import cv2

import copy as cp
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.pyplot import MultipleLocator
from matplotlib.font_manager import FontProperties

# '''VCM'''
# imgs_folder=r'C:\Users\ASUS\Desktop\500mm'
# output_folder=r'C:\Users\ASUS\Desktop\AF\500mm'

#E_P.Experiment5AreaFactor(imgs_folder,output_folder)
# E_P.Experiment5AreaWeight(imgs_folder,output_folder)
# E_P.ExperimentBlockModuleRatio(imgs_folder,output_folder)

# #img_gray=O_I.BatchImages(imgs_folder)[1][10]
# #plt.imshow(img_gray,cmap='gray')
# #cv2.imshow('gray',img_gray)

# '''tmp-Luminance, Near-others'''
# experiment_folder=r'C:\Users\ASUS\Desktop\500mm'
 
# #E_P.ExperimentContrastComparison(experiment_folder,'Constant')
#E_P.ExperimentContrastComparison(experiment_folder,'Advanced')
# #E_P.ExperimentContrastComparison(experiment_folder,'Standard Deviation')
    
# '''[:2]-tmp, [2:]-Near'''
# root_folder=r'C:\Users\Administrator\Desktop\Experiment'

# list_imgs_folder_name=[r'Luminance\Low',
#                        r'Luminance\High',
#                        r'Texture\Unobvious',
#                        r'Texture\Obvious',
#                        r'Distance\Invarious',
#                        r'Distance\Various']

# list_imgs_folder=[root_folder+'\\'+this_imgs_folder_name for this_imgs_folder_name in list_imgs_folder_name[:2]]

# E_P.ExperimentOverall(list_imgs_folder)

# imgs_folder=r'C:\Users\ASUS\Desktop\Experiment\Focus Calibration Lite-Small\100mm'
# imgs_folder=r'C:\Users\ASUS\Desktop\Experiment\Random\Polight'
# imgs_folder=r'C:\Users\ASUS\Desktop\Experiment\poLight\1000mm'

# C_P_S.FullSweep(imgs_folder,'Boccignone','Center')

# contain coarse and fine
# S_A_F.AutoFocusAnimation(imgs_folder,'Boccignone','Center')

total_folder=r'C:\Users\ASUS\Desktop\Experiment\Focus Calibration Lite-Large'
# total_folder=r'C:\Users\ASUS\Desktop\Experiment\poLight-Coarse'
# total_folder=r'C:\Users\ASUS\Desktop\Experiment\poLight-Fine'

for this_imgs_folder_name in os.listdir(total_folder):
    
    this_imgs_folder=total_folder+'\\'+this_imgs_folder_name
    
    C_P_S.FullSweep(this_imgs_folder,'Boccignone','Center')

    #contain coarse and fine
    # S_A_F.ImageAndContrast(this_imgs_folder,'Boccignone','Center')

