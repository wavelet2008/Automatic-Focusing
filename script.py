# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 10:50:07 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title：Contrast Calculation
"""

import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import MultipleLocator
from matplotlib.font_manager import FontProperties

imgs_folder=r'C:\Users\Administrator\Desktop\Ink_Step50'

'''cv2 read image with the format of BGR meanwhile plt read it with the one of RGB'''
#list to contain img matrix (rgb and gray)
list_imgs_bgr=[]
list_imgs_gray=[]
list_VCM_code=[]

#traverse all image
for this_img_name in os.listdir(imgs_folder):
    
    this_img_path=imgs_folder+'\\'+this_img_name

    #read image
    this_img_rgb=cv2.imread(this_img_path)
    
    #convert rgb img to gray img
    this_img_gray=cv2.cvtColor(this_img_rgb,cv2.COLOR_BGR2GRAY)
    
    #collect it
    list_imgs_bgr.append(this_img_rgb)
    list_imgs_gray.append(this_img_gray)
    list_VCM_code.append(int(this_img_name.strip('.jpg').split('VCM')[-1]))
    
img_bgr=list_imgs_bgr[10]
img_gray=list_imgs_gray[10]

#plt.imshow(img_gray,cmap='gray')
#cv2.imshow('gray',img_gray)

#------------------------------------------------------------------------------
"""
Calculation of histogram

Args:
    img_bgr: matrix of bgr img
    img_gray: matrix of gray img
    
Returns:
    None
"""
def Histogram(img_bgr,img_gray):
    
    #plot gray histogram
    plt.figure()
    hist_gray=cv2.calcHist([img_gray],[0],None,[256],[0,256])
    plt.plot(hist_gray,color='k')
    plt.xlim([0, 256])
    plt.title('gray histogram')
    
    #plot BGR histogram
    plt.figure()
    colors=('b','g','r')
    
    #3 channels
    for i, col in enumerate(colors):
        
        hist= cv2.calcHist([img_bgr],[i],None,[256],[0, 256])
        plt.plot(hist,color=col)
        plt.xlim([0, 256])
        
    plt.title('BGR histogram')

'''
Contrast (Luminance Contrast) is the relationship between the luminance
of a brighter area of interest and that of an adjacent darker area.
'''

#------------------------------------------------------------------------------
"""
Calculation of contrast with different mode

Args:
    img_gray: matrix of gray img
    contrast_mode: mode of contrast calculation ['Whittle','Simple','Michelson','RMS']
    
Returns:
    contrast value
"""
def Contrast(img_gray,contrast_mode):
    
    #vectorization
    gray_array=img_gray.ravel()
    
    L_max=np.max(gray_array)
    L_min=np.min(gray_array)
    
    if contrast_mode=='Whittle':
        
        return (L_max-L_min)/L_min
    
    if contrast_mode=='Simple':
        
        return L_max/L_min
    
    if contrast_mode=='Michelson':
        
        return (L_max-L_min)/(L_max+L_min)
    
    if contrast_mode=='RMS':
        
        #mean value of img gray
        gray_average=np.average(gray_array)
        
        return np.average(np.square(np.array(gray_array)-gray_average))

#------------------------------------------------------------------------------
"""
Calculation of contrast with different mode from global pixels

Args:
    img_gray: matrix of gray img
    contrast_mode: mode of contrast calculation ['Whittle','Simple','Michelson','RMS']
    
Returns:
    global contrast value
"""
def GlobalContrast(img_gray,contrast_mode):
    
    return Contrast(img_gray,contrast_mode)

#------------------------------------------------------------------------------
"""
Plot contrast curve with pixel mode

Args:
    img_gray: matrix of gray img
    pixel_mode: mode of pixel ['Global','5-Area','16-Area']
    
Returns:
    None
"""
def ContrastCurve(img_gray,pixel_mode):
    
    #legned font
    legend_font={'family':'Gill Sans MT','weight':'normal','size':12}
    
    #title font
    annotation_font=FontProperties(fname=r"C:\Windows\Fonts\GILI____.ttf",size=16)
    
    #annotation font
    title_font=FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=20)
    
    list_contrast_mode=['Whittle','Simple','Michelson','RMS']
    list_contrast_color=['b','g','r','c']
    
    fig,ax=plt.subplots(figsize=(10,6))
    
    #total value for plot
    total_generalized_contrast=[]
    
    for k in range(len(list_contrast_mode)):
        
        #color of this mode
        this_mode=list_contrast_mode[k]
        this_color=list_contrast_color[k]
        
        #contrast value 
        list_contrast=[]
        
        for this_img_gray in list_imgs_gray:
        
            if pixel_mode=='Global':
                
                list_contrast.append(GlobalContrast(this_img_gray,this_mode))
    
        #generalized contrast value
        list_generalized_contrast=[]
        
        for this_contrast in list_contrast:
            
            list_generalized_contrast.append(this_contrast/np.max(list_contrast))
         
        #collect the generalized contrast list
        total_generalized_contrast+=list_generalized_contrast
        
        plt.plot(list_VCM_code,
                 list_generalized_contrast,
                 color=this_color,
                 marker='.',
                 markersize=6,
                 linestyle='-',
                 label=this_mode)
        
        plt.legend(prop=legend_font)
    
    #set ticks
    plt.tick_params(labelsize=12)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    
    #label fonts
    [this_label.set_fontname('Times New Roman') for this_label in labels]
        
    plt.title(pixel_mode+' Contrast-VCM Code Curve',FontProperties=title_font)  
    
    plt.xlabel('VCM Code',FontProperties=annotation_font)
    plt.ylabel('Contrast',FontProperties=annotation_font)
    
    #tick step
    x_major_step=100
    x_major_step=50
    y_major_step=(max(total_generalized_contrast)-min(total_generalized_contrast))/10
    y_minor_step=(max(total_generalized_contrast)-min(total_generalized_contrast))/20
    
    #set locator
    ax.xaxis.set_major_locator(MultipleLocator(x_major_step))
    ax.xaxis.set_minor_locator(MultipleLocator(x_major_step))
    ax.yaxis.set_major_locator(MultipleLocator(y_major_step))
    ax.yaxis.set_minor_locator(MultipleLocator(y_minor_step))

ContrastCurve(img_gray,'Global')