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
output_folder=r'C:\Users\Administrator\Desktop\Contrast'
   
#Exp.ExperimentBlockModuleRatio(imgs_folder,output_folder)
#Exp.Experiment5AreaWeight(imgs_folder,output_folder)
#Exp.Experiment5AreaFactor(imgs_folder,output_folder)

'''find the best one'''
'''criteria of Critiria and Algorithm from DB or photos'''
'''change the histogram'''

#img_gray=Im.BatchImport(imgs_folder)[1][10]
#
#equ = cv2.equalizeHist(img_gray)
#
#Hist.GrayHistogramCurve(img_gray)
#
#Hist.GrayHistogramCurve(equ)

#img_rgb=Im.BatchImport(imgs_folder)[0][10]

all_mode_normalized_contrast=Con.ContrastCurve(imgs_folder,'Constant','5-Area')
#Con.ContrastCurve(imgs_folder,'Standard Deviation','Block Module',ratio=0.2)

#plt.imshow(img_gray,cmap='gray')
#cv2.imshow('gray',img_gray)

'''operate all mode normalized contrast'''
#weight depends on different contrast mode which relates to gray distribution
all_mode_weight=[1/len(all_mode_normalized_contrast)]*len(all_mode_normalized_contrast)
all_mode_max_index=[]

for this_list_normalized_contrast in all_mode_normalized_contrast:
    
    #sum of consecutive 3 element
    this_list_tri_sum=[]
    
    for k in range(1,len(this_list_normalized_contrast)-1):
        
        this_list_tri_sum.append(np.average(this_list_normalized_contrast[k-1:k+2]))
        
    all_mode_max_index.append(this_list_tri_sum.index(np.max(this_list_tri_sum))+1)

'''plot the bound'''
print(np.sum(np.array(all_mode_weight)*np.array(all_mode_max_index)))
