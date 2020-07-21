# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 10:50:07 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Contrast Calculation
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

# '''optimized frames construction'''

imgs_folder=r'C:\Users\ASUS\Desktop\Experiment\Random\Office'

'''gif look like peak search'''
'''only coarse'''
# C_P_S.FullSweep(imgs_folder,'Boccignone')
S_A_F.ImageAndContrast(imgs_folder,'Boccignone')

# img = cv2.imread("test.jpg")
    
# try:
    
#     img_shape=img.shape
    
# except:
    
#     print('imread error')
    
# img=cv2.resize(img,(int(img_shape[1]/20),int(img_shape[0]/20)),interpolation=cv2.INTER_CUBIC)

# img_gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# contrast=C_T_F.MapTextureFeature(img_gray)['Contrast']
