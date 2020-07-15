# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 10:18:02 2020

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Simulation of Auto Focus Calibration
"""

from o_circle import circle

import copy as cp
import numpy as np

import matplotlib.pyplot as plt

#list of offset sign
list_sign=[[+1,+1],
           [+1,-1],
           [-1,-1],
           [-1,+1]]

def EqualCircleArray(canvas,
                     n_interval,
                     radius_circle,
                     interval_circle):
    
    print()
    print('-- Equal Circle Array')
    
    center_canvas=[canvas.shape[0]/2,canvas.shape[1]/2]
    
    #each frame
    this_frame=cp.deepcopy(canvas)   
                     
    #init circle
    center_circle=circle()
    
    center_circle.radius=radius_circle
    center_circle.center=center_canvas
    
    center_circle.Init()
    
    #copy them
    for k_i in range(n_interval):
    
        for k_j in range(n_interval):
            
            for sign_i,sign_j in list_sign:
                
                for this_i,this_j in center_circle.points_inside:
                    
                    #copied points coordinates
                    this_i_copied=this_i+sign_i*k_i*interval_circle
                    this_j_copied=this_j+sign_j*k_j*interval_circle
                    
                    i_center_copied=center_canvas[0]+sign_i*k_i*interval_circle
                    j_center_copied=center_canvas[1]+sign_j*k_j*interval_circle
                    
                    if interval_circle<=i_center_copied<canvas.shape[0]-interval_circle\
                    and interval_circle<=j_center_copied<canvas.shape[1]-interval_circle:
                        
                        this_frame[this_i_copied,this_j_copied]=1  
                        
                    else:
                        
                        if 0<=this_i_copied<canvas.shape[0] and 0<=this_j_copied<canvas.shape[1]:
                        
                            this_frame[this_i_copied,this_j_copied]=1  
                
    plt.figure(figsize=(16,9))
    plt.imshow(this_frame,cmap='gray_r')
    
    plt.xticks([])
    plt.yticks([])  
    
def GenerateCircleSamples(offset_start,
                          offset_end,
                          n_interval,
                          radius_circle_original,
                          center_canvas,
                          zoom_factor_frame):
    
    #generate circle based on various radius
    samples_circle=[]
    
    for k in range(n_interval+1):
        
        this_offset=offset_start+(offset_end-offset_start)*k/n_interval
        this_zoom_factor=this_offset/offset_end
        
        #init circle
        center_circle=circle()
        
        center_circle.radius=radius_circle_original/this_zoom_factor/zoom_factor_frame
        center_circle.center=center_canvas
        
        center_circle.Init()
    
        samples_circle.append(center_circle)
    
    return samples_circle

def UnequalCircleEqual(canvas,
                       n_interval,
                       interval_circle,
                       samples_circle):
    
    print()
    print('-- Unequal Circle Array')
    
    center_canvas=[canvas.shape[0]/2,canvas.shape[1]/2]
    
    #each frame
    frame_original=cp.deepcopy(canvas) 

    for k_i in range(n_interval):

        for k_j in range(n_interval):
            
            k_valid=np.max([k_i,k_j])
            points_inside_valid=samples_circle[k_valid].points_inside
            
            for sign_i,sign_j in list_sign:
                
                for this_i,this_j in points_inside_valid:
                    
                    #copied points coordinates
                    this_i_copied=this_i+sign_i*k_i*interval_circle
                    this_j_copied=this_j+sign_j*k_j*interval_circle
                    
                    i_center_copied=center_canvas[0]+sign_i*k_i*interval_circle
                    j_center_copied=center_canvas[1]+sign_j*k_j*interval_circle
                    
                    if interval_circle<=i_center_copied<canvas.shape[0]-interval_circle\
                    and interval_circle<=j_center_copied<canvas.shape[1]-interval_circle:
                        
                        frame_original[this_i_copied,this_j_copied]=1  
                        
                    else:
                        
                        if 0<=this_i_copied<canvas.shape[0] and 0<=this_j_copied<canvas.shape[1]:
                        
                            frame_original[this_i_copied,this_j_copied]=1 
                            
    plt.figure(figsize=(16,9))
    plt.imshow(frame_original,cmap='gray_r')
    
    plt.xticks([])
    plt.yticks([]) 