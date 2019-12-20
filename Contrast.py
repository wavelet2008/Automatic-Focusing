# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 11:01:31 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title：Module-Contrast
"""

import cv2
import copy as cp
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.pyplot import MultipleLocator
from matplotlib.font_manager import FontProperties

import Import as Im
import Histogram as His

#legned font
legend_font={'family':'Gill Sans MT','weight':'normal','size':12}

#title font
annotation_font=FontProperties(fname=r"C:\Windows\Fonts\GILI____.ttf",size=16)

#annotation font
title_font=FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=20)

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
def GlobalContrast(img_gray,contrast_mode):
    
    amount_gray_level=256
    
    '''Constant'''
    #vectorization
    gray_array=His.HistogramArray(img_gray,amount_gray_level)
#    gray_array=img_gray.ravel()
    
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
    
    '''Standard Deviation'''
    #for frequency calculation
    pixel_amount=len(list(img_gray.ravel()))
    
    #step between gray level nearby
    step_gray_level=int(np.ceil(256/amount_gray_level))
    
    '''column vector'''
    hist_gray=cv2.calcHist([img_gray],[0],None,[amount_gray_level],[0,256])
    
    #x axis gray level
    list_gray_level=np.array([step_gray_level*(k+0.5) for k in range(amount_gray_level)])

    #y axis frequency
    list_frequency=np.array([frequency_this_gray_level/pixel_amount for frequency_this_gray_level in hist_gray])
  
    #range of luminance
#    range_gray_level=np.max(list_gray_level)-np.min(list_gray_level)
    
    #average value of luminance
    average_gray_level=np.sum(list_gray_level*list_frequency)
    
#    print(list_gray_level)
#    print(list_frequency)
#    print(sum(list_frequency))
#    print(len(list_gray_level),len(list_frequency))      
#    print(average_gray_level)
    
    #simplism
#    G=cp.deepcopy(amount_gray_level)
    L=cp.deepcopy(list_gray_level).ravel()
    P=cp.deepcopy(list_frequency).ravel()
    Lm=cp.deepcopy(average_gray_level)
#    R=cp.deepcopy(range_gray_level)
    
#    print(Li,Pi)
    
    #standard deviation
    if contrast_mode=='SD':
        
        SD=np.sum(P*np.square(L-Lm))
        
        return SD
        
    #standard deviation of logarithm of luminance
    if contrast_mode=='SDLG':
        
        '''np.log() stands for ln() in mathamatics'''
        LG_L=np.log2(L)
        LG_Lm=np.sum(P*LG_L)
        
#        print(np.sum(Pi))
#        print(LG_Lm)
#        print(LG_Li)
        
        SDLG=np.sum(P*np.square(LG_L-LG_Lm))
        
        return SDLG
        
    #space-average of Michelson contrast
    if contrast_mode=='SAM':
        
        SAM=0
        
        for i in range(len(L)):
            
            this_sum=0
            
            for j in range(len(L)):
                
                if i==j:
                    
                    continue
                
                this_sum+=P[j]*np.abs(L[i]-L[j])/(L[i]+L[j])
                
            SAM+=P[i]*this_sum
            
        return SAM
    
    #space-average logarithm of Michelson contrast
    if contrast_mode=='SALGM':
        
        SALGM=0
        
        for i in range(len(L)):
            
            this_sum=0
            
            for j in range(len(L)):
                
                if i==j:
                    
                    continue
                
                this_sum+=P[j]*np.log2(np.abs(L[i]-L[j])/(L[i]+L[j]))
                
            SALGM+=P[i]*this_sum
            
        return SALGM

    #space-average of Whittle contrast
    if contrast_mode=='SAW':
        
        SAW=0
        
        for i in range(len(L)):
            
            this_sum=0
            
            for j in range(len(L)):
                
                if i==j:
                    
                    continue
                
                this_sum+=P[j]*np.abs(L[i]-L[j])/np.min([L[i],L[j]])
                
            SAW+=P[i]*this_sum
            
        return SAW
    
    #space-average logarithm of Whittle contrast
    if contrast_mode=='SALGW':
        
        SALGW=0
        
        for i in range(len(L)):
            
            this_sum=0
            
            for j in range(len(L)):
                
                if i==j:
                    
                    continue
                
                this_sum+=P[j]*np.log2(np.abs(L[i]-L[j])/np.min([L[i],L[j]]))
                
            SALGW+=P[i]*this_sum
            
        return SALGW

#------------------------------------------------------------------------------
"""
Calculation of contrast with different mode with 5-Area

Args:
    img_gray: matrix of gray img
    contrast_mode: mode of contrast calculation ['Whittle','Simple','Michelson','RMS',
                                                 'SD','SDLG','SAM','SALGM','SAW','SALGW']
    
Returns:
    contrast value
