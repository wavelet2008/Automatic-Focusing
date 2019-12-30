# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 17:54:22 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title：Module-Simulation of AutoFocus
"""

import os

#------------------------------------------------------------------------------
"""
Construct frame object from folder

Args:
    imgs_folder: images folder
    pre_fix: same part of imgs name
    
Returns:
    frame object list
"""
def FramesConstruction(imgs_folder,pre_fix):
    
    #final image object list
    list_frames=[]
    
    #traverse all image
    for this_img_name in os.listdir(imgs_folder):
        
        #define a new image object
        that_image=frame()

        that_image.path=imgs_folder+'\\'+this_img_name
        that_image.pre_fix=pre_fix
        
        that_image.Init()
        
        list_frames.append(that_image)

    return list_frames        
