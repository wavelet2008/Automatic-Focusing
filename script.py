# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 10:50:07 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title：Contrast Calculation
"""

from __init__ import *

import os
import cv2

import copy as cp
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.pyplot import MultipleLocator
from matplotlib.font_manager import FontProperties

imgs_folder=r'C:\Users\Administrator\Desktop\Ink_Step50'
output_folder=r'C:\Users\Administrator\Desktop\Contrast\Parameter'

#E_P.Experiment5AreaFactor(imgs_folder,output_folder,1)
#E_P.Experiment5AreaWeight(imgs_folder,output_folder,1)
#E_P.ExperimentBlockModuleRatio(imgs_folder,output_folder,1)

#img_gray=O_I.BatchImages(imgs_folder)[1][10]
#plt.imshow(img_gray,cmap='gray')
#cv2.imshow('gray',img_gray)

experiment_folder=r'C:\Users\Administrator\Desktop\Experiment\Texture'
 
#E_P.ExperimentContrastComparison(experiment_folder,'Constant')
#E_P.ExperimentContrastComparison(experiment_folder,'Advanced')
#E_P.ExperimentContrastComparison(experiment_folder,'Standard Deviation')
    
root_folder=r'C:\Users\Administrator\Desktop\Experiment'

list_imgs_folder_name=[r'Luminance\Low',
                       r'Luminance\High',
                       r'Texture\Unobvious',
                       r'Texture\Obvious',
                       r'Distance\Invarious',
                       r'Distance\Various']

list_imgs_folder=[root_folder+'\\'+this_imgs_folder_name for this_imgs_folder_name in list_imgs_folder_name[:2]]

#E_P.ExperimentOverall(list_imgs_folder)

'''criteria of Critiria and Algorithm from DB or photos''' 

'''optimized frames construction'''

'''plot maximum bound and output the best frame'''

imgs_folder=r'C:\Users\Administrator\Desktop\Experiment\Luminance\Low'

C_P_S.FullSweep(imgs_folder,'Michelson')
