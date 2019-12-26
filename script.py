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
#plt.imshow(img_gray,cmap='gray')
#cv2.imshow('gray',img_gray)

'''criteria of Critiria and Algorithm from DB or photos'''
'''change the histogram'''

#Con.ContrastCurve(imgs_folder,'Constant','5-Area')
#Con.ContrastCurve(imgs_folder,'Standard Deviation','5-Area')

def ForeAndBackDiscrimination(img_gray,e=0.1,show=False):
    
    #gray level histogram
    hist_gray=cv2.calcHist([img_gray],[0],None,[256],[0,256])
    
    #array of gray level and frequency
    array_gray_level=np.array([k for k in range(256)])
    array_frequency=hist_gray.ravel()/len(img_gray.ravel())
    
    #average value of gray level
    average_gray_level=np.sum(array_gray_level*array_frequency)
    
    #init threshold
    threshold_pre=average_gray_level
    threshold_next=threshold_pre+10*e
    
    count=1
    
    while np.abs(threshold_next-threshold_pre)>e:
        
        threshold_pre=cp.deepcopy(threshold_next)
        
        #divide the gray level
        '''background'''
        array_gray_level_b=array_gray_level[np.where(array_gray_level<=threshold_pre)]
        array_frequency_b=array_frequency[np.where(array_gray_level<=threshold_pre)]
        
        '''foreground'''
        array_gray_level_f=array_gray_level[np.where(array_gray_level>threshold_pre)]
        array_frequency_f=array_frequency[np.where(array_gray_level>threshold_pre)]
        
        #average value of gray level of b&f
        average_gray_level_b=np.sum(array_gray_level_b*array_frequency_b)/np.sum(array_frequency_b)
        average_gray_level_f=np.sum(array_gray_level_f*array_frequency_f)/np.sum(array_frequency_f)
        
        #update threhold
        threshold_next=0.5*(average_gray_level_f+average_gray_level_b)
    
    #    print(count,np.abs(threshold_next-threshold_pre))
        
        count+=1
      
    if show:
        
        #divide B and F
        img_binary=np.zeros(np.shape(img_gray))
        
        #background: 1 
        img_binary[np.where(img_gray>threshold_next)]=1

        #foreground: 0
        img_binary[np.where(img_gray<=threshold_next)]=0

        plt.figure(figsize=(10,6))
        
        plt.subplot(121)
        plt.imshow(img_gray,cmap='gray')
        plt.xticks([])
        plt.yticks([])
        
        plt.subplot(122)
        plt.imshow(img_binary,cmap='gray')
        plt.xticks([])
        plt.yticks([])
        
    return average_gray_level_b,average_gray_level_f

#luminance of background and foreground
L_b,L_f=ForeAndBackDiscrimination(img_gray)