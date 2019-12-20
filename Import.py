# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 11:08:33 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title：Module-Import
"""

import os
import cv2

#------------------------------------------------------------------------------
"""
Import a batch of images from folder

Args:
    imgs_folder: images folder
    
Returns:
    list_imgs_bgr,list_imgs_gray,list_VCM_code
"""
def BatchImport(imgs_folder):
    
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
        
    return list_imgs_bgr,list_imgs_gray,list_VCM_code