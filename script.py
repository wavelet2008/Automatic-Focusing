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

#imgs_folder=r'C:\Users\Administrator\Desktop\Ink_Step50'

#imgs_folder=r'C:\Users\Administrator\Desktop\Experiment\Distance\Invarious\Coarse'
#imgs_folder=r'C:\Users\Administrator\Desktop\Experiment\Distance\Various\Coarse'
#imgs_folder=r'C:\Users\Administrator\Desktop\Experiment\Luminance\High\Coarse'
#imgs_folder=r'C:\Users\Administrator\Desktop\Experiment\Luminance\Low\Coarse'
#imgs_folder=r'C:\Users\Administrator\Desktop\Experiment\Texture\Obvious\Coarse'
#imgs_folder=r'C:\Users\Administrator\Desktop\Experiment\Texture\Unobvious\Coarse'

#output_folder=r'C:\Users\Administrator\Desktop\Contrast'
   
#Exp.ExperimentBlockModuleRatio(imgs_folder,output_folder,1)
#Exp.Experiment5AreaWeight(imgs_folder,output_folder,1)
#Exp.Experiment5AreaFactor(imgs_folder,output_folder,1)

#img_gray=Im.BatchImport(imgs_folder)[1][10]
#plt.imshow(img_gray,cmap='gray')
#cv2.imshow('gray',img_gray)

folder_texture=r'C:\Users\Administrator\Desktop\Experiment\Texture'

'''criteria of Critiria and Algorithm from DB or photos'''
folder_total=r'C:\Users\Administrator\Desktop\Experiment'

for name_this_experiment in os.listdir(folder_total):
    
    Exp.ExperimentComparison(folder_total+'\\'+name_this_experiment)
