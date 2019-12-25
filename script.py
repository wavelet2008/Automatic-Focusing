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
   
#Exp.ExperimentBlockModuleRatio(imgs_folder,output_folder,1)
#Exp.Experiment5AreaWeight(imgs_folder,output_folder,1)
#Exp.Experiment5AreaFactor(imgs_folder,output_folder,1)

img_gray=Im.BatchImport(imgs_folder)[1][10]
plt.imshow(img_gray,cmap='gray')
#cv2.imshow('gray',img_gray)

'''criteria of Critiria and Algorithm from DB or photos'''
'''change the histogram'''

#Con.ContrastCurve(imgs_folder,'Constant','5-Area')
#Con.ContrastCurve(imgs_folder,'Standard Deviation','5-Area')
