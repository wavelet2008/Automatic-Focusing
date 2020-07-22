# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 11:08:33 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Import
"""

import os
import cv2

import operation_dictionary as O_D

from o_frame import frame

#pre_fix: same part of imgs name
pre_fix='12M_0500mm_VCM_bottom'

#------------------------------------------------------------------------------
"""
Import a batch of images from folder

Args:
    imgs_folder: images folder
    
Returns:
    list_imgs_bgr,list_imgs_gray,list_VCM_code
"""
def BatchImages(imgs_folder):
    
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
        
        if '.jpg' in this_img_name:
            
            list_VCM_code.append(int(this_img_name.strip('.jpg').split(pre_fix)[-1]))
        
        if '.png' in this_img_name:
            
            list_VCM_code.append(int(this_img_name.strip('.png').split(pre_fix)[-1]))
            
    #construct map between VCM code and imgs_gray/imgs_bgr
    map_VCM_code_imgs_bgr=dict(zip(list_VCM_code,list_imgs_bgr))
    map_VCM_code_imgs_gray=dict(zip(list_VCM_code,list_imgs_gray))
    
    #sort the VCM code list in an ascending order
    list_VCM_code.sort()

    #sort imgs
    list_imgs_bgr=list(O_D.DictSortByIndex(map_VCM_code_imgs_bgr,list_VCM_code).values())
    list_imgs_gray=list(O_D.DictSortByIndex(map_VCM_code_imgs_gray,list_VCM_code).values())
    
    return list_imgs_bgr,list_imgs_gray,list_VCM_code

'''combine images from imgs folder list'''
#------------------------------------------------------------------------------
"""
Combine images from imgs folder list

Args:
    list_imgs_folder: images folder list

Returns:
    list_imgs_bgr,list_imgs_gray,list_VCM_code
"""
def CombineImages(list_imgs_folder):
    
    #define new list
    list_imgs_bgr,list_imgs_gray,list_VCM_code=[],[],[]
    
    for this_imgs_folder in list_imgs_folder:
        
        this_list_imgs_bgr,\
        this_list_imgs_gray,\
        this_list_VCM_code=BatchImages(this_imgs_folder)
        
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
    list_imgs_bgr=list(O_D.DictSortByIndex(map_VCM_code_imgs_bgr,list_VCM_code).values())
    list_imgs_gray=list(O_D.DictSortByIndex(map_VCM_code_imgs_gray,list_VCM_code).values())
    
    return list_imgs_bgr,list_imgs_gray,list_VCM_code
        
#------------------------------------------------------------------------------
"""
Construct all frame object from folder

Args:
    imgs_folder: images folder
    
Returns:
    frame object list
"""
def FramesConstruction(imgs_folder):
    
    #final image object list and their paths
    list_frames=[]

    #traverse all image
    for this_img_name in os.listdir(imgs_folder):
        
        #define a new image object
        that_image=frame()

        that_image.path=imgs_folder+'\\'+this_img_name
        that_image.pre_fix=pre_fix
        
        that_image.Init()
        
        list_frames.append(that_image)
        
    list_VCM_code=[this_frame.VCM_code for this_frame in list_frames]
    
    #construct map between VCM code and frame object
    map_VCM_code_frames=dict(zip(list_VCM_code,list_frames))
    
    #sort the VCM code list in an ascending order
    list_VCM_code=list(set(list_VCM_code))
    list_VCM_code.sort()
    
    return list(O_D.DictSortByIndex(map_VCM_code_frames,list_VCM_code).values())   

'''combine frames from imgs folder list'''
#------------------------------------------------------------------------------
"""
Combine frames from imgs folder list

Args:
    list_imgs_folder: images folder list
    
Returns:
    list_imgs_bgr,list_imgs_gray,list_VCM_code
"""
def CombineFrames(list_imgs_folder):
    
    #total frames
    list_frames=[]
    
    for this_imgs_folder in list_imgs_folder:
        
        list_frames+=FramesConstruction(this_imgs_folder) 
        
    #total VCM code
    list_VCM_code=[this_frame.VCM_code for this_frame in list_frames]
    
    #construct map between VCM code and frame object
    map_VCM_code_frames=dict(zip(list_VCM_code,list_frames))
    
    #sort the VCM code list in an ascending order
    list_VCM_code=list(set(list_VCM_code))
    list_VCM_code.sort()
    
    return list(O_D.DictSortByIndex(map_VCM_code_frames,list_VCM_code).values())   