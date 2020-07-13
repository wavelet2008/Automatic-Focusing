# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 17:15:48 2020

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Module-Histogram
"""

import os
import numpy as np
import matplotlib.pyplot as plt

size_fig=[16,9]

#------------------------------------------------------------------------------
"""
Determines and creates a folder under a path

Args:
    path: path to be preprocessed

Returns:
    None
"""
def GenerateFolder(path):

    #remove first space
    path=path.strip()
    
    #remove tail \ sign
    path=path.rstrip("\\")
 
    #determine if the path exists (True/False)
    Exist=os.path.exists(path)
 
    #determine the results
    if not Exist:
        
        #Create directory operation function: creates a directory if it does not exist 
        os.makedirs(path)
        
def PlotCircle(center,radius):
    
    # plt.scatter(x=center[0],y=center[1],s=300,color='k')
    
    plt.plot(center[0],
             center[1],
             marker='o',
             markersize=radius,
             markeredgewidth=1.3,
             markeredgecolor='black',
             markerfacecolor='black')
    
def Scaling(zoom_factor):
    
    plt.xlim([-0.5*size_fig[0]*zoom_factor-0.5,0.5*size_fig[0]*zoom_factor+0.5])
    plt.ylim([-0.5*size_fig[0]*zoom_factor-0.5,0.5*size_fig[1]*zoom_factor+0.5])
    
def MoveOn(offset):
    
    plt.xlim([-offset,size_fig[0]+offset])
    plt.ylim([-offset,size_fig[1]+offset])  
    
plt.figure(figsize=tuple(size_fig))
        
plt.xticks([])
plt.yticks([])

#regard the distance grow meter by 1 millimeter
folder_path=os.getcwd()+'//calibration plane frames'

GenerateFolder(folder_path)

d1=3
d2=5

n_interval=10

for k in range(n_interval+1):
    
    this_zoom_factor=(d1+k*(d2-d1)/n_interval)/d2
    this_radius=int(23/this_zoom_factor)
    
    print('')
    print('--frame:',k)
    print('--zoom factor:',this_zoom_factor)
    
    for x in range(size_fig[0]+1):
    
        for y in range(size_fig[1]+1):
            
            PlotCircle([+x,+y],this_radius)
            PlotCircle([+x,-y],this_radius)
            PlotCircle([-x,-y],this_radius)
            PlotCircle([-x,+y],this_radius)
        
    Scaling(this_zoom_factor)
    
    plt.xticks([])
    plt.yticks([])
    
    this_fig_path=folder_path+'//'+str(k)+'.png'
    plt.savefig(this_fig_path,dpi=300,bbox_inches='tight')
    
plt.close()