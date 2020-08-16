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
import matplotlib.pyplot as plt

'''using that style and plot them'''
list_object_depth=[(k+1)*100 for k in range(10)]

#data from 100mm is from small chart plane, so that dot distance need to mutiply a factor (14/2.8)
list_focused_VCM_code=[850,580,500,460,440,420,410,400,400,390]

list_dot_scale=[2.8]+[14]*9
list_dot_distance_focused=[100.8,231.6,156.0,111.6,89.3,75.5,64.3,55.7,49.3,44.6]
list_dot_distance_200mm=[96.72,231.6,157.8,113.7,91,77.4,66.1,57.4,50.8,45.9]

list_image_distance_focused=np.array(list_object_depth)*np.array(list_dot_distance_focused)/np.array(list_dot_scale)*1.2/1000
list_image_distance_200mm=np.array(list_object_depth)*np.array(list_dot_distance_200mm)/np.array(list_dot_scale)*1.2/1000

# plt.plot(list_image_depth)

 #plot curve of Focus VCM Code-Object Depth Curve
O_C.Curve(list_object_depth,
          list_focused_VCM_code,
          'maroon',
          'Focused VCM Code',
          'Object Depth (mm)',
          'Focused VCM Code (--)',
          'Focused VCM Code-Object Depth Curve')

plt.savefig('a.png',dpi=300,bbox='tight')
# #plot curve of Dot Distance-Object Depth Curve
# O_C.Curve(list_object_depth,
#           list_image_distance_focused,
#           'olive',
#           'Image Distance,
#           'Object Depth (mm)',
#           'Image Distance (mm)',
#           'Image Distance-Object Depth Curve')

# folder=r'C:\Users\ASUS\Desktop\Experiment\Focus Calibration Lite-Small\100mm'

# img_src=plt.imread(folder+'\\top_VCM_850.png')
# plt.imshow(img_src)

# O_C.CurveBatch([list_object_depth]*2,
#                [list_image_distance_focused,list_image_distance_200mm],
#                list_contrast_color,
#                ['Focused VCM Code in various g','Focused VCM Code in g=200mm'],
#                'Object Depth (mm)',
#                'Image Distance (mm)',
#                'Image Distance-Object Depth Curve')

'''poLight'''
# list_focused_DAC_code=[656,512,464,448,416,416,400,400,400,400]
# list_focused_DAC_code=[678,480,444,426,406,400,394,388,384,378]

list_focused_DAC_code_300_1000=[464,436,416,400,394,388,384,378]
list_focused_DAC_code_60_300=[986,836,718,644,604,564,542,526,510,490,484,474,466]

list_object_distance_300_1000=list(np.linspace(300,1000,8))
list_object_distance_60_300=list(np.linspace(60,300,13))

# #plot curve of Focus VCM Code-Object Depth Curve
# O_C.Curve(list_object_distance_300_1000,
#           list_focused_DAC_code_300_1000,
#           'maroon',
#           'Focused DAC Code',
#           'Object Depth (mm)',
#           'Focused DAC Code (--)',
#           'Focused DAC Code-Object Depth Curve (poLight)')

#curve fitting and export the map into txt file
O_E.WriteTupleList2File(C_N_A.OptimizedFitting(list_object_distance_60_300,
                                               list_focused_DAC_code_60_300,
                                               241),
                        'g_code_60_300.txt')

O_E.WriteTupleList2File(C_N_A.OptimizedFitting(list_object_distance_300_1000,
                                               list_focused_DAC_code_300_1000,
                                               701),
                        'g_code_300_1000.txt')

O_C.CurveBatch([list_object_distance_60_300,list_object_distance_300_1000],
               [list_focused_DAC_code_60_300,list_focused_DAC_code_300_1000],
               ['maroon','olive'],
               ['60-300mm','300-1000mm'],
               'Object Depth (mm)',
               'Focused DAC Code (mm)',
               'Focused DAC Code-Object Depth Curve (poLight)')

plt.figure(figsize=(8,6))
code=np.linspace(300,700,5)
voltage=[8.2,13.5,19,24.4,29]

plt.plot(code,voltage,'k-')
plt.scatter(383,12.7,color='r')

plt.xlabel('DAC Code')
plt.ylabel('Voltage')

