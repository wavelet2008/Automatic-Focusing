# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 10:54:44 2020

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Configuration for Simulation of Auto Focus Calibration
"""

from __init__ import *

import numpy as np

offset_end=5

n_interval=23

#regard the distance grow meter by 1 millimeter
interval_offset=0.0666

offset_start=offset_end-interval_offset*n_interval

canvas=np.zeros((1080,1920))

'''add the circle lap by lap'''
radius_circle_original=13
interval_circle_original=47

#generate output folder path
equal_folder_path=os.getcwd()+'//calibration plane frames/equal'
unequal_folder_path=os.getcwd()+'//calibration plane frames/unequal'

O_P.GenerateFolder(equal_folder_path)
O_P.GenerateFolder(unequal_folder_path)