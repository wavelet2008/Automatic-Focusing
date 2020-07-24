# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 10:50:07 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: script-AFC Curve
"""

import os
import cv2

import copy as cp
import numpy as np
import matplotlib.pyplot as plt

'''using that style and plot them'''
list_depth=[(k+1)*100 for k in range(10)]
list_best_VCM_code=[850,580,500,460,440,430,410,400,400,400]
plt.plot(list_depth,list_best_VCM_code)


folder_path=r'F:\GitHub\KAMERAWERK\Calculation-Chart-Plane\Calib\\'

img_name='top_VCM_660.png'

img_src=plt.imread(folder_path+img_name)

plt.figure(figsize=(8,8))
plt.imshow(img_src)