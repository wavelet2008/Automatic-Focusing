# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 10:54:44 2020

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Simulation of Auto Focus Calibration
"""

from __init__ import *

import os,imageio

import copy as cp
import numpy as np

import matplotlib.pyplot as plt

#regard the distance grow meter by 1 millimeter
equal_folder_path=os.getcwd()+'//calibration plane frames/equal'
unequal_folder_path=os.getcwd()+'//calibration plane frames/unequal'

O_P.GenerateFolder(equal_folder_path)
O_P.GenerateFolder(unequal_folder_path)

canvas=np.zeros((1080,1920))

offset_start=3
offset_end=5

interval_circle=66

n_interval=23

#list of offset sign
list_sign=[[+1,+1],
           [+1,-1],
           [-1,-1],
           [-1,+1]]

'''fast method'''

def EqualCircleArray(canvas,radius_circle,interval_circle):
    
    print()
    print('-- Equal Circle Array')
    
    center_canvas=[canvas.shape[0]/2,canvas.shape[1]/2]
    
    #each frame
    this_frame=cp.deepcopy(canvas)   
                     
    #init circle
    center_circle=circle()
    
    center_circle.radius=radius_circle
    center_circle.center=[center_canvas[0],center_canvas[1]]
    
    center_circle.Init()
    
    #copy them
    for k_i in range(n_interval):
    
        for k_j in range(n_interval):
            
            for sign_i,sign_j in list_sign:
                
                for this_i,this_j in center_circle.points_inside:
                    
                    #copied points coordinates
                    this_i_copied=this_i+sign_i*k_i*interval_circle
                    this_j_copied=this_j+sign_j*k_j*interval_circle
                    
                    i_center_copied=center_circle.center[0]+sign_i*k_i*interval_circle
                    j_center_copied=center_circle.center[1]+sign_j*k_j*interval_circle
                    
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
    
# figures=[]

# #invarious offset in different frame associated VCM code
# for k in range(n_interval+1):
    
#     this_offset=offset_start+(offset_end-offset_start)*k/n_interval
#     this_zoom_factor=this_offset/offset_end
    
#     print('-- zoom factor:',this_zoom_factor)
    
#     #Generate circle array
#     EqualCircleArray(canvas,
#                       int(np.round(23/this_zoom_factor)),
#                       int(np.round(66/this_zoom_factor)))
    
#     this_fig_path=equal_folder_path+'//'+str(k)+'.png'
#     plt.savefig(this_fig_path,dpi=300,bbox_inches='tight')
    
#     #collect fig to create GIF
#     figures.append(imageio.imread(this_fig_path))
        
#     plt.close()

# #save GIF 
# '''operator experiment'''
# imageio.mimsave(folder_path+'\\'+'equal circle array.gif',figures,duration=0.23) 

'''add the circle lap by lap'''
radius_circle_original=23
interval_circle_original=66

center_canvas=[canvas.shape[0]/2,canvas.shape[1]/2]

#each frame
frame_original=cp.deepcopy(canvas) 
    
figures=[]

#invarious offset in different frame associated VCM code
for k in range(n_interval+1):
    
    this_offset=offset_start+(offset_end-offset_start)*k/n_interval
    this_zoom_factor=this_offset/offset_end
    
    print('-- zoom factor:',this_zoom_factor)
    
    '''wrong function'''
    #Generate circle array
    EqualCircleArray(frame_original,
                     int(np.round(radius_circle_original)),
                     int(np.round(interval_circle_original/this_zoom_factor)))
    
    this_fig_path=unequal_folder_path+'//'+str(k)+'.png'
    plt.savefig(this_fig_path,dpi=300,bbox_inches='tight')
    
    #collect fig to create GIF
    figures.append(imageio.imread(this_fig_path))
        
    plt.close()
                 
# #init circle
# center_circle=circle()

# center_circle.radius=radius_circle
# center_circle.center=[center_canvas[0],center_canvas[1]]
    
# #copy them
# for k_i in range(n_interval):

#     for k_j in range(n_interval):
        
#         for sign_i,sign_j in list_sign:
            
#             for this_i,this_j in center_circle.points_inside:
                
#                 #copied points coordinates
#                 this_i_copied=this_i+sign_i*k_i*interval_circle
#                 this_j_copied=this_j+sign_j*k_j*interval_circle
                
#                 i_center_copied=center_circle.center[0]+sign_i*k_i*interval_circle
#                 j_center_copied=center_circle.center[1]+sign_j*k_j*interval_circle
                
#                 if interval_circle<=i_center_copied<canvas.shape[0]-interval_circle\
#                 and interval_circle<=j_center_copied<canvas.shape[1]-interval_circle:
                    
#                     frame_original[this_i_copied,this_j_copied]=1  
                    
#                 else:
                    
#                     if 0<=this_i_copied<canvas.shape[0] and 0<=this_j_copied<canvas.shape[1]:
                    
#                         frame_original[this_i_copied,this_j_copied]=1 
