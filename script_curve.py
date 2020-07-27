# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 10:50:07 2019

@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: script-AFC Curve
"""

import os
import cv2

import copy as cp
import numpy as np
import matplotlib.pyplot as plt

from scipy import interpolate 
from matplotlib.pyplot import MultipleLocator
from configuration_font import text_font,label_font,title_font,sample_font

#------------------------------------------------------------------------------
"""
B-Spline Interpolation on 1D

Args:
    X: X array
    Y: Y array
    n_step: amount of step
    
Returns:
    Interpolatd coordinates serial
""" 
def BSplineInterpolation(X,Y,n_step=100):
    
    X_new = np.linspace(min(X),max(X),n_step)

    Y_new = interpolate.splev(X_new,interpolate.splrep(X, Y))
    
    return [[X_new[k],Y_new[k]] for k in range(len(X_new))]

#------------------------------------------------------------------------------
"""
P-Chip Interpolation on 1D

Args:
    X: X array
    Y: Y array
    n_step: amount of step
    
Returns:
    Interpolatd coordinates serial
""" 
def PChipInterpolation(X,Y,n_step=100):
    
    X_new = np.linspace(min(X),max(X),n_step)

    Y_new = interpolate.PchipInterpolator(X, Y)(X_new)
    
    return [[X_new[k],Y_new[k]] for k in range(len(X_new))]

'''using that style and plot them'''
list_depth=[(k+1)*100 for k in range(10)]

#data from 100mm is from small chart plane, so that dot distance need to mutiply a factor (14/2.8)
list_focus_VCM_code=[850,580,500,460,440,430,410,400,400,400]
list_dot_distance=[100.8*5,231.6,156.0,111.6,89.3,75.5,64.3,55.7,49.3,44.6];

# plt.plot(list_depth,list_best_VCM_code)
# plt.plot(list_depth,list_dot_distance)

def Curve(list_x,
          list_y,
          str_title,
          str_xlabel,
          str_ylabel):
    
    #limit of x and y
    x_min,x_max=np.min(list_x),np.max(list_x)
    y_min,y_max=np.min(list_y),np.max(list_y)
    
    #tick step
    x_major_step=np.ceil((x_max-x_min)/10/50)*50
    x_minor_step=np.ceil((x_max-x_min)/10/50)*25
    y_major_step=np.ceil((y_max-y_min)/10/50)*50
    y_minor_step=np.ceil((y_max-y_min)/10/50)*25
    
    plt.figure(figsize=(13,6))
    
    '''p-chip interpolation'''
    smoothed_x_y=PChipInterpolation(list_x,list_y)

    x_smoothed=[this_x_y[0] for this_x_y in smoothed_x_y]
    y_smoothed=[this_x_y[1] for this_x_y in smoothed_x_y]

    plt.plot(x_smoothed,y_smoothed,'grey')
            
    # plt.plot(list_x,list_y,color='grey')
    
    for k in range(len(list_x)):
        
        plt.scatter(list_x[k],list_y[k],color='k')
        
        plt.annotate('%d'%list_y[k],
                         xy=(list_x[k],list_y[k]),
                         xytext=(list_x[k]+0.1*x_major_step,
                                 list_y[k]+0.1*y_major_step),
                        color='k',
                        fontproperties=sample_font)
        
    ax=plt.gca()
    
    ax.xaxis.set_major_locator(MultipleLocator(x_major_step))
    ax.xaxis.set_minor_locator(MultipleLocator(x_minor_step))
    ax.yaxis.set_major_locator(MultipleLocator(y_major_step))
    ax.yaxis.set_minor_locator(MultipleLocator(y_minor_step))
    
    #axis boundary
    plt.xlim([x_min-x_minor_step,x_max+x_minor_step])
    plt.ylim([y_min-y_minor_step,y_max+y_minor_step])  
     
    #set ticks fonts
    plt.tick_params(labelsize=12)
    labels=ax.get_xticklabels()+ax.get_yticklabels()
    
    #label fonts
    [this_label.set_fontname('Times New Roman') for this_label in labels]
        
    plt.title(str_title,FontProperties=title_font)
    
    plt.xlabel(str_xlabel,FontProperties=label_font)
    plt.ylabel(str_ylabel,FontProperties=label_font)

    #show the grid
    plt.grid()
    plt.show()
    
#plot curve of Focus VCM Code-Object Depth Curve
Curve(list_depth,
      list_focus_VCM_code,
      'Focus VCM Code-Object Depth Curve',
      'Object Depth (mm)',
      'Focus VCM Code (--)')

#plot curve of Dot Distance-Object Depth Curve
Curve(list_depth,
      list_dot_distance,
      'Dot Distance-Object Depth Curve',
      'Object Depth (mm)',
      'Dot Distance (pixel)')