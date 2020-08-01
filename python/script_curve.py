# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 10:50:07 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: script-AFC Curve
"""

from __init__ import *

import numpy as np

'''using that style and plot them'''
list_object_depth=[(k+1)*100 for k in range(10)]

#data from 100mm is from small chart plane, so that dot distance need to mutiply a factor (14/2.8)
list_focused_VCM_code=[850,580,500,460,440,420,410,400,400,390]

list_dot_scale=[2.8]+[14]*9
list_dot_distance=[100.8,231.6,156.0,111.6,89.3,75.5,64.3,55.7,49.3,44.6];

list_image_distance=np.array(list_object_depth)*np.array(list_dot_distance)/np.array(list_dot_scale)*1.2/1000

# plt.plot(list_image_depth)

#plot curve of Focus VCM Code-Object Depth Curve
O_C.Curve(list_object_depth,
          list_focused_VCM_code,
          'maroon',
          'Focused VCM Code-Object Depth Curve',
          'Object Depth (mm)',
          'Focused VCM Code (--)',
          'Focused VCM Code')

#plot curve of Dot Distance-Object Depth Curve
O_C.Curve(list_object_depth,
          list_image_distance,
          'olive',
          'Image Distance-Object Depth Curve',
          'Object Depth (mm)',
          'Image Distance (mm)',
          'Image Distance')

# folder=r'C:\Users\ASUS\Desktop\Experiment\Focus Calibration Lite-Small\100mm'

# img_src=plt.imread(folder+'\\top_VCM_850.png')
# plt.imshow(img_src)