"""
def Contrast5Area(img_gray,contrast_mode):
    
    #shrink factor
    window_size_factor=20
    
    height,width=np.shape(img_gray)
    
    if contrast_mode=='ANSI':
        
        #size of img patch
        patch_height=int(height/4)
        patch_width=int(width/4)
    
        #list index
        list_index_white=[[0,0],[0,2],[1,1],[1,3],[2,0],[2,2],[3,0],[3,2]]
        list_index_black=[[0,1],[0,3],[1,0],[1,2],[2,1],[2,3],[3,1],[3,3]]

        #list patch
        list_patches_white=[img_gray[i*patch_height:(i+1)*patch_height,j*patch_width:(j+1)*patch_width] for i,j in list_index_white]
        list_patches_black=[img_gray[i*patch_height:(i+1)*patch_height,j*patch_width:(j+1)*patch_width] for i,j in list_index_black]
        
        #B and W
#        white_average=np.average([np.average(HistogramArray(this_patch)) for this_patch in list_patches_white])
#        black_average=np.average([np.average(HistogramArray(this_patch)) for this_patch in list_patches_black])
        white_average=np.average([np.average(this_patch.ravel()) for this_patch in list_patches_white])
        black_average=np.average([np.average(this_patch.ravel()) for this_patch in list_patches_black])
       
        return white_average/black_average

    else:
        
        list_5_points=[[ height/4, width/4],
                       [ height/4,-width/4],
                       [-height/4,-width/4],
                       [-height/4, width/4],
                       [ height/2, width/2]]
        
        #size of area
        area_half_height,area_half_width=int(np.shape(img_gray)[0]/window_size_factor),int(np.shape(img_gray)[1]/window_size_factor)
        
        #calculate contrast in each area
        list_contrast_5_areas=[]
        list_weight_5_areas=[0.14,0.14,0.14,0.14,0.44]
#        list_weight_5_areas=[0.16,0.16,0.16,0.16,0.36]
#        list_weight_5_areas=[0.2,0.2,0.2,0.2,0.2]
        
        for i,j in list_5_points:
            
            this_area=img_gray[int(i)-area_half_height:int(i)+area_half_height,
                               int(j)-area_half_width:int(j)+area_half_width]

            #collect it
            list_contrast_5_areas.append(GlobalContrast(this_area,contrast_mode))

#        print(list_weight_5_areas)
#        print(list_contrast_5_areas)
#        print(np.array(list_weight_5_areas)*np.array(list_contrast_5_areas))
        
        return np.sum(np.array(list_weight_5_areas)*np.array(list_contrast_5_areas))

#------------------------------------------------------------------------------
"""
Plot contrast curve with pixel mode

Args:
    imgs_folder: images folder   
    mode: contrast series ['Constant','Standard Deviation']
    
Returns:
    None
"""
def ContrastCurve(imgs_folder,mode):
    
    list_imgs_bgr,list_imgs_gray,list_VCM_code=Im.BatchImport(imgs_folder)     
 
    list_contrast_mode=['Whittle',
                        'Simple',
                        'Michelson',
                        'RMS',
                        'SD',
                        'SDLG',
                        'SAM',
                        'SALGM',
                        'SAW',
                        'SALGW']
        
    list_contrast_color=['slategray',
                         'steelblue',
                         'rosybrown',
                         'maroon',
                         'lightsalmon',
                         'thistle',
                         'mediumturquoise',
                         'orchid',
                         'tan',
                         'mediumslateblue',]
    
    #map between mode and color
    if mode=='Constant':
    
        map_mode_color=dict(zip(list_contrast_mode[:4],list_contrast_color[:4]))
        
    if mode=='Standard Deviation':
    
        map_mode_color=dict(zip(list_contrast_mode[4:],list_contrast_color[4:]))
        
    fig,ax=plt.subplots(figsize=(10,6))
    
    #total value for plot
    total_normalized_contrast=[]
    
    for k in range(len(map_mode_color)):
        
        #color of this mode
        this_mode=list(map_mode_color.keys())[k]
        this_color=list(map_mode_color.values())[k]
        
        #contrast value 
        list_contrast=[]
        
        for this_img_gray in list_imgs_gray:

            list_contrast.append(Contrast5Area(this_img_gray,this_mode))
                
        #generalized contrast value
        list_normalized_contrast=[]
        
        for this_contrast in list_contrast:
            
            '''Normalization'''
            list_normalized_contrast.append((this_contrast-np.min(list_contrast))/(np.max(list_contrast)-np.min(list_contrast)))
         
        #collect the generalized contrast list
        total_normalized_contrast+=list_normalized_contrast
        
        plt.plot(list_VCM_code,
                 list_normalized_contrast,
                 color=this_color,
                 marker='.',
                 markersize=6,
                 linestyle='-',
                 label=this_mode)
        
        plt.legend(prop=legend_font)
#        
#        print(list_contrast)
#        print(list_generalized_contrast)
        
    #set ticks
    plt.tick_params(labelsize=12)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    
    #label fonts
    [this_label.set_fontname('Times New Roman') for this_label in labels]
        
    plt.title('Contrast-VCM Code Curve',FontProperties=title_font)  
    
    plt.xlabel('VCM Code',FontProperties=annotation_font)
    plt.ylabel('Contrast',FontProperties=annotation_font)
    
    #tick step
    x_major_step=50
    x_minor_step=25
    y_major_step=(max(total_normalized_contrast)-min(total_normalized_contrast))/10
    y_minor_step=(max(total_normalized_contrast)-min(total_normalized_contrast))/20
    
    #set locator
    ax.xaxis.set_major_locator(MultipleLocator(x_major_step))
    ax.xaxis.set_minor_locator(MultipleLocator(x_minor_step))
    ax.yaxis.set_major_locator(MultipleLocator(y_major_step))
    ax.yaxis.set_minor_locator(MultipleLocator(y_minor_step))
    