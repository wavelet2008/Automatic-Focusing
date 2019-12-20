# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 10:50:07 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title：Contrast Calculation
"""

import os
import cv2

import copy as cp
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.pyplot import MultipleLocator
from matplotlib.font_manager import FontProperties

import Contrast as Con
import Import as Im

#plt.imshow(img_gray,cmap='gray')
#cv2.imshow('gray',img_gray)

imgs_folder=r'C:\Users\Administrator\Desktop\Ink_Step50'
 
Con.ContrastCurve(imgs_folder,'Constant')
#Con.ContrastCurve(imgs_folder,'Standard Deviation')
#img_gray=Im.BatchImport(imgs_folder)[1][10]

'''block module'''
'''find the best one'''
'''Module folder'''
'''criteria of Critiria and Algorithm from DB or photos'''