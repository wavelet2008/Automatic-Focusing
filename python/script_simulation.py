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
imgs_folder=r'C:\Users\ASUS\Desktop\Experiment\Random\Mechanical Arm'

C_P_S.FullSweep(imgs_folder,'Boccignone','5-Area')

# contain coarse and fine
# S_A_F.AutoFocusAnimation(imgs_folder,'Boccignone','Center')

# total_folder=r'C:\Users\ASUS\Desktop\Experiment\poLight-Medium-Coarse'

# for this_imgs_folder_name in os.listdir(total_folder):
    
#     this_imgs_folder=total_folder+'\\'+this_imgs_folder_name
    
#     C_P_S.FullSweep(this_imgs_folder,'Boccignone','Center')

    #contain coarse and fine
    # S_A_F.ImageAndContrast(this_imgs_folder,'Boccignone','Center')

