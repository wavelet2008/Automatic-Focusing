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
To arrange the dictionary index in the order of a list

Args:
    which_dict: dictionary object to be arranged
    which_keys: keys list of new dictionary
    
Returns:
    new dictionary object
"""
def DictSortByIndex(which_dict,which_keys):
    
    #The results of operation
    that_dict={}
    
    #Traverse the new list and populate the dictionary
    for this_key in which_keys:
        
        that_dict[this_key]=which_dict[this_key]
        
    return that_dict

#------------------------------------------------------------------------------
"""
Import a batch of images from folder

Args:
    imgs_folder: images folder
    pre_fix: same part of imgs name
    
Returns:
    list_imgs_bgr,list_imgs_gray,list_VCM_code
"""
def BatchImages(imgs_folder,pre_fix='Near'):
    
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
        list_VCM_code.append(int(this_img_name.strip('.jpg').split(pre_fix)[-1]))
        
    #construct map between VCM code and imgs_gray/imgs_bgr
    map_VCM_code_imgs_bgr=dict(zip(list_VCM_code,list_imgs_bgr))
    map_VCM_code_imgs_gray=dict(zip(list_VCM_code,list_imgs_gray))
    
    #sort the VCM code list in an ascending order
    list_VCM_code.sort()

    #sort imgs
    list_imgs_bgr=list(DictSortByIndex(map_VCM_code_imgs_bgr,list_VCM_code).values())
    list_imgs_gray=list(DictSortByIndex(map_VCM_code_imgs_gray,list_VCM_code).values())
    
    return list_imgs_bgr,list_imgs_gray,list_VCM_code

'''combine images from imgs folder list'''
#------------------------------------------------------------------------------
"""
Combine images from imgs folder list

Args:
    list_imgs_folder: images folder list
    pre_fix: same part of imgs name
    
Returns:
    list_imgs_bgr,list_imgs_gray,list_VCM_code
"""
def CombineImages(list_imgs_folder,pre_fix='Near'):
    
    #define new list
    list_imgs_bgr,list_imgs_gray,list_VCM_code=[],[],[]
    
    for this_imgs_folder in list_imgs_folder:
        
        this_list_imgs_bgr,\
        this_list_imgs_gray,\
        this_list_VCM_code=BatchImages(this_imgs_folder,pre_fix)
        
        #combine this list
        list_imgs_bgr+=this_list_imgs_bgr
        list_imgs_gray+=this_list_imgs_gray
        list_VCM_code+=this_list_VCM_code
        
    #construct map between VCM code and imgs_gray/imgs_bgr
    map_VCM_code_imgs_bgr=dict(zip(list_VCM_code,list_imgs_bgr))
    map_VCM_code_imgs_gray=dict(zip(list_VCM_code,list_imgs_gray))
    
    #sort the VCM code list in an ascending order
    list_VCM_code=list(set(list_VCM_code))
    list_VCM_code.sort()
    
    #sort imgs
    list_imgs_bgr=list(DictSortByIndex(map_VCM_code_imgs_bgr,list_VCM_code).values())
    list_imgs_gray=list(DictSortByIndex(map_VCM_code_imgs_gray,list_VCM_code).values())
    
    return list_imgs_bgr,list_imgs_gray,list_VCM_code
        
        