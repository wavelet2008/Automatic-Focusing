# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 16:30:34 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title：Module-Discrimination of foreground and background
"""

import cv2
import copy as cp
import numpy as np
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------
"""
Calculation of luminance of foreground and background

Args:
    img_gray: matrix of gray img
    e: small value for convergence
    
Returns:
    contrast value
"""
def ForeAndBackLuminance(img_gray,e=0.1,show=False):
    
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