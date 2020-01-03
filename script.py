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

#imgs_folder=r'C:\Users\Administrator\Desktop\Experiment\Distance\Invarious\Coarse'
#imgs_folder=r'C:\Users\Administrator\Desktop\Experiment\Distance\Various\Coarse'
#imgs_folder=r'C:\Users\Administrator\Desktop\Experiment\Luminance\High\Coarse'
#imgs_folder=r'C:\Users\Administrator\Desktop\Experiment\Luminance\Low\Coarse'
#imgs_folder=r'C:\Users\Administrator\Desktop\Experiment\Texture\Obvious\Coarse'
imgs_folder=r'C:\Users\Administrator\Desktop\Experiment\Texture\Unobvious\Coarse'

img_gray=O_I.BatchImages(imgs_folder)[1][10]
#plt.imshow(img_gray,cmap='gray')
#cv2.imshow('gray',img_gray)

#folder_total=r'C:\Users\Administrator\Desktop\Experiment'
#
#for name_this_experiment in os.listdir(folder_total):
#    
#    E_P.ExperimentContrastComparison(folder_total+'\\'+name_this_experiment,'Constant')
#    E_P.ExperimentContrastComparison(folder_total+'\\'+name_this_experiment,'Advanced')

#imgs_folder=r'C:\Users\Administrator\Desktop\Experiment\Texture\Unobvious' 
#imgs_folder=r'C:\Users\Administrator\Desktop\Experiment\Texture\Obvious' 
#imgs_folder=r'C:\Users\Administrator\Desktop\Experiment\Distance\Invarious'
#imgs_folder=r'C:\Users\Administrator\Desktop\Experiment\Distance\Various'

root_folder=r'C:\Users\Administrator\Desktop\Experiment'

list_imgs_folder_name=[r'Luminance\Low',
                       r'Luminance\High',
                       r'Texture\Unobvious',
                       r'Texture\Obvious',
                       r'Distance\Invarious',
                       r'Distance\Various']

list_imgs_folder=[root_folder+'\\'+this_imgs_folder_name for this_imgs_folder_name in list_imgs_folder_name]

E_P.ExperimentOverall(list_imgs_folder)

'''criteria of Critiria and Algorithm from DB or photos''' 

'''optimized frames construction'''

'''plot maximum bound and output the best frame'''