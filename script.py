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

        
#plt.imshow(img_gray,cmap='gray')
#cv2.imshow('gray',img_gray)

imgs_folder=r'C:\Users\Administrator\Desktop\Ink_Step50'
 
Con.ContrastCurve(imgs_folder,'Constant','Block Module',ratio=0.2)
#Con.ContrastCurve(imgs_folder,'Standard Deviation','Block Module',ratio=0.2)

#img_gray=Im.BatchImport(imgs_folder)[1][10]

output_folder=r'C:\Users\Administrator\Desktop\Contrast'

#annotation font
annotation_font=FontProperties(fname="C:\Windows\Fonts\GILI____.ttf",size=16)

#------------------------------------------------------------------------------
"""
Experiment: block module size factor

Args:
    imgs_folder: images folder  
    output_folder: figs output_folder

Returns:
    None
"""
def ExperimentBlockModuleRatio(imgs_folder,output_folder):
    
    final_folder=output_folder+'\\Block Module\\Ratio\\'
    
    #construct a folder
    Pa.GenerateFolder(final_folder)   
    
    #ratio 0.1-0.9 step is 0.1
    for k in range(1,10):
        
        this_ratio=0.1*k
        
        '''Constant'''
        #plot curve
        Con.ContrastCurve(imgs_folder,'Constant','Block Module',ratio=this_ratio)
    
        #add annotation
        plt.text(0,1,'Block Module Ratio: %.1f'%(this_ratio),FontProperties=annotation_font)
        plt.savefig(final_folder+str(k)+' (Constant).png')
        plt.close()
        
#        '''Standard Deviation'''
#        #plot curve
#        Con.ContrastCurve(imgs_folder,'Standard Deviation','Block Module',ratio=this_ratio)
#    
#        #add annotation
#        plt.text(0,1,'Block Module Ratio: %.1f'%(this_ratio),FontProperties=annotation_font)
#        plt.savefig(final_folder+str(k)+' (Standard Deviation).png')
#        plt.close()
        
#------------------------------------------------------------------------------
"""
Experiment: weight in 5 area method

Args:
    imgs_folder: images folder  
    output_folder: figs output_folder

Returns:
    None
"""
def Experiment5AreaWeight(imgs_folder,output_folder):
    
    final_folder=output_folder+'\\5-Area\\Weight\\'
    
    #construct a folder
    Pa.GenerateFolder(final_folder)   
    
    #ratio 0.1-0.9 step is 0.1
    for k in range(1,10):
        
        center_weight=0.16+0.04*k
        
        this_weight=[center_weight]+4*[(1-center_weight)/4]
        
#        print(this_weight)
        
        '''Constant'''
        #plot curve
        Con.ContrastCurve(imgs_folder,'Constant','5-Area',weight=this_weight)
    
        #add annotation
        plt.text(0,1,'5-Area Weight: %.2f-%.2f'%(this_weight[0],this_weight[1]),FontProperties=annotation_font)
        plt.savefig(final_folder+str(k)+' (Constant).png')
        plt.close()
        
#        '''Standard Deviation'''
#        #plot curve
#        Con.ContrastCurve(imgs_folder,'Standard Deviation','5-Area',weight=this_weight)
#    
#        #add annotation
#        plt.text(0,1,'5-Area Weight: %.2f-%.2f'%(this_weight[0],this_weight[1]),FontProperties=annotation_font)
#        plt.savefig(final_folder+str(k)+' (Standard Deviation).png')
#        plt.close()
        
#------------------------------------------------------------------------------
"""
Experiment: 5 area module factor

Args:
    imgs_folder: images folder  
    output_folder: figs output_folder

Returns:
    None
"""
def Experiment5AreaFactor(imgs_folder,output_folder):
    
    final_folder=output_folder+'\\5-Area\\Factor\\'
    
    #construct a folder
    Pa.GenerateFolder(final_folder)   
    
    #ratio 0.1-0.9 step is 0.1
    for k in range(1,10):
         
        this_factor=10+2*k
        
#        print(this_weight)
        
        '''Constant'''
        #plot curve
        Con.ContrastCurve(imgs_folder,'Constant','5-Area',factor=this_factor)
    
        #add annotation
        plt.text(0,1,'5-Area Factor: %d'%this_factor,FontProperties=annotation_font)
        plt.savefig(final_folder+str(k)+' (Constant).png')
        plt.close()
        
#        '''Standard Deviation'''
#        #plot curve
#        Con.ContrastCurve(imgs_folder,'Standard Deviation','5-Area',factor=this_factor)
#    
#        #add annotation
#        plt.text(0,1,'5-Area Factor: %d'%this_factor,FontProperties=annotation_font)
#        plt.savefig(final_folder+str(k)+' (Standard Deviation).png')
#        plt.close()
        
#ExperimentBlockModuleRatio(imgs_folder,output_folder)
#Experiment5AreaWeight(imgs_folder,output_folder)
#Experiment5AreaFactor(imgs_folder,output_folder)

'''find the best one'''
'''criteria of Critiria and Algorithm from DB or photos'''
'''change the histogram'''