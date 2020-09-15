# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 10:50:07 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: script-Automatic Focusing Simulation
"""

"""
demand:
    1 gif look like peak search
    2 optimized frames construction
"""

from __init__ import *

# imgs_folder=r'C:\Users\ASUS\Desktop\Experiment\poLight-Medium-Coarse\60mm'
# imgs_folder=r'C:\Users\ASUS\Desktop\Experiment\poLight-Medium-Fine\60mm'
# imgs_folder=r'C:\Users\ASUS\Desktop\Material\Screen\30cm-bright'

# C_P_S.PeakSearch(imgs_folder,'Boccignone','5-Area','Binary')

# contain coarse and fine
# S_A_F.AutoFocusAnimation(imgs_folder,'Boccignone','Center')

# total_folder=r'D:\Material\Plant'
total_folder=r'C:\Users\ASUS\Desktop\Material\Bottle'

for this_imgs_folder_name in os.listdir(total_folder):
    
    this_imgs_folder=total_folder+'\\'+this_imgs_folder_name
    
    # C_P_S.PeakSearch(this_imgs_folder,'Boccignone','Center','Binary')
    # C_P_S.PeakSearch(this_imgs_folder,'Boccignone','Center','Global')
    S_A_F.LensAnimation(this_imgs_folder,'Boccignone','Center','Binary')
    S_A_F.LensAnimation(this_imgs_folder,'Boccignone','Center','Global')
    
    S_A_F.FOVAnimation(this_imgs_folder,'Boccignone','Center','Binary')
    S_A_F.FOVsAnimation(this_imgs_folder,'Boccignone','Center','Global')
    
    # #contain coarse and fine
    # S_A_F.ImageAndContrast(this_imgs_folder,'Boccignone','Center')

# l=[1,2,3,4,5,6,7,8,9,8,7,6,5,4,3,2,1]
# idx_peak=C_P_S.GlobalSearch(l)

'''JL method'''
'''Rule-based'''